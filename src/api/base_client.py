import aiohttp
import random
import logging
from configs import settings


class BaseAPIClient:
    def __init__(self, jwt_token: str = None):
        """
        :param jwt_token: JWT-токен для авторизации (если требуется)
        """
        self.servers = settings.API_SERVERS
        self.jwt_token = jwt_token

    def get_server_url(self) -> str:
        return random.choice(self.servers)

    def get_headers(self) -> dict:
        headers = {"Content-Type": "application/json"}
        if self.jwt_token:
            headers["Authorization"] = f"Bearer {self.jwt_token}"
        return headers

    async def send_request(self, method: str, endpoint: str, json: dict = None) -> dict:
        url = f"{self.get_server_url()}{endpoint}"
        async with aiohttp.ClientSession() as session:
            async with session.request(method, url, headers=self.get_headers(), json=json) as response:
                status = response.status
                try:
                    data = await response.json()
                except Exception:
                    data = {"error": "Invalid JSON response from server"}

                return {"status": status, "data": data}
