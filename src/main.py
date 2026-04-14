import logging
from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Query, Path
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List
from contextlib import asynccontextmanager

from .config import config
from .api.client import WeChatClient
from .api.auth import AuthManager
from .api.materials import MaterialsManager
from .api.articles import ArticlesManager
from .api.messages import MessagesManager
from .api.users import UsersManager
from .api.menus import MenusManager
from .api.analytics import AnalyticsManager
from .utils.exceptions import WeChatAPIError, NetworkError

logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


client: Optional[WeChatClient] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global client
    try:
        config.validate()
        client = WeChatClient()
        logger.info("WeChat client initialized successfully")
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        raise
    yield
    if client:
        await client._client.aclose()


app = FastAPI(
    title="WXGZH-MCP API",
    description="微信公众号管理API",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "WXGZH-MCP API", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.get("/api/auth/token")
async def get_token_status():
    auth_manager = AuthManager(client)
    return await auth_manager.get_token_status()


@app.post("/api/auth/token/refresh")
async def refresh_token():
    auth_manager = AuthManager(client)
    return await auth_manager.refresh_token()


@app.post("/api/materials/upload")
async def upload_material(
    type: str = Form(...),
    file: UploadFile = File(...)
):
    try:
        materials_manager = MaterialsManager(client)
        content = await file.read()
        result = await materials_manager.upload_temporary_material(
            file_data=content,
            material_type=type
        )
        return result
    except (WeChatAPIError, NetworkError) as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/materials/permanent")
async def add_permanent_material(
    type: str = Form(...),
    file: Optional[UploadFile] = File(None)
):
    try:
        materials_manager = MaterialsManager(client)
        content = None
        if file:
            content = await file.read()
        
        result = await materials_manager.add_permanent_material(
            material_type=type,
            file_data=content
        )
        return result
    except (WeChatAPIError, NetworkError) as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/materials")
async def get_materials(
    type: str = Query(...),
    offset: int = Query(0),
    count: int = Query(20)
):
    try:
        materials_manager = MaterialsManager(client)
        result = await materials_manager.get_material_list(type, offset, count)
        return result
    except (WeChatAPIError, NetworkError) as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/materials/{media_id}")
async def get_material(media_id: str = Path(...)):
    try:
        materials_manager = MaterialsManager(client)
        result = await materials_manager.get_permanent_material(media_id)
        return result
    except (WeChatAPIError, NetworkError) as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/api/materials/{media_id}")
async def delete_material(media_id: str = Path(...)):
    try:
        materials_manager = MaterialsManager(client)
        result = await materials_manager.delete_permanent_material(media_id)
        return result
    except (WeChatAPIError, NetworkError) as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/materials/count")
async def get_material_count():
    try:
        materials_manager = MaterialsManager(client)
        result = await materials_manager.get_material_count()
        return result
    except (WeChatAPIError, NetworkError) as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/articles")
async def create_article(articles: List[dict]):
    try:
        articles_manager = ArticlesManager(client)
        result = await articles_manager.create_article(articles)
        return result
    except (WeChatAPIError, NetworkError) as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/articles")
async def get_articles(
    offset: int = Query(0),
    count: int = Query(20)
):
    try:
        articles_manager = ArticlesManager(client)
        result = await articles_manager.get_article_list(offset, count)
        return result
    except (WeChatAPIError, NetworkError) as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/articles/{media_id}")
async def get_article(media_id: str = Path(...)):
    try:
        articles_manager = ArticlesManager(client)
        result = await articles_manager.get_article(media_id)
        return result
    except (WeChatAPIError, NetworkError) as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.put("/api/articles/{media_id}")
async def update_article(
    media_id: str = Path(...),
    index: int = Query(0),
    articles: dict = ...
):
    try:
        articles_manager = ArticlesManager(client)
        result = await articles_manager.update_article(media_id, index, articles)
        return result
    except (WeChatAPIError, NetworkError) as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/api/articles/{media_id}")
async def delete_article(media_id: str = Path(...)):
    try:
        articles_manager = ArticlesManager(client)
        result = await articles_manager.delete_article(media_id)
        return result
    except (WeChatAPIError, NetworkError) as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/articles/{media_id}/preview")
async def preview_article(
    media_id: str = Path(...),
    touser: Optional[str] = Query(None),
    towxname: Optional[str] = Query(None)
):
    try:
        articles_manager = ArticlesManager(client)
        result = await articles_manager.preview_article(media_id, touser, towxname)
        return result
    except (WeChatAPIError, NetworkError) as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/messages/send")
async def send_message(
    touser: str = Query(...),
    msgtype: str = Query("text"),
    content: Optional[str] = Query(None),
    media_id: Optional[str] = Query(None),
    title: Optional[str] = Query(None),
    description: Optional[str] = Query(None),
    url: Optional[str] = Query(None),
    appid: Optional[str] = Query(None),
    pagepath: Optional[str] = Query(None)
):
    try:
        messages_manager = MessagesManager(client)
        
        if msgtype == "text":
            result = await messages_manager.send_text_message(touser, content)
        elif msgtype == "image":
            result = await messages_manager.send_image_message(touser, media_id)
        elif msgtype == "voice":
            result = await messages_manager.send_voice_message(touser, media_id)
        elif msgtype == "video":
            result = await messages_manager.send_video_message(touser, media_id, title, description)
        elif msgtype == "mpnews":
            result = await messages_manager.send_article_message(touser, media_id)
        elif msgtype == "link":
            result = await messages_manager.send_link_message(touser, title, description, url)
        elif msgtype == "miniprogrampage":
            result = await messages_manager.send_miniprogram_message(
                touser, appid, title, pagepath, media_id
            )
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported msgtype: {msgtype}")
        
        return result
    except (WeChatAPIError, NetworkError) as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/messages/broadcast")
async def broadcast_message(
    msgtype: str = Query(...),
    is_to_all: bool = Query(True),
    tag_id: Optional[int] = Query(None),
    openid_list: Optional[List[str]] = Query(None),
    content: Optional[str] = Query(None),
    media_id: Optional[str] = Query(None)
):
    try:
        messages_manager = MessagesManager(client)
        
        if is_to_all:
            filter_data = {"is_to_all": True}
        elif tag_id:
            filter_data = {"is_to_all": False, "tag_id": tag_id}
        elif openid_list:
            filter_data = {"is_to_all": False, "openid_list": openid_list}
        else:
            raise HTTPException(status_code=400, detail="Must specify tag or user list")
        
        result = await messages_manager.broadcast_message(
            msgtype=msgtype,
            filter=filter_data,
            content=content,
            media_id=media_id
        )
        return result
    except (WeChatAPIError, NetworkError) as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/messages/template")
async def send_template_message(
    touser: str = Query(...),
    template_id: str = Query(...),
    url: Optional[str] = Query(None),
    data: dict = Query(...),
    appid: Optional[str] = Query(None),
    pagepath: Optional[str] = Query(None)
):
    try:
        messages_manager = MessagesManager(client)
        
        miniprogram = None
        if appid and pagepath:
            miniprogram = {"appid": appid, "pagepath": pagepath}
        
        result = await messages_manager.send_template_message(
            touser=touser,
            template_id=template_id,
            data=data,
            url=url,
            miniprogram=miniprogram
        )
        return result
    except (WeChatAPIError, NetworkError) as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/users")
async def get_users(next_openid: str = Query("")):
    try:
        users_manager = UsersManager(client)
        result = await users_manager.get_user_list(next_openid)
        return result
    except (WeChatAPIError, NetworkError) as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/users/{openid}")
async def get_user_info(
    openid: str = Path(...),
    lang: str = Query("zh_CN")
):
    try:
        users_manager = UsersManager(client)
        result = await users_manager.get_user_info(openid, lang)
        return result
    except (WeChatAPIError, NetworkError) as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.put("/api/users/{openid}")
async def update_user_remark(
    openid: str = Path(...),
    remark: str = Query(...)
):
    try:
        users_manager = UsersManager(client)
        result = await users_manager.update_user_remark(openid, remark)
        return result
    except (WeChatAPIError, NetworkError) as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/users/tags")
async def get_user_tags():
    try:
        users_manager = UsersManager(client)
        result = await users_manager.get_user_tags()
        return result
    except (WeChatAPIError, NetworkError) as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/users/tags")
async def create_tag(name: str = Query(...)):
    try:
        users_manager = UsersManager(client)
        result = await users_manager.create_tag(name)
        return result
    except (WeChatAPIError, NetworkError) as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/api/users/tags/{tag_id}")
async def delete_tag(tag_id: int = Path(...)):
    try:
        users_manager = UsersManager(client)
        result = await users_manager.delete_tag(tag_id)
        return result
    except (WeChatAPIError, NetworkError) as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/users/tags/{tag_id}")
async def batch_tag_users(
    tag_id: int = Path(...),
    openid_list: List[str] = Query(...)
):
    try:
        users_manager = UsersManager(client)
        result = await users_manager.batch_tag_users(tag_id, openid_list)
        return result
    except (WeChatAPIError, NetworkError) as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/api/users/tags/{tag_id}")
async def batch_untag_users(
    tag_id: int = Path(...),
    openid_list: List[str] = Query(...)
):
    try:
        users_manager = UsersManager(client)
        result = await users_manager.batch_untag_users(tag_id, openid_list)
        return result
    except (WeChatAPIError, NetworkError) as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/menus")
async def get_menus():
    try:
        menus_manager = MenusManager(client)
        result = await menus_manager.get_menu()
        return result
    except (WeChatAPIError, NetworkError) as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/menus")
async def create_menu(buttons: List[dict]):
    try:
        menus_manager = MenusManager(client)
        result = await menus_manager.create_menu(buttons)
        return result
    except (WeChatAPIError, NetworkError) as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/api/menus")
async def delete_menu():
    try:
        menus_manager = MenusManager(client)
        result = await menus_manager.delete_menu()
        return result
    except (WeChatAPIError, NetworkError) as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/analytics/users")
async def get_user_analytics(
    begin_date: str = Query(...),
    end_date: str = Query(...),
    type: str = Query("summary")
):
    try:
        analytics_manager = AnalyticsManager(client)
        
        if type == "summary":
            result = await analytics_manager.get_user_summary(begin_date, end_date)
        else:
            result = await analytics_manager.get_user_cumulate(begin_date, end_date)
        
        return result
    except (WeChatAPIError, NetworkError) as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/analytics/articles")
async def get_article_analytics(
    begin_date: str = Query(...),
    end_date: str = Query(...),
    type: str = Query("summary")
):
    try:
        analytics_manager = AnalyticsManager(client)
        
        if type == "summary":
            result = await analytics_manager.get_article_summary(begin_date, end_date)
        elif type == "total":
            result = await analytics_manager.get_article_total(begin_date, end_date)
        elif type == "read":
            result = await analytics_manager.get_user_read_summary(begin_date, end_date)
        else:
            result = await analytics_manager.get_article_share_summary(begin_date, end_date)
        
        return result
    except (WeChatAPIError, NetworkError) as e:
        raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=config.API_PORT)
