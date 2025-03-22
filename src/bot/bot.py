import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.exceptions import TelegramAPIError
from configs.config import settings
from src.utils import logger
from src.api.user_client import UserAPIClient
from src.api.admin_client import AdminAPIClient
from database.crud import update_user_token
from src.bot.payments import PaymentManager
from src.bot.keyboards.navigations import get_main_menu_keyboard
from src.bot.keyboards.admin_keyboard import get_admin_main_keyboard
from src.bot.handlers.callbacks import (check_payment_callback,
                                        registration_callback,
                                        process_name,
                                        handle_admin_callbacks)
from src.bot.handlers.states import RegistrationState
from database.crud import update_user_label, get_user_label
from .handlers.commands import get_user_handler, create_config_handler
from src.bot.handlers.callbacks import router as menu_router


class TelegramBot:
    def __init__(self):
        self.bot = Bot(token=settings.TELEGRAM_API_KEY)
        self.dp = Dispatcher()

        self.user_api = UserAPIClient()
        self.admin_api = AdminAPIClient()
        self.payment_manager = PaymentManager(
                token=settings.YOOMONEY_TOKEN,
                receiver=settings.YOOMONEY_RECEIVER    
        )
        # commands
        self.dp.message.register(self.handle_start, Command("start"))
        self.dp.message.register(self.handle_get_user, Command("me"))
        self.dp.message.register(self.handle_payment, Command("pay"))
        self.dp.message.register(self.handle_admin_panel, Command("admin"))
        self.dp.message.register(self.handle_main_menu, Command("menu"))
        # callbacks

        self.dp.callback_query.register(check_payment_callback, lambda c: c.data.startswith("check_payment:"))
        self.dp.callback_query.register(registration_callback, lambda c: c.data.startswith("register:"))
        self.dp.callback_query.register(self.handle_payment_callback, lambda c: c.data.startswith("pay_callback"))
        self.dp.callback_query.register(handle_admin_callbacks, lambda c: c.data.startswith("admin:"))
        
        self.dp.message.register(process_name, RegistrationState.waiting_for_name)
        self.dp.message.register(self.handle_create_config, Command("create_config"))

        self.dp.include_router(menu_router)
        # self_assign
        self.bot.bot_instance = self

    async def handle_start(self, message: types.Message):
        text = (
        "👋 <b>Добро пожаловать!</b>\n\n"
        "Этот бот поможет вам получить доступ к защищённому VPN-соединению через WireGuard.\n"
        "После оплаты вы получите <b>конфигурационный файл</b>, который нужно импортировать в приложение WireGuard.\n\n"
        "📲 <b>Ссылки для установки WireGuard:</b>\n"
        "🔹 <a href=\"https://play.google.com/store/apps/details?id=com.wireguard.android&hl=ru\">Android</a>\n"
        "🔹 <a href=\"https://apps.apple.com/ru/app/wireguard/id1441195209\">iOS</a>\n"
        "🔹 <a href=\"https://www.wireguard.com/install/\">Windows / Linux / MacOS</a>\n\n"
        "📋 Ниже доступно главное меню:"
        )
        await message.answer(text, disable_web_page_preview=True, parse_mode="HTML", reply_markup=get_main_menu_keyboard())
        
        
    async def handle_payment_callback(self, callback_query: types.CallbackQuery):
        await callback_query.answer()
        await self.handle_payment(callback_query.message)

    async def handle_get_user(self, message: types.Message):
        await get_user_handler(self, message)

    async def handle_create_config(self, message: types.Message):
        await create_config_handler(self, message)

    async def handle_main_menu(self, message: types.Message):
        await message.answer("📋 Главное меню:", reply_markup=get_main_menu_keyboard())

    async def handle_payment(self, message: types.Message):
        telegram_id = message.from_user.id
        label = await get_user_label(telegram_id)
        if not label:
            label = self.payment_manager.generate_label(telegram_id)
        await update_user_label(telegram_id=telegram_id, label=label)

        keyboard = await self.payment_manager.get_payment_keyboard(amount=2, label=label)
        try:
            await message.edit_text("💳 Нажмите кнопку ниже, чтобы оплатить подписку на 30 дней:", reply_markup=keyboard)
        except TelegramAPIError:
            await message.answer("💳 Нажмите кнопку ниже, чтобы оплатить подписку на 30 дней:", reply_markup=keyboard)
    
    async def handle_admin_panel(self, message: types.Message):
        telegram_id = message.from_user.id
        response = await self.admin_api.get_admin_token(telegram_id)
        token = response.get("data", {}).get("access_token")
        if not token:
            await message.answer("⛔ У вас нет доступа.")
            return
        await update_user_token(telegram_id,
                                token)
        self.admin_api.jwt_token = token
        await message.answer("🛠 Панель администратора:", reply_markup=get_admin_main_keyboard())
    
    async def run(self):
        "Start the boot"
        await self.dp.start_polling(self.bot)


if __name__ == "__main__":
    bot = TelegramBot()
    asyncio.run(bot.run())
