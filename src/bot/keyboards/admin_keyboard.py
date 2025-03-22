from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def get_admin_main_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="👥 Пользователи", callback_data="admin:users")],
            [InlineKeyboardButton(text="💳 Подписки", callback_data="admin:subscriptions")],
            [InlineKeyboardButton(text="🛠 Конфиги", callback_data="admin:configs")],
            [InlineKeyboardButton(text="🔙 Назад", callback_data="menu:back")],
        ]
    )

def get_admin_users_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📋 Все пользователи", callback_data="admin:all_users")],
            [InlineKeyboardButton(text="🔎 Найти по ID", callback_data="admin:find_user")],
            [InlineKeyboardButton(text="🗑 Удалить по ID", callback_data="admin:delete_user")],
            [InlineKeyboardButton(text="🔙 Назад", callback_data="admin:main")],
        ]
    )

def get_admin_subscriptions_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📅 Продлить подписку", callback_data="admin:extend_sub")],
            [InlineKeyboardButton(text="🔙 Назад", callback_data="admin:main")],
        ]
    )

    
def get_admin_configs_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⚙ Создать конфиг", callback_data="admin:create_config_select:0")],
            [InlineKeyboardButton(text="🔙 Назад", callback_data="admin:main")],
        ]
    )

def get_admin_subscriptions_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📅 Продлить подписку", callback_data="admin:extend_subscription_select:0")],
            [InlineKeyboardButton(text="🔙 Назад", callback_data="admin:main")],
        ]
    )
