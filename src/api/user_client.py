from src.api.base_client import BaseAPIClient


class UserAPIClient(BaseAPIClient):
    async def create_user(self, telegram_id: int, name: str, days: int = 30) -> dict:
        """
        Создание пользователя.
        POST /api/create_user
        """
        payload = {"telegram_id": telegram_id, "name": name, "days": days}
        result = await self.send_request("POST", "/api/create_user", json=payload)
        if "access_token" in result:
            self.jwt_token = result["access_token"]
        return result

    async def get_user(self) -> dict:
        """
        Получение данных пользователя.
        GET /api/get_user
        """
        return await self.send_request("GET", "/api/get_user")

    async def delete_user(self) -> dict:
        """
        Удаление пользователя.
        DELETE /api/delete_user
        """
        return await self.send_request("DELETE", "/api/delete_user")

    async def extend_subscription(self, days: int) -> dict:
        """
        Продление подписки.
        PUT /api/extend_subscription
        """
        payload = {"days": days}
        return await self.send_request("PUT", "/api/extend_subscription", json=payload)

    async def remove_client(self) -> dict:
        """
        Удаление клиента из WireGuard.
        PUT /api/remove_client
        """
        return await self.send_request("PUT", "/api/remove_client")

    async def confirm_payment(self) -> dict:
        """
        Подтверждение платежа.
        PUT /api/confirm_payment
        """
        return await self.send_request("PUT", "/api/confirm_payment")

    async def create_config(self) -> dict:
        """
        Создание VPN-конфигурации для пользователя.
        Проверка оплаты (is_paid) выполняется на сервере.
        """
        return await self.send_request("POST", "/api/create_config")

    async def get_configs(self) -> dict:
        """
        Получение списка VPN-конфигураций пользователя.
        """
        return await self.send_request("GET", "/api/get_configs")

    async def delete_config(self, config_id: int) -> dict:
        """
        Удаление VPN-конфигурации пользователя по её идентификатору.
        """
        endpoint = f"/del_config/{config_id}"
        return await self.send_request("DELETE", endpoint)
