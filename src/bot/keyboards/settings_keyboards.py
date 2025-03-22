from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_settings_keyboard() -> InlineKeyboardMarkup:
    """
    Главное меню настроек.
    """
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="📍 Регион", callback_data="settings_region"),
            ],
            [
                InlineKeyboardButton(text="🏠 Комнаты", callback_data="settings_rooms"),
            ],
            [
                InlineKeyboardButton(text="💰 Цена", callback_data="settings_price"),
            ],
            [
                InlineKeyboardButton(text="🚶 Метро", callback_data="settings_only_foot"),
            ],
            [
                InlineKeyboardButton(text="📏 Квадратура", callback_data="settings_set_area"),
            ],
            [
                InlineKeyboardButton(text="🏗 Год постройки", callback_data="setting_house_year"),
            ],
            [InlineKeyboardButton(text="✅ Готово", callback_data="settings_done")],
        ]
    )
    return keyboard


def get_region_keyboard() -> InlineKeyboardMarkup:
    keyboard_buttons = []
    regions = {"Москва": 1, "Санкт-Петербург": 2, "Сочи": 3, "Казань": 4}
    for name, reg_id in regions.items():
        keyboard_buttons.append(InlineKeyboardButton(text=name, callback_data=f"set_region_{reg_id}"))
    keyboard = InlineKeyboardMarkup(inline_keyboard=[keyboard_buttons])
    return keyboard


def get_rooms_keyboard() -> InlineKeyboardMarkup:
    rooms_options = ["Студия", "1", "2", "3+", "Любое"]
    keyboard_buttons = []
    for room in rooms_options:
        keyboard_buttons.append(InlineKeyboardButton(text=room, callback_data=f"set_rooms_{room}"))
    keyboard = InlineKeyboardMarkup(inline_keyboard=[keyboard_buttons])
    return keyboard


def get_price_keyboard() -> InlineKeyboardMarkup:
    price_ranges = {
        "2-5 млн": (2000000, 5000000),
        "5-10 млн": (5000000, 10000000),
        "10-13 млн": (10000000, 13000000),
        "10-20 млн": (10000000, 20000000),
        "20+ млн": (20000000, None),
    }
    keyboard_buttons = []
    for label, (min_price, max_price) in price_ranges.items():
        keyboard_buttons.append(
            InlineKeyboardButton(
                text=label, callback_data=f"set_price_{min_price}_{max_price if max_price is not None else 'None'}"
            )
        )
    keyboard = InlineKeyboardMarkup(inline_keyboard=[keyboard_buttons])
    return keyboard


def get_only_foot_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🚶 Только пешком", callback_data="set_only_foot_2"),
            ],
            [
                InlineKeyboardButton(text="🚗 Далеко от метро", callback_data="set_only_foot_-2"),
            ],
            [
                InlineKeyboardButton(text="❌ Не важно", callback_data="set_only_foot_0"),
            ],
        ]
    )
    return keyboard


def get_main_menu() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🔍 Начать поиск", callback_data="start_search"),
            ],
            [
                InlineKeyboardButton(text="⚙ Настройки", callback_data="settings"),
            ],
            [
                InlineKeyboardButton(text="❌ Отмена", callback_data="cancel"),
            ],
        ]
    )
    return keyboard


def get_area_keyboard() -> InlineKeyboardMarkup:
    area_options = {
        "от 30 м²": "set_area_30",
        "от 40 м²": "set_area_40",
        "от 50 м²": "set_area_50",
        "от 60 м²": "set_area_60",
        "от 70 м²": "set_area_70",
    }

    keyboard_buttons = [[InlineKeyboardButton(text=label, callback_data=callback)] for label, callback in area_options.items()]
    keyboard_buttons.append([InlineKeyboardButton(text="🔙 Назад", callback_data="settings")])

    return InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)


def get_year_keyboard() -> InlineKeyboardMarkup:
    year_option = {
        "от 1950": "set_year_1950",
        "от 1960": "set_year_1960",
        "от 1970": "set_year_1970",
        "от 1980": "set_year_1980",
        "от 1990": "set_year_1990",
        "от 2000": "set_year_2000",
        "от 2010": "set_year_2010",
        "от 2020": "set_year_2020",
    }
    keyboard_buttons = [[InlineKeyboardButton(text=label, callback_data=callback)] for label, callback in year_option.items()]
    keyboard_buttons.append([InlineKeyboardButton(text="🔙 Назад", callback_data="settings")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)


def get_user_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📄 Мои конфиги", callback_data="my_configs")],
            [InlineKeyboardButton(text="💸 Оплатить / Продлить", callback_data="pay_callback")],
        ]
    )
    return keyboard
