from typing import Dict, Any, List, Optional
from .client import WeChatClient


class MenusManager:
    def __init__(self, client: WeChatClient):
        self.client = client
    
    async def create_menu(self, buttons: List[Dict[str, Any]]) -> Dict[str, Any]:
        endpoint = "/cgi-bin/menu/create"
        data = {"button": buttons}
        return await self.client.post(endpoint, data=data)
    
    async def get_menu(self) -> Dict[str, Any]:
        endpoint = "/cgi-bin/menu/get"
        return await self.client.get(endpoint)
    
    async def delete_menu(self) -> Dict[str, Any]:
        endpoint = "/cgi-bin/menu/delete"
        return await self.client.delete(endpoint)
    
    async def create_conditional_menu(
        self,
        buttons: List[Dict[str, Any]],
        matchrule: Dict[str, Any]
    ) -> Dict[str, Any]:
        endpoint = "/cgi-bin/menu/addconditional"
        data = {
            "button": buttons,
            "matchrule": matchrule
        }
        return await self.client.post(endpoint, data=data)
    
    async def delete_conditional_menu(self, menuid: str) -> Dict[str, Any]:
        endpoint = "/cgi-bin/menu/delconditional"
        data = {"menuid": menuid}
        return await self.client.post(endpoint, data=data)
    
    async def try_match_menu(self, user_id: str) -> Dict[str, Any]:
        endpoint = "/cgi-bin/menu/trymatch"
        data = {"user_id": user_id}
        return await self.client.post(endpoint, data=data)
    
    async def get_current_selfmenu_info(self) -> Dict[str, Any]:
        endpoint = "/cgi-bin/get_current_selfmenu_info"
        return await self.client.get(endpoint)
