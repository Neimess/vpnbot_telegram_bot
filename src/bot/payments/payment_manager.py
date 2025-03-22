from uuid import uuid4
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types.web_app_info import WebAppInfo
from src.bot.keyboards.navigations import get_back_button
from .yoomoney_client import YooMoneyClient


class PaymentManager:
    def __init__(self, token: str, receiver: str):
        self.yoomoney = YooMoneyClient(token, receiver)

    def generate_label(self, user_id: int) -> str:
        return f"{user_id}-{uuid4()}"

    async def get_payment_keyboard(self, amount: float, label: str) -> InlineKeyboardMarkup:
        url = await self.yoomoney.create_payment_link(amount=amount, label=label)
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text=f"💳 Оплатить {amount}₽", web_app=WebAppInfo(url=url)),
                    InlineKeyboardButton(text="✅ Я оплатил", callback_data=f"check_payment:{label}"),
                ],
                [InlineKeyboardButton(text="🔙 Назад", callback_data="menu:back")],
            ]
        )

    async def check_payment(self, label: str) -> bool:
        return await self.yoomoney.is_payment_successful(label)
