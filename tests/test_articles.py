import pytest
from unittest.mock import AsyncMock, MagicMock
from src.api.articles import ArticlesManager
from src.api.client import WeChatClient


@pytest.fixture
def articles_manager(mock_client):
    return ArticlesManager(mock_client)


@pytest.fixture
def mock_client():
    return MagicMock(spec=WeChatClient)


@pytest.mark.asyncio
async def test_create_article(articles_manager, mock_client):
    mock_client.post = AsyncMock(return_value={
        "media_id": "test_media_id"
    })
    
    articles = [
        {
            "title": "Test Article",
            "thumb_media_id": "thumb123",
            "author": "Test Author",
            "content": "<p>Test content</p>",
            "digest": "Test digest"
        }
    ]
    
    result = await articles_manager.create_article(articles)
    
    assert "media_id" in result
    mock_client.post.assert_called_once()


@pytest.mark.asyncio
async def test_get_article(articles_manager, mock_client):
    mock_client.post = AsyncMock(return_value={
        "news_item": [
            {
                "title": "Test Article",
                "author": "Test Author",
                "content": "<p>Test content</p>"
            }
        ]
    })
    
    result = await articles_manager.get_article("test_media_id")
    
    assert "news_item" in result
    assert len(result["news_item"]) == 1
    mock_client.post.assert_called_once()


@pytest.mark.asyncio
async def test_update_article(articles_manager, mock_client):
    mock_client.post = AsyncMock(return_value={
        "errcode": 0,
        "errmsg": "updated"
    })
    
    articles = {
        "title": "Updated Article",
        "thumb_media_id": "thumb123",
        "author": "Test Author",
        "content": "<p>Updated content</p>"
    }
    
    result = await articles_manager.update_article("test_media_id", 0, articles)
    
    assert result["errcode"] == 0
    mock_client.post.assert_called_once()


@pytest.mark.asyncio
async def test_delete_article(articles_manager, mock_client):
    mock_client.post = AsyncMock(return_value={
        "errcode": 0,
        "errmsg": "deleted"
    })
    
    result = await articles_manager.delete_article("test_media_id")
    
    assert result["errcode"] == 0
    mock_client.post.assert_called_once()


@pytest.mark.asyncio
async def test_preview_article_with_touser(articles_manager, mock_client):
    mock_client.post = AsyncMock(return_value={
        "errcode": 0,
        "errmsg": "preview sent"
    })
    
    result = await articles_manager.preview_article(
        media_id="test_media_id",
        touser="test_openid"
    )
    
    assert result["errcode"] == 0
    mock_client.post.assert_called_once()


@pytest.mark.asyncio
async def test_preview_article_with_towxname(articles_manager, mock_client):
    mock_client.post = AsyncMock(return_value={
        "errcode": 0,
        "errmsg": "preview sent"
    })
    
    result = await articles_manager.preview_article(
        media_id="test_media_id",
        towxname="test_wxname"
    )
    
    assert result["errcode"] == 0
    mock_client.post.assert_called_once()


@pytest.mark.asyncio
async def test_preview_article_without_user():
    mock_client = MagicMock(spec=WeChatClient)
    articles_manager = ArticlesManager(mock_client)
    
    with pytest.raises(ValueError):
        await articles_manager.preview_article(media_id="test_media_id")


@pytest.mark.asyncio
async def test_get_article_list(articles_manager, mock_client):
    mock_client.post = AsyncMock(return_value={
        "total_count": 10,
        "item_count": 2,
        "item": [
            {"media_id": "media1"},
            {"media_id": "media2"}
        ]
    })
    
    result = await articles_manager.get_article_list(0, 20)
    
    assert result["total_count"] == 10
    assert result["item_count"] == 2
    mock_client.post.assert_called_once()
