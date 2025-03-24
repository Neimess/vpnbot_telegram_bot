from functools import wraps

import jwt
import jwt.exceptions
from aiogram.types import CallbackQuery, Message

from config import settings
from database.crud import get_user, update_user_token
from src.api import AuthAPIClient
from src.utils.loggers import logger


def error_handler(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            self = args[0]
            logger.error(f"Handled error in {func.__name__}: {str(e)}")
            await self.bot.send_message(chat_id=settings.TELEGRAM_ADMIN_ID, text=f"Error in {func.__name__}: {str(e)[:4096]}")
            return {"status_code": 500, "message": "Internal Server Error"}

    return wrapper


def token_required(handler_func):
    @wraps(handler_func)
    async def wrapper(self, obj, *args, **kwargs):
        telegram_id = None
        if isinstance(obj, Message):
            telegram_id = obj.chat.id
        elif isinstance(obj, CallbackQuery):
            telegram_id = obj.message.chat.id
        else:
            telegram_id = getattr(self, "telegram", None)
        if telegram_id is None:
            logger.error("Не удалось определить telegram_id для проверки токена.")
            return {"status_code": 400, "message": "Invalid Telegram ID"}

        user = await get_user(telegram_id)
        if not user or not user.access_token:
            logger.warning(f"Пользователь {telegram_id} не зарегистрирован или токен отсутствует.")

            if isinstance(obj, Message):
                await obj.answer("❗ Вы не зарегистрированы. Пожалуйста, авторизуйтесь в боте.")
            elif isinstance(obj, CallbackQuery):
                await obj.answer("❗ Вы не зарегистрированы. Авторизуйтесь через /start.", show_alert=True)

            return

        try:
            jwt.decode(user.access_token, settings.JWT_SECRET, algorithms=["HS256"])
            logger.info("Токен пользователя %s действителен.", telegram_id)
            self.user_api.jwt_token = user.access_token

        except jwt.exceptions.ExpiredSignatureError:
            logger.warning("Токен пользователя %s просрочен. Пытаемся обновить...", telegram_id)
            auth_client = AuthAPIClient(jwt_token=None)
            refresh_result = await auth_client.refresh_token(telegram_id)

            logger.info(f"Refresh Token Response: {refresh_result}")

            if (
                "status" not in refresh_result
                or refresh_result["status"] != 200
                or "data" not in refresh_result
                or "access_token" not in refresh_result["data"]
            ):
                logger.error(f"Ошибка обновления токена для {telegram_id}: {refresh_result}")
                return {"status_code": 401, "message": "Unauthorized: Token Expired"}

            new_token = refresh_result["data"]["access_token"]
            await update_user_token(telegram_id, new_token)
            self.user_api.jwt_token = new_token
            logger.info("Токен пользователя %s успешно обновлён.", telegram_id)

        except jwt.exceptions.DecodeError:
            logger.error(f"❌ Токен пользователя {telegram_id} повреждён или неверен.")
            return {"status_code": 401, "message": "Unauthorized: Invalid Token"}

        except Exception as e:
            logger.error("Ошибка при проверке токена: %s", e)
            return {"status_code": 500, "message": "Internal Server Error"}

        return await handler_func(self, obj, *args, **kwargs)

    return wrapper


def payed_required(handler_func):
    @wraps(handler_func)
    async def wrapper(self, obj, *args, **kwargs):
        telegram_id = None
        if isinstance(obj, Message):
            telegram_id = obj.chat.id
        elif isinstance(obj, CallbackQuery):
            telegram_id = obj.message.chat.id
        else:
            telegram_id = getattr(self, "telegram", None)

        if telegram_id is None:
            logger.error("Не удалось определить telegram_id для проверки оплаты.")
            return {"status_code": 400, "message": "Invalid Telegram ID"}

        user = await get_user(telegram_id)
        if not user:
            logger.warning("Пользователь не найден при проверке оплаты: %s", telegram_id)
            return {"status_code": 404, "message": "User Not Found"}

        if not user.is_paid:
            logger.info("Попытка доступа без оплаты: %s", telegram_id)
            return {"status_code": 402, "message": "Payment Required"}

        return await handler_func(self, obj, *args, **kwargs)

    return wrapper
