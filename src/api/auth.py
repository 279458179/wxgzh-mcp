from typing import Dict, Any
from .client import WeChatClient


class AuthManager:
    def __init__(self, client: WeChatClient):
        self.client = client
    
    async def get_token_status(self) -> Dict[str, Any]:
        return self.client._get_token_status()
    
    async def refresh_token(self) -> Dict[str, Any]:
        new_token = await self.client.get_access_token(force_refresh=True)
        return {
            "access_token": new_token,
            "status": "refreshed"
        }
    
    async def verify_token(self) -> Dict[str, Any]:
        try:
            status = await self.get_token_status()
            if not status["has_token"]:
                return {
                    "valid": False,
                    "reason": "No token available"
                }
            
            if status["is_expired"]:
                return {
                    "valid": False,
                    "reason": "Token expired"
                }
            
            return {
                "valid": True,
                "expires_in": status["expires_in"]
            }
        except Exception as e:
            return {
                "valid": False,
                "reason": str(e)
            }
