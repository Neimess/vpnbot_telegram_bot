import asyncio

from yoomoney import Client, Quickpay


class YooMoneyClient:
    def __init__(self, token: str, receiver: str):
        self.client = Client(token=token)
        self.receiver = receiver

    async def create_payment_link(self, amount: float, label: str, comment: str = "Подписка VPN"):
        def sync_call():
            quickpay = Quickpay(
                receiver=self.receiver,
                quickpay_form="shop",
                targets=comment,
                paymentType="SB",
                sum=amount,
                label=label,
            )
            return quickpay.redirected_url

        return await asyncio.to_thread(sync_call)

    async def is_payment_successful(self, label: str) -> bool:
        def sync_check():
            history = self.client.operation_history(label=label)
            return any(op.status == "success" for op in history.operations)

        return await asyncio.to_thread(sync_check)
