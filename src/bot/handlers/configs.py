from aiogram import types
from src.utils.decorators import token_required, payed_required
from database.crud import get_user


@token_required
@payed_required
async def create_config_handler(self, message: types.Message):
    telegram_id = message.from_user.id
    user = await get_user(telegram_id)
    if user and user.is_admin:
        result = await self.admin_api.admin_create_config(telegram_id)
    else:
        result = await self.user_api.create_config()

    if "error" in result:
        await message.reply(f"Ошибка: {result['error']}")
    else:
        await message.reply("✅ Конфигурация успешно создана!")
