from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton


def get_main_menu_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="🧾 Личный кабинет", callback_data="menu:profile"),
        InlineKeyboardButton(text="💳 Оплатить", callback_data="menu:pay"),
    )
    builder.row(
        InlineKeyboardButton(text="⚙️ Конфигурации", callback_data="menu:configs"),
        InlineKeyboardButton(text="🔐 Регистрация", callback_data="menu:registration"),
    )
    builder.row(
        InlineKeyboardButton(text="🆘 Помощь", callback_data="menu:help"),
    )
    return builder.as_markup()


def get_back_button():
    return InlineKeyboardBuilder().row(InlineKeyboardButton(text="🔙 Назад", callback_data="menu:back")).as_markup()
