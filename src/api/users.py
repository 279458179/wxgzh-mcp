from typing import Dict, Any, List, Optional
from .client import WeChatClient


class UsersManager:
    def __init__(self, client: WeChatClient):
        self.client = client
    
    async def get_user_info(self, openid: str, lang: str = "zh_CN") -> Dict[str, Any]:
        endpoint = "/cgi-bin/user/info"
        params = {
            "openid": openid,
            "lang": lang
        }
        return await self.client.get(endpoint, params=params)
    
    async def get_user_list(self, next_openid: str = "") -> Dict[str, Any]:
        endpoint = "/cgi-bin/user/get"
        params = {"next_openid": next_openid}
        return await self.client.get(endpoint, params=params)
    
    async def get_batch_user_info(self, user_list: List[Dict[str, str]]) -> Dict[str, Any]:
        endpoint = "/cgi-bin/user/info/batchget"
        data = {"user_list": user_list}
        return await self.client.post(endpoint, data=data)
    
    async def update_user_remark(self, openid: str, remark: str) -> Dict[str, Any]:
        endpoint = "/cgi-bin/user/info/updateremark"
        data = {
            "openid": openid,
            "remark": remark
        }
        return await self.client.post(endpoint, data=data)
    
    async def get_user_tags(self) -> Dict[str, Any]:
        endpoint = "/cgi-bin/tags/get"
        return await self.client.get(endpoint)
    
    async def create_tag(self, name: str) -> Dict[str, Any]:
        endpoint = "/cgi-bin/tags/create"
        data = {"tag": {"name": name}}
        return await self.client.post(endpoint, data=data)
    
    async def update_tag(self, tag_id: int, name: str) -> Dict[str, Any]:
        endpoint = "/cgi-bin/tags/update"
        data = {
            "tag": {
                "id": tag_id,
                "name": name
            }
        }
        return await self.client.post(endpoint, data=data)
    
    async def delete_tag(self, tag_id: int) -> Dict[str, Any]:
        endpoint = "/cgi-bin/tags/delete"
        data = {"tag": {"id": tag_id}}
        return await self.client.post(endpoint, data=data)
    
    async def get_tag_users(self, tag_id: int, next_openid: str = "") -> Dict[str, Any]:
        endpoint = "/cgi-bin/tag/get"
        data = {
            "tagid": tag_id,
            "next_openid": next_openid
        }
        return await self.client.post(endpoint, data=data)
    
    async def batch_tag_users(self, tag_id: int, openid_list: List[str]) -> Dict[str, Any]:
        endpoint = "/cgi-bin/tags/members/batchtagging"
        data = {
            "tagid": tag_id,
            "openid_list": openid_list
        }
        return await self.client.post(endpoint, data=data)
    
    async def batch_untag_users(self, tag_id: int, openid_list: List[str]) -> Dict[str, Any]:
        endpoint = "/cgi-bin/tags/members/batchuntagging"
        data = {
            "tagid": tag_id,
            "openid_list": openid_list
        }
        return await self.client.post(endpoint, data=data)
    
    async def get_user_id_list_by_tag(self, tag_id: int) -> Dict[str, Any]:
        endpoint = "/cgi-bin/tags/getid"
        data = {"tagid": tag_id}
        return await self.client.post(endpoint, data=data)
    
    async def blacklist_user(self, openid_list: List[str]) -> Dict[str, Any]:
        endpoint = "/cgi-bin/tags/members/blacklist"
        data = {"openid_list": openid_list}
        return await self.client.post(endpoint, data=data)
    
    async def unblacklist_user(self, openid_list: List[str]) -> Dict[str, Any]:
        endpoint = "/cgi-bin/tags/members/unblacklist"
        data = {"openid_list": openid_list}
        return await self.client.post(endpoint, data=data)
