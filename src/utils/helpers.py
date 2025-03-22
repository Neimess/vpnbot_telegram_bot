async def handle_api_error(message_or_cb, status: int, error: str):
    if status == 403:
        await message_or_cb.reply("💳 Подписка неактивна. Пожалуйста, оплатите через /pay.")
    elif status == 401:
        await message_or_cb.reply("🔐 Авторизация недействительна. Повторите регистрацию.")
    elif status == 404:
        await message_or_cb.reply("❌ Данные не найдены. Попробуйте зарегистрироваться заново.")
    elif status == 500:
        await message_or_cb.reply("💥 Временная ошибка сервера. Попробуйте позже.")
    else:
        await message_or_cb.reply(f"❗ {error or 'Произошла ошибка'}")
