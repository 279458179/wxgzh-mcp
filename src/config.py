import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    APP_ID: str = os.getenv("WECHAT_APP_ID", "")
    APP_SECRET: str = os.getenv("WECHAT_APP_SECRET", "")
    TOKEN: str = os.getenv("WECHAT_TOKEN", "")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    TOKEN_CACHE_FILE: str = os.getenv("TOKEN_CACHE_FILE", "./token_cache.json")
    
    BASE_API_URL: str = "https://api.weixin.qq.com"
    TOKEN_URL: str = f"{BASE_API_URL}/cgi-bin/token"
    
    @classmethod
    def validate(cls):
        if not cls.APP_ID or not cls.APP_SECRET:
            raise ValueError("WECHAT_APP_ID and WECHAT_APP_SECRET must be set")


config = Config()
