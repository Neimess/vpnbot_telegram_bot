from config.config import settings
from src.api.base_client import BaseAPIClient


class AdminAPIClient(BaseAPIClient):
    async def get_admin_token(self, telegram_id: int) -> dict:
        """
        Получение токена администратора по telegram_id и admin_secret.
        POST /api/auth/refresh_admin_token
        """
        payload = {"telegram_id": telegram_id, "admin_secret": settings.ADMIN_SECRET}
        return await self.send_request("POST", "/api/auth/refresh_admin_token", json=payload)

    async def get_all_users(self) -> dict:
        """
        Получение всех пользователей.
        GET /api/admin/users
        """
        return await self.send_request("GET", "/api/admin/users")

    async def get_user_by_id(self, telegram_id: int) -> dict:
        """
        Получение данных пользователя по telegram_id.
        GET /api/admin/user/{telegram_id}
        """
        payload = {"telegram_id": telegram_id}
        return await self.send_request("POST", "/api/admin/user", json=payload)

    # async def admin_delete_user(self, telegram_id: int) -> dict:
    #     """
    #     Удаление пользователя.
    #     DELETE /api/admin/remove_user/{telegram_id}
    #     """
    #     endpoint = f"/api/admin/remove_user/{telegram_id}"
    #     return await self.send_request("DELETE", endpoint)

    async def admin_extend_subscription(self, telegram_id: int, days: int) -> dict:
        """
        PUT /api/admin/extend_any_subscription
        """
        payload = {"telegram_id": telegram_id, "amount": days}
        return await self.send_request("PUT", "/api/admin/extend_any_subscription", json=payload)

    async def admin_create_config(self, telegram_id: int) -> dict:
        """
        PUT /api/admin/create_config
        """
        payload = {"telegram_id": telegram_id}
        return await self.send_request("PUT", "/api/admin/create_config", json=payload)

    async def get_payments(self) -> dict:
        """
        Получение истории платежей.
        GET /api/admin/payments
        """
        return await self.send_request("GET", "/api/admin/payments")
