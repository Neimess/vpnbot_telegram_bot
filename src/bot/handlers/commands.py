import asyncio
from babel.dates import format_datetime
from aiogram import types

from database.connection import database
from src.bot.keyboards.settings_keyboards import get_user_keyboard
from src.bot.keyboards.auth_keyboard import get_registration_keyboard
from src.utils import error_handler, log, token_required, payed_required, logger
from database.crud import get_user, create_user
from datetime import datetime
from src.utils.helpers import handle_api_error
from src.bot.keyboards.navigations import get_main_menu_keyboard
from aiogram.utils.keyboard import InlineKeyboardBuilder


@log
async def start_handler(message: types.Message):
    """
    Обработчик команды /start.
    Выводит приветственное сообщение с инлайн-клавиатурой для регистрации.
    """
    await message.answer(
        "Добро пожаловать! 🚀\nНажмите кнопку ниже, чтобы зарегистрироваться.", reply_markup=get_registration_keyboard()
    )


@token_required
async def get_user_handler(self, message: types.Message):
    try:
        response = await self.user_api.get_user()
        status = response["status"]
        data = response["data"]

        if status != 200:
            await handle_api_error(message, status, data.get("error"))
            return

        expires_at_raw = data.get("expires_at")
        try:
            expires_at = datetime.fromisoformat(expires_at_raw.replace("Z", "+00:00"))
            expires_at_str = format_datetime(expires_at, "d MMMM y 'г.' HH:mm", locale="ru")
        except Exception:
            expires_at_str = expires_at_raw

        active_configs = len(data.get("configs") or [])
        profile_text = (
            "🔐 <b>Личный кабинет</b>\n\n"
            "🆔 <b>Ваши данные:</b>\n"
            f"▪️ ID: <code>{data.get('telegram_id')}</code>\n"
            f"▪️ Имя: <b>{data.get('name')}</b>\n"
            f"▪️ Администратор: {'✅ Да' if data.get('is_admin') else '❌ Нет'}\n\n"
            "💳 <b>Подписка:</b>\n"
            f"▪️ Статус оплаты: {'✅ Оплачено' if data.get('is_paid') else '❌ Не оплачено'}\n"
            f"▪️ Действует до: <b>{expires_at_str}</b>\n\n"
            "⚙️ <b>Конфигурации:</b>\n"
            f"▪️ Активных: <b>{active_configs}</b>\n\n"
        )

        await message.answer(profile_text, parse_mode="HTML")

        configs = data.get("configs", [])[:3]
        media = []

        for config in configs:
            content = config.get("config")
            name = config.get("config_path", "config.conf").split("/")[-1]
            if content:
                file = types.BufferedInputFile(content.encode("utf-8"), filename=f"{name}")
                media.append(types.InputMediaDocument(media=file))

        if media:
            await message.bot.send_media_group(chat_id=message.chat.id, media=media)

    except Exception as e:
        logger.exception(f"[get_user_handler] Unexpected error: {e}")
        await message.reply("❗ Произошла внутренняя ошибка. Попробуйте позже.")


@token_required
@payed_required
async def create_config_handler(self, message: types.Message):
    try:
        response = await self.user_api.create_config()
        status = response["status"]
        data = response["data"]

        if status != 200:
            await handle_api_error(message, status, data.get("error"))
            return

        config_name = data.get("config_name", "vpn_config")
        config_text = data.get("config").get("config")
        if not config_text:
            await message.reply("✅ Конфигурация создана, но сервер не вернул файл.")
            return

        await message.reply_document(
            document=types.BufferedInputFile(config_text.encode(), filename=f"{config_name}.conf"),
            caption="✅ Конфигурация успешно создана! 🔐",
        )

    except Exception as e:
        logger.exception(f"[create_config_handler] Unexpected error: {e}")
        await message.reply("❗ Внутренняя ошибка. Попробуйте позже.")
