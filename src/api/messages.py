from typing import Dict, Any, Optional, List
from .client import WeChatClient


class MessagesManager:
    def __init__(self, client: WeChatClient):
        self.client = client
    
    async def send_text_message(self, touser: str, content: str) -> Dict[str, Any]:
        endpoint = "/cgi-bin/message/custom/send"
        data = {
            "touser": touser,
            "msgtype": "text",
            "text": {"content": content}
        }
        return await self.client.post(endpoint, data=data)
    
    async def send_image_message(self, touser: str, media_id: str) -> Dict[str, Any]:
        endpoint = "/cgi-bin/message/custom/send"
        data = {
            "touser": touser,
            "msgtype": "image",
            "image": {"media_id": media_id}
        }
        return await self.client.post(endpoint, data=data)
    
    async def send_voice_message(self, touser: str, media_id: str) -> Dict[str, Any]:
        endpoint = "/cgi-bin/message/custom/send"
        data = {
            "touser": touser,
            "msgtype": "voice",
            "voice": {"media_id": media_id}
        }
        return await self.client.post(endpoint, data=data)
    
    async def send_video_message(
        self, 
        touser: str, 
        media_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        endpoint = "/cgi-bin/message/custom/send"
        video_data = {"media_id": media_id}
        if title:
            video_data["title"] = title
        if description:
            video_data["description"] = description
            
        data = {
            "touser": touser,
            "msgtype": "video",
            "video": video_data
        }
        return await self.client.post(endpoint, data=data)
    
    async def send_article_message(self, touser: str, media_id: str) -> Dict[str, Any]:
        endpoint = "/cgi-bin/message/custom/send"
        data = {
            "touser": touser,
            "msgtype": "mpnews",
            "mpnews": {"media_id": media_id}
        }
        return await self.client.post(endpoint, data=data)
    
    async def send_link_message(
        self, 
        touser: str, 
        title: str,
        description: str,
        url: str,
        thumb_media_id: Optional[str] = None
    ) -> Dict[str, Any]:
        endpoint = "/cgi-bin/message/custom/send"
        link_data = {
            "title": title,
            "description": description,
            "url": url
        }
        if thumb_media_id:
            link_data["thumb_url"] = thumb_media_id
            
        data = {
            "touser": touser,
            "msgtype": "link",
            "link": link_data
        }
        return await self.client.post(endpoint, data=data)
    
    async def send_miniprogram_message(
        self,
        touser: str,
        appid: str,
        title: str,
        pagepath: str,
        thumb_media_id: str
    ) -> Dict[str, Any]:
        endpoint = "/cgi-bin/message/custom/send"
        data = {
            "touser": touser,
            "msgtype": "miniprogrampage",
            "miniprogrampage": {
                "title": title,
                "appid": appid,
                "pagepath": pagepath,
                "thumb_media_id": thumb_media_id
            }
        }
        return await self.client.post(endpoint, data=data)
    
    async def broadcast_message(
        self,
        msgtype: str,
        filter: Dict[str, Any],
        content: Optional[str] = None,
        media_id: Optional[str] = None,
        articles: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        endpoint = "/cgi-bin/message/mass/sendall"
        msg_data = {"msgtype": msgtype}
        
        if msgtype == "text":
            msg_data["text"] = {"content": content}
        elif msgtype == "image":
            msg_data["image"] = {"media_id": media_id}
        elif msgtype == "voice":
            msg_data["voice"] = {"media_id": media_id}
        elif msgtype == "video":
            msg_data["video"] = {"media_id": media_id}
        elif msgtype == "mpnews":
            msg_data["mpnews"] = {"media_id": media_id}
        elif msgtype == "news":
            msg_data["news"] = {"articles": articles}
        elif msgtype == "wxcard":
            msg_data["wxcard"] = {"card_id": media_id}
        
        data = {
            "filter": filter,
            **msg_data
        }
        
        return await self.client.post(endpoint, data=data)
    
    async def send_template_message(
        self,
        touser: str,
        template_id: str,
        data: Dict[str, Any],
        url: Optional[str] = None,
        miniprogram: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        endpoint = "/cgi-bin/message/template/send"
        msg_data = {
            "touser": touser,
            "template_id": template_id,
            "data": data
        }
        
        if url:
            msg_data["url"] = url
        
        if miniprogram:
            msg_data["miniprogram"] = miniprogram
        
        return await self.client.post(endpoint, data=msg_data)
