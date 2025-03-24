from datetime import datetime

from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.crud import confirm_local_payment, create_user, get_user, get_user_label
from src.bot.keyboards.admin_keyboard import (
    get_admin_configs_keyboard,
    get_admin_main_keyboard,
    get_admin_subscriptions_keyboard,
    get_admin_users_keyboard,
)
from src.bot.keyboards.navigations import get_main_menu_keyboard
from src.utils.helpers import handle_api_error

from .states import AdminState, RegistrationState

router = Router()


def get_router() -> Router:
    return router


async def cancel(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text("❌ Действие отменено.")


async def check_payment_callback(callback_query: types.CallbackQuery):
    telegram_id = callback_query.message.chat.id
    label = await get_user_label(telegram_id)
    bot_instance = callback_query.bot.bot_instance

    if not await bot_instance.payment_manager.check_payment(label):
        await callback_query.answer("❌ Платёж не найден. Попробуйте позже.", show_alert=True)
        return

    user = await get_user(telegram_id)
    if not user:
        await callback_query.answer("⚠️ Пользователь не найден. Пройдите регистрацию через /start.", show_alert=True)
        return

    response = await bot_instance.user_api.get_user()
    status = response.get("status")
    data = response.get("data", {})

    if status != 200:
        await handle_api_error(callback_query.message, status, data.get("error"))
        return

    is_paid_server = data.get("is_paid", False)
    now = datetime.now()

    if user.expires_at and user.expires_at > now:
        if not is_paid_server:
            await bot_instance.user_api.confirm_payment()
        await callback_query.message.edit_text("✅ У вас уже активна подписка.")
        return

    if user.expires_at and user.expires_at < now:
        await callback_query.message.edit_text(
            "⏳ Срок действия вашей подписки истёк.\n💳 Пожалуйста, оплатите повторно через /pay."
        )
        return

    await confirm_local_payment(telegram_id)
    await bot_instance.user_api.confirm_payment()
    await callback_query.message.edit_text("✅ Платёж подтверждён. Подписка активирована!")


async def registration_callback(callback_query: types.CallbackQuery, state: FSMContext):
    """
    Обработчик нажатия на кнопку регистрации.
    Запрашивает у пользователя ввести имя для регистрации.
    """
    await callback_query.answer()
    await callback_query.message.answer("Введите ваше имя для регистрации")
    await state.set_state(RegistrationState.waiting_for_name)


async def process_name(message: types.Message, state: FSMContext):
    bot_instance = message.bot.bot_instance
    telegram_id = message.from_user.id
    name = message.text

    response = await bot_instance.user_api.create_user(telegram_id, name)
    status = response.get("status")
    data = response.get("data", {})

    if status != 201:
        await handle_api_error(message, status, data.get("error"))
        return

    await create_user(telegram_id, name, data.get("access_token"))
    await message.reply("✅ Вы успешно зарегистрированы!\nТеперь вы можете использовать /me или /pay.")
    await state.clear()


@router.callback_query(lambda c: c.data.startswith("menu:"))
async def handle_main_menu(callback_query: types.CallbackQuery, state: FSMContext):
    data = callback_query.data.split(":")[1]
    bot_instance = callback_query.bot.bot_instance
    await callback_query.answer()

    if data == "profile":
        await bot_instance.handle_get_user(callback_query.message)
    elif data == "pay":
        await bot_instance.handle_payment(callback_query.message)
    elif data == "configs":
        await callback_query.message.edit_text(
            "⚙️ Управление конфигурациями:",
            reply_markup=InlineKeyboardBuilder()
            .row(
                InlineKeyboardButton(text="Создать 🛠", callback_data="config:create"),
                InlineKeyboardButton(text="Удалить 🗑", callback_data="config:delete"),
            )
            .row(InlineKeyboardButton(text="🔙 Назад", callback_data="menu:back"))
            .as_markup(),
        )
    elif data == "back":
        await callback_query.message.edit_text("📋 Главное меню:", reply_markup=get_main_menu_keyboard())
    elif data == "help":
        await callback_query.message.edit_text(
            "🆘 <b>Помощь</b>\n\n"
            "/start – регистрация\n"
            "/me – профиль\n"
            "/pay – оплата\n"
            "/create_config – создать конфиг\n\n"
            '📬 По всем вопросам: <a href="https://t.me/Neimes">свяжитесь с поддержкой</a>',
            parse_mode="HTML".row(InlineKeyboardButton(text="🔙 Назад", callback_data="menu:back")).as_markup(),
        )
    elif data == "registration":
        await registration_callback(callback_query, state)


@router.callback_query(lambda c: c.data == "config:create")
async def config_create_callback(callback_query: types.CallbackQuery):
    await callback_query.answer()
    bot_instance = callback_query.bot.bot_instance
    await bot_instance.handle_create_config(callback_query.message)


@router.callback_query(lambda c: c.data == "config:delete")
async def config_delete_callback(callback_query: types.CallbackQuery):
    await callback_query.answer("🔧 Функция удаления пока в разработке.")


async def handle_admin_callbacks(callback_query: types.CallbackQuery, state: FSMContext):
    bot_instance = callback_query.bot.bot_instance
    data = callback_query.data.split(":")[1]
    await callback_query.answer()

    if data == "main":
        await callback_query.message.edit_text("🛠 Панель администратора:", reply_markup=get_admin_main_keyboard())
    elif data == "users":
        await callback_query.message.edit_text("👥 Пользователи:", reply_markup=get_admin_users_keyboard())
    elif data == "subscriptions":
        await callback_query.message.edit_text("💳 Управление подписками:", reply_markup=get_admin_subscriptions_keyboard())
    elif data == "configs":
        await callback_query.message.edit_text("🛠 Управление конфигурациями:", reply_markup=get_admin_configs_keyboard())
    elif data == "all_users":
        response = await bot_instance.admin_api.get_all_users()
        users = response.get("data", [])
        text = "\n".join([f"▪️ {u['telegram_id']} | {u['name']}" for u in users[:10]]) or "❌ Нет пользователей"
        await callback_query.message.edit_text(f"👥 Список пользователей:\n\n{text}")
    elif callback_query.data.startswith("admin:create_config_select:"):
        try:
            offset = int(callback_query.data.split(":")[2])
        except (IndexError, ValueError):
            offset = 0
        await show_user_selection(callback_query, offset, action="create_config")

    # Выполнение действия над выбранным пользователем
    elif callback_query.data.startswith("admin:extend_subscription_select:"):
        try:
            offset = int(callback_query.data.split(":")[2])
        except (IndexError, ValueError):
            offset = 0
        await show_user_selection(callback_query, offset, action="extend_subscription")

    elif data.startswith("extend_subscription_for"):
        target_id = int(data.split(":")[2])
        result = await bot_instance.admin_api.admin_extend_subscription(target_id, days=30)
        if result["status"] == 200:
            await callback_query.message.edit_text("📅 Подписка продлена на 30 дней.")
        else:
            await handle_api_error(callback_query.message, result["status"], result["data"].get("error"))

    else:
        await callback_query.message.answer("⏳ Эта функция пока в разработке.")


@router.message(AdminState.waiting_for_user_id_lookup)
async def handle_lookup_user(message: types.Message, state: FSMContext):
    bot_instance = message.bot.bot_instance
    try:
        telegram_id = int(message.text)
        result = await bot_instance.admin_api.get_user_by_id(telegram_id)
        data = result.get("data", {})
        if result["status"] != 200:
            await handle_api_error(message, result["status"], data.get("error"))
            return
        user_info = (
            f"🔎 <b>Пользователь:</b>\n"
            f"▪️ ID: <code>{data.get('telegram_id')}</code>\n"
            f"▪️ Имя: <b>{data.get('name')}</b>\n"
            f"▪️ Подписка до: <b>{data.get('expires_at')}</b>\n"
            f"▪️ Админ: {'✅' if data.get('is_admin') else '❌'}\n"
        )
        await message.answer(user_info, parse_mode="HTML")
    except Exception:
        await message.answer("❌ Ошибка. Убедитесь, что введён правильный ID.")
    await state.clear()


@router.message(AdminState.waiting_for_user_id_delete)
async def handle_delete_user(message: types.Message, state: FSMContext):
    bot_instance = message.bot.bot_instance
    try:
        telegram_id = int(message.text)
        result = await bot_instance.admin_api.admin_delete_user(telegram_id)
        if result["status"] == 200:
            await message.answer("✅ Пользователь успешно удалён.")
        else:
            await handle_api_error(message, result["status"], result["data"].get("error"))
    except Exception:
        await message.answer("❌ Ошибка удаления. Введите корректный Telegram ID.")
    await state.clear()


@router.message(AdminState.waiting_for_user_id_extend)
async def handle_extend_user(message: types.Message, state: FSMContext):
    bot_instance = message.bot.bot_instance
    try:
        telegram_id = int(message.text)
        result = await bot_instance.admin_api.admin_extend_subscription(telegram_id, days=30)
        if result["status"] == 200:
            await message.answer("📅 Подписка продлена на 30 дней.")
        else:
            await handle_api_error(message, result["status"], result["data"].get("error"))
    except Exception:
        await message.answer("❌ Ошибка продления. Убедитесь, что ID корректный.")
    await state.clear()


async def show_user_selection(callback_query: types.CallbackQuery, offset: int, action: str):
    bot_instance = callback_query.bot.bot_instance
    response = await bot_instance.admin_api.get_all_users()
    users = response.get("data", [])

    per_page = 5
    total = len(users)
    users_page = users[offset : offset + per_page]

    kb = InlineKeyboardBuilder()
    for user in users_page:
        uid = user["telegram_id"]
        name = user.get("name", "без имени")
        if action == "create_config":
            cb = f"admin:create_config_for:{uid}"
            text = f"📁 {uid} | {name}"
        else:
            cb = f"admin:extend_subscription_for:{uid}"
            text = f"📅 {uid} | {name}"
        kb.row(InlineKeyboardButton(text=text, callback_data=cb))

    nav_row = []
    if offset > 0:
        nav_row.append(InlineKeyboardButton(text="⬅️ Назад", callback_data=f"admin:{action}_select:{offset - per_page}"))
    if offset + per_page < total:
        nav_row.append(InlineKeyboardButton(text="➡️ Далее", callback_data=f"admin:{action}_select:{offset + per_page}"))
    if nav_row:
        kb.row(*nav_row)
    kb.row(InlineKeyboardButton(text="🔙 Назад", callback_data="admin:main"))

    title = "👤 Выберите пользователя:"
    await callback_query.message.edit_text(title, reply_markup=kb.as_markup())
