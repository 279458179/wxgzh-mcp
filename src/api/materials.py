from typing import Dict, Any, Optional
import os
from .client import WeChatClient


class MaterialsManager:
    def __init__(self, client: WeChatClient):
        self.client = client
    
    async def upload_temporary_material(
        self, 
        file_path: Optional[str] = None,
        file_data: Optional[bytes] = None,
        material_type: str = "image"
    ) -> Dict[str, Any]:
        if not file_path and not file_data:
            raise ValueError("Either file_path or file_data must be provided")
        
        if file_path:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")
            
            filename = os.path.basename(file_path)
            with open(file_path, "rb") as f:
                file_data = f.read()
        else:
            filename = f"temp_file.{material_type}"
        
        files = {
            "media": (filename, file_data)
        }
        
        endpoint = f"/cgi-bin/media/upload"
        params = {"type": material_type}
        
        return await self.client.post(endpoint, params=params, files=files)
    
    async def add_permanent_material(
        self,
        material_type: str,
        file_path: Optional[str] = None,
        file_data: Optional[bytes] = None,
        articles: Optional[list] = None
    ) -> Dict[str, Any]:
        if material_type == "news":
            if not articles:
                raise ValueError("Articles must be provided for news type")
            data = {"articles": articles}
            endpoint = "/cgi-bin/material/add_news"
            return await self.client.post(endpoint, data=data)
        
        if not file_path and not file_data:
            raise ValueError("Either file_path or file_data must be provided")
        
        if file_path:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")
            
            filename = os.path.basename(file_path)
            with open(file_path, "rb") as f:
                file_data = f.read()
        else:
            filename = f"permanent_file.{material_type}"
        
        files = {
            "media": (filename, file_data)
        }
        
        endpoint = "/cgi-bin/material/add_material"
        params = {"type": material_type}
        
        return await self.client.post(endpoint, params=params, files=files)
    
    async def get_permanent_material(self, media_id: str) -> Dict[str, Any]:
        endpoint = "/cgi-bin/material/get_material"
        data = {"media_id": media_id}
        return await self.client.post(endpoint, data=data)
    
    async def delete_permanent_material(self, media_id: str) -> Dict[str, Any]:
        endpoint = "/cgi-bin/material/del_material"
        data = {"media_id": media_id}
        return await self.client.post(endpoint, data=data)
    
    async def update_permanent_news(self, media_id: str, index: int, articles: list) -> Dict[str, Any]:
        endpoint = "/cgi-bin/material/update_news"
        data = {
            "media_id": media_id,
            "index": index,
            "articles": articles
        }
        return await self.client.post(endpoint, data=data)
    
    async def get_material_count(self) -> Dict[str, Any]:
        endpoint = "/cgi-bin/material/get_materialcount"
        return await self.client.get(endpoint)
    
    async def get_material_list(
        self, 
        material_type: str, 
        offset: int = 0, 
        count: int = 20
    ) -> Dict[str, Any]:
        endpoint = "/cgi-bin/material/batchget_material"
        data = {
            "type": material_type,
            "offset": offset,
            "count": count
        }
        return await self.client.post(endpoint, data=data)
