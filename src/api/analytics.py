from typing import Dict, Any, Optional
from .client import WeChatClient


class AnalyticsManager:
    def __init__(self, client: WeChatClient):
        self.client = client
    
    async def get_user_summary(
        self, 
        begin_date: str, 
        end_date: str
    ) -> Dict[str, Any]:
        endpoint = "/datacube/getusersummary"
        data = {
            "begin_date": begin_date,
            "end_date": end_date
        }
        return await self.client.post(endpoint, data=data)
    
    async def get_user_cumulate(
        self, 
        begin_date: str, 
        end_date: str
    ) -> Dict[str, Any]:
        endpoint = "/datacube/getusercumulate"
        data = {
            "begin_date": begin_date,
            "end_date": end_date
        }
        return await self.client.post(endpoint, data=data)
    
    async def get_article_summary(
        self, 
        begin_date: str, 
        end_date: str
    ) -> Dict[str, Any]:
        endpoint = "/datacube/getarticlesummary"
        data = {
            "begin_date": begin_date,
            "end_date": end_date
        }
        return await self.client.post(endpoint, data=data)
    
    async def get_article_total(
        self, 
        begin_date: str, 
        end_date: str
    ) -> Dict[str, Any]:
        endpoint = "/datacube/getarticletotal"
        data = {
            "begin_date": begin_date,
            "end_date": end_date
        }
        return await self.client.post(endpoint, data=data)
    
    async def get_user_read_summary(
        self, 
        begin_date: str, 
        end_date: str
    ) -> Dict[str, Any]:
        endpoint = "/datacube/getuserread"
        data = {
            "begin_date": begin_date,
            "end_date": end_date
        }
        return await self.client.post(endpoint, data=data)
    
    async def get_user_read_hourly(
        self, 
        begin_date: str, 
        end_date: str
    ) -> Dict[str, Any]:
        endpoint = "/datacube/getuserreadhour"
        data = {
            "begin_date": begin_date,
            "end_date": end_date
        }
        return await self.client.post(endpoint, data=data)
    
    async def get_article_share_summary(
        self, 
        begin_date: str, 
        end_date: str
    ) -> Dict[str, Any]:
        endpoint = "/datacube/getarticleshare"
        data = {
            "begin_date": begin_date,
            "end_date": end_date
        }
        return await self.client.post(endpoint, data=data)
    
    async def get_article_share_hourly(
        self, 
        begin_date: str, 
        end_date: str
    ) -> Dict[str, Any]:
        endpoint = "/datacube/getarticlesharehour"
        data = {
            "begin_date": begin_date,
            "end_date": end_date
        }
        return await self.client.post(endpoint, data=data)
    
    async def get_upstream_msg_summary(
        self, 
        begin_date: str, 
        end_date: str
    ) -> Dict[str, Any]:
        endpoint = "/datacube/getupstreammsg"
        data = {
            "begin_date": begin_date,
            "end_date": end_date
        }
        return await self.client.post(endpoint, data=data)
    
    async def get_upstream_msg_hourly(
        self, 
        begin_date: str, 
        end_date: str
    ) -> Dict[str, Any]:
        endpoint = "/datacube/getupstreammsghour"
        data = {
            "begin_date": begin_date,
            "end_date": end_date
        }
        return await self.client.post(endpoint, data=data)
    
    async def get_upstream_msg_week_summary(
        self, 
        begin_date: str, 
        end_date: str
    ) -> Dict[str, Any]:
        endpoint = "/datacube/getupstreammsgweek"
        data = {
            "begin_date": begin_date,
            "end_date": end_date
        }
        return await self.client.post(endpoint, data=data)
    
    async def get_upstream_msg_month_summary(
        self, 
        begin_date: str, 
        end_date: str
    ) -> Dict[str, Any]:
        endpoint = "/datacube/getupstreammsgmonth"
        data = {
            "begin_date": begin_date,
            "end_date": end_date
        }
        return await self.client.post(endpoint, data=data)
    
    async def get_interface_summary(
        self, 
        begin_date: str, 
        end_date: str
    ) -> Dict[str, Any]:
        endpoint = "/datacube/getinterfacesummary"
        data = {
            "begin_date": begin_date,
            "end_date": end_date
        }
        return await self.client.post(endpoint, data=data)
    
    async def get_interface_summary_hourly(
        self, 
        begin_date: str, 
        end_date: str
    ) -> Dict[str, Any]:
        endpoint = "/datacube/getinterfacesummaryhour"
        data = {
            "begin_date": begin_date,
            "end_date": end_date
        }
        return await self.client.post(endpoint, data=data)
