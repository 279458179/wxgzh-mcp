import httpx
import logging
from typing import Optional, Dict, Any
from datetime import datetime
from ..config import config
from ..utils.exceptions import (
    WeChatAPIError, 
    AuthenticationError, 
    TokenExpiredError, 
    RateLimitError,
    InvalidParameterError,
    NetworkError
)
from ..utils.helpers import load_json_file, save_json_file

logger = logging.getLogger(__name__)


class WeChatClient:
    def __init__(self, app_id: Optional[str] = None, app_secret: Optional[str] = None):
        self.app_id = app_id or config.APP_ID
        self.app_secret = app_secret or config.APP_SECRET
        self.access_token: Optional[str] = None
        self.expires_in: Optional[int] = None
        self.refresh_time: Optional[datetime] = None
        self._client = httpx.AsyncClient(timeout=30.0)
        
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._client.aclose()
        
    def _load_token_from_cache(self) -> bool:
        try:
            token_data = load_json_file(config.TOKEN_CACHE_FILE)
            if token_data:
                self.access_token = token_data.get("access_token")
                self.expires_in = token_data.get("expires_in")
                self.refresh_time = datetime.fromisoformat(token_data.get("refresh_time"))
                
                from ..utils.helpers import is_token_expired
                if not is_token_expired(self.expires_in, self.refresh_time):
                    logger.info("Loaded access token from cache")
                    return True
                else:
                    logger.info("Cached token has expired")
        except Exception as e:
            logger.warning(f"Failed to load token from cache: {e}")
        return False
    
    def _save_token_to_cache(self) -> None:
        try:
            token_data = {
                "access_token": self.access_token,
                "expires_in": self.expires_in,
                "refresh_time": self.refresh_time.isoformat()
            }
            save_json_file(config.TOKEN_CACHE_FILE, token_data)
            logger.info("Saved access token to cache")
        except Exception as e:
            logger.warning(f"Failed to save token to cache: {e}")
    
    async def get_access_token(self, force_refresh: bool = False) -> str:
        if not force_refresh and self._load_token_from_cache() and self.access_token:
            return self.access_token
        
        url = f"{config.TOKEN_URL}?grant_type=client_credential&appid={self.app_id}&secret={self.app_secret}"
        
        for attempt in range(3):
            try:
                response = await self._client.get(url)
                response.raise_for_status()
                data = response.json()
                
                if "access_token" in data:
                    self.access_token = data["access_token"]
                    self.expires_in = data["expires_in"]
                    self.refresh_time = datetime.now()
                    self._save_token_to_cache()
                    logger.info("Successfully obtained new access token")
                    return self.access_token
                else:
                    errcode = data.get("errcode", -1)
                    errmsg = data.get("errmsg", "Unknown error")
                    raise AuthenticationError(errcode, errmsg)
                    
            except httpx.HTTPError as e:
                logger.warning(f"HTTP error attempt {attempt + 1}: {e}")
                if attempt == 2:
                    raise NetworkError(f"Failed to get access token: {e}")
                
        raise NetworkError("Failed to get access token after 3 attempts")
    
    def _get_token_status(self) -> Dict[str, Any]:
        if self.access_token and self.refresh_time and self.expires_in:
            from ..utils.helpers import is_token_expired
            is_expired = is_token_expired(self.expires_in, self.refresh_time)
            
            remaining_seconds = self.expires_in - int((datetime.now() - self.refresh_time).total_seconds())
            
            return {
                "has_token": True,
                "is_expired": is_expired,
                "expires_in": remaining_seconds if remaining_seconds > 0 else 0,
                "refresh_time": self.refresh_time.isoformat()
            }
        
        return {
            "has_token": False,
            "is_expired": True,
            "expires_in": None,
            "refresh_time": None
        }
    
    async def _make_request(
        self, 
        method: str, 
        endpoint: str, 
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        url = f"{config.BASE_API_URL}{endpoint}"
        
        if "access_token" not in (params or {}):
            token = await self.get_access_token()
            params = params or {}
            params["access_token"] = token
        
        for attempt in range(3):
            try:
                if method.upper() == "GET":
                    response = await self._client.get(url, params=params)
                elif method.upper() == "POST":
                    if files:
                        response = await self._client.post(url, params=params, files=files)
                    else:
                        response = await self._client.post(url, params=params, json=data)
                elif method.upper() == "PUT":
                    response = await self._client.put(url, params=params, json=data)
                elif method.upper() == "DELETE":
                    response = await self._client.request(method, url, params=params)
                else:
                    raise ValueError(f"Unsupported HTTP method: {method}")
                
                response.raise_for_status()
                result = response.json()
                
                if "errcode" in result and result["errcode"] != 0:
                    errcode = result["errcode"]
                    errmsg = result["errmsg"]
                    
                    if errcode == 40001:
                        logger.warning("Access token expired, refreshing...")
                        await self.get_access_token(force_refresh=True)
                        params["access_token"] = self.access_token
                        continue
                    elif errcode == 40013:
                        raise AuthenticationError(errcode, errmsg)
                    elif errcode in [40001, 42001]:
                        raise TokenExpiredError(errcode, errmsg)
                    elif errcode == 45009:
                        raise RateLimitError(errcode, errmsg)
                    elif errcode in [40003, 40004, 40005, 40006, 40007]:
                        raise InvalidParameterError(errcode, errmsg)
                    else:
                        raise WeChatAPIError(errcode, errmsg)
                
                return result
                
            except httpx.HTTPError as e:
                logger.warning(f"HTTP error attempt {attempt + 1}: {e}")
                if attempt == 2:
                    raise NetworkError(f"Request failed: {e}")
                    
        raise NetworkError("Request failed after 3 attempts")
    
    async def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return await self._make_request("GET", endpoint, params=params)
    
    async def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return await self._make_request("POST", endpoint, data=data, params=params)
    
    async def put(self, endpoint: str, data: Optional[Dict[str, Any]] = None, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return await self._make_request("PUT", endpoint, data=data, params=params)
    
    async def delete(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return await self._make_request("DELETE", endpoint, params=params)
