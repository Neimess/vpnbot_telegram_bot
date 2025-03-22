from src.api.base_client import BaseAPIClient


class AuthAPIClient(BaseAPIClient):
    async def refresh_token(self, telegram_id: int) -> dict:
        """
        Обновление JWT-токена.
        POST /api/auth/refresh_token telegram ID в теле запроса.
        """
        payload = {"telegram_id": telegram_id}
        return await self.send_request("POST", "/api/auth/refresh_token", json=payload)
