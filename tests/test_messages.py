import pytest
from unittest.mock import AsyncMock, MagicMock
from src.api.messages import MessagesManager
from src.api.client import WeChatClient


@pytest.fixture
def messages_manager(mock_client):
    return MessagesManager(mock_client)


@pytest.fixture
def mock_client():
    return MagicMock(spec=WeChatClient)


@pytest.mark.asyncio
async def test_send_text_message(messages_manager, mock_client):
    mock_client.post = AsyncMock(return_value={
        "errcode": 0,
        "errmsg": "ok"
    })
    
    result = await messages_manager.send_text_message(
        touser="test_openid",
        content="Hello, World!"
    )
    
    assert result["errcode"] == 0
    mock_client.post.assert_called_once()


@pytest.mark.asyncio
async def test_send_image_message(messages_manager, mock_client):
    mock_client.post = AsyncMock(return_value={
        "errcode": 0,
        "errmsg": "ok"
    })
    
    result = await messages_manager.send_image_message(
        touser="test_openid",
        media_id="image_media_id"
    )
    
    assert result["errcode"] == 0
    mock_client.post.assert_called_once()


@pytest.mark.asyncio
async def test_send_video_message(messages_manager, mock_client):
    mock_client.post = AsyncMock(return_value={
        "errcode": 0,
        "errmsg": "ok"
    })
    
    result = await messages_manager.send_video_message(
        touser="test_openid",
        media_id="video_media_id",
        title="Test Video",
        description="Test Description"
    )
    
    assert result["errcode"] == 0
    mock_client.post.assert_called_once()


@pytest.mark.asyncio
async def test_send_article_message(messages_manager, mock_client):
    mock_client.post = AsyncMock(return_value={
        "errcode": 0,
        "errmsg": "ok"
    })
    
    result = await messages_manager.send_article_message(
        touser="test_openid",
        media_id="article_media_id"
    )
    
    assert result["errcode"] == 0
    mock_client.post.assert_called_once()


@pytest.mark.asyncio
async def test_send_link_message(messages_manager, mock_client):
    mock_client.post = AsyncMock(return_value={
        "errcode": 0,
        "errmsg": "ok"
    })
    
    result = await messages_manager.send_link_message(
        touser="test_openid",
        title="Test Link",
        description="Link description",
        url="https://example.com"
    )
    
    assert result["errcode"] == 0
    mock_client.post.assert_called_once()


@pytest.mark.asyncio
async def test_send_miniprogram_message(messages_manager, mock_client):
    mock_client.post = AsyncMock(return_value={
        "errcode": 0,
        "errmsg": "ok"
    })
    
    result = await messages_manager.send_miniprogram_message(
        touser="test_openid",
        appid="wx123456789",
        title="Mini Program",
        pagepath="pages/index",
        thumb_media_id="thumb123"
    )
    
    assert result["errcode"] == 0
    mock_client.post.assert_called_once()


@pytest.mark.asyncio
async def test_broadcast_message_to_all(messages_manager, mock_client):
    mock_client.post = AsyncMock(return_value={
        "errcode": 0,
        "errmsg": "ok",
        "msg_id": 1234567890,
        "msg_data_id": 1234567890
    })
    
    result = await messages_manager.broadcast_message(
        msgtype="text",
        filter={"is_to_all": True},
        content="Broadcast message"
    )
    
    assert "msg_id" in result
    mock_client.post.assert_called_once()


@pytest.mark.asyncio
async def test_broadcast_message_to_tag(messages_manager, mock_client):
    mock_client.post = AsyncMock(return_value={
        "errcode": 0,
        "errmsg": "ok",
        "msg_id": 1234567890
    })
    
    result = await messages_manager.broadcast_message(
        msgtype="mpnews",
        filter={"is_to_all": False, "tag_id": 100},
        media_id="article_media_id"
    )
    
    assert "msg_id" in result
    mock_client.post.assert_called_once()


@pytest.mark.asyncio
async def test_send_template_message(messages_manager, mock_client):
    mock_client.post = AsyncMock(return_value={
        "errcode": 0,
        "errmsg": "ok",
        "msgid": 1234567890
    })
    
    data = {
        "first": {"value": "Hello"},
        "keyword1": {"value": "Test"},
        "remark": {"value": "End"}
    }
    
    result = await messages_manager.send_template_message(
        touser="test_openid",
        template_id="template_id_123",
        data=data,
        url="https://example.com"
    )
    
    assert "msgid" in result
    mock_client.post.assert_called_once()


@pytest.mark.asyncio
async def test_send_template_message_with_miniprogram(messages_manager, mock_client):
    mock_client.post = AsyncMock(return_value={
        "errcode": 0,
        "errmsg": "ok",
        "msgid": 1234567890
    })
    
    data = {
        "first": {"value": "Hello"}
    }
    
    miniprogram = {
        "appid": "wx123456789",
        "pagepath": "pages/index"
    }
    
    result = await messages_manager.send_template_message(
        touser="test_openid",
        template_id="template_id_123",
        data=data,
        miniprogram=miniprogram
    )
    
    assert "msgid" in result
    mock_client.post.assert_called_once()
