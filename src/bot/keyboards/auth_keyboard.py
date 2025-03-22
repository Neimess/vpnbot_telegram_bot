from aiogram import types


def get_registration_keyboard() -> types.InlineKeyboardMarkup:
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[[types.InlineKeyboardButton(text="Зарегистрироваться", callback_data="register:form")]]
    )
    return keyboard
