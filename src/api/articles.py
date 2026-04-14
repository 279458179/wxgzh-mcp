from typing import Dict, Any, List
from .client import WeChatClient


class ArticlesManager:
    def __init__(self, client: WeChatClient):
        self.client = client
    
    async def create_article(self, articles: List[Dict[str, Any]]) -> Dict[str, Any]:
        endpoint = "/cgi-bin/material/add_news"
        data = {"articles": articles}
        return await self.client.post(endpoint, data=data)
    
    async def get_article(self, media_id: str) -> Dict[str, Any]:
        endpoint = "/cgi-bin/material/get_material"
        data = {"media_id": media_id}
        return await self.client.post(endpoint, data=data)
    
    async def update_article(
        self, 
        media_id: str, 
        index: int, 
        articles: Dict[str, Any]
    ) -> Dict[str, Any]:
        endpoint = "/cgi-bin/material/update_news"
        data = {
            "media_id": media_id,
            "index": index,
            "articles": articles
        }
        return await self.client.post(endpoint, data=data)
    
    async def delete_article(self, media_id: str) -> Dict[str, Any]:
        endpoint = "/cgi-bin/material/del_material"
        data = {"media_id": media_id}
        return await self.client.post(endpoint, data=data)
    
    async def preview_article(
        self, 
        media_id: str,
        touser: str = None,
        towxname: str = None
    ) -> Dict[str, Any]:
        endpoint = "/cgi-bin/message/mass/preview"
        data = {
            "msgtype": "mpnews",
            "mpnews": {"media_id": media_id}
        }
        
        if touser:
            data["touser"] = touser
        elif towxname:
            data["towxname"] = towxname
        else:
            raise ValueError("Either touser or towxname must be provided")
        
        return await self.client.post(endpoint, data=data)
    
    async def get_article_list(self, offset: int = 0, count: int = 20) -> Dict[str, Any]:
        endpoint = "/cgi-bin/material/batchget_material"
        data = {
            "type": "news",
            "offset": offset,
            "count": count
        }
        return await self.client.post(endpoint, data=data)
