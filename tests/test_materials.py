import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from src.api.materials import MaterialsManager
from src.api.client import WeChatClient


@pytest.fixture
def materials_manager(mock_client):
    return MaterialsManager(mock_client)


@pytest.fixture
def mock_client():
    return MagicMock(spec=WeChatClient)


@pytest.mark.asyncio
async def test_upload_temporary_material_with_file_path(materials_manager, mock_client):
    with patch('os.path.exists', return_value=True):
        with patch('builtins.open', MagicMock()):
            mock_client.post = AsyncMock(return_value={
                "media_id": "test_media_id",
                "url": "http://example.com/image.jpg"
            })
            
            result = await materials_manager.upload_temporary_material(
                file_path="/path/to/image.jpg",
                material_type="image"
            )
            
            assert "media_id" in result
            mock_client.post.assert_called_once()


@pytest.mark.asyncio
async def test_upload_temporary_material_with_file_data(materials_manager, mock_client):
    mock_client.post = AsyncMock(return_value={
        "media_id": "test_media_id"
    })
    
    result = await materials_manager.upload_temporary_material(
        file_data=b"fake image data",
        material_type="image"
    )
    
    assert "media_id" in result
    mock_client.post.assert_called_once()


@pytest.mark.asyncio
async def test_upload_temporary_material_without_file():
    mock_client = MagicMock(spec=WeChatClient)
    materials_manager = MaterialsManager(mock_client)
    
    with pytest.raises(ValueError):
        await materials_manager.upload_temporary_material(
            material_type="image"
        )


@pytest.mark.asyncio
async def test_add_permanent_material_news(materials_manager, mock_client):
    mock_client.post = AsyncMock(return_value={
        "media_id": "test_media_id"
    })
    
    articles = [
        {
            "title": "Test Article",
            "thumb_media_id": "thumb123",
            "author": "Test Author",
            "content": "<p>Test content</p>"
        }
    ]
    
    result = await materials_manager.add_permanent_material(
        material_type="news",
        articles=articles
    )
    
    assert "media_id" in result
    mock_client.post.assert_called_once()


@pytest.mark.asyncio
async def test_get_permanent_material(materials_manager, mock_client):
    mock_client.post = AsyncMock(return_value={
        "news_item": [
            {
                "title": "Test Article",
                "content": "<p>Test content</p>"
            }
        ]
    })
    
    result = await materials_manager.get_permanent_material("test_media_id")
    
    assert "news_item" in result
    mock_client.post.assert_called_once()


@pytest.mark.asyncio
async def test_delete_permanent_material(materials_manager, mock_client):
    mock_client.post = AsyncMock(return_value={
        "errcode": 0,
        "errmsg": "deleted"
    })
    
    result = await materials_manager.delete_permanent_material("test_media_id")
    
    assert result["errcode"] == 0
    mock_client.post.assert_called_once()


@pytest.mark.asyncio
async def test_get_material_count(materials_manager, mock_client):
    mock_client.get = AsyncMock(return_value={
        "total_count": 100,
        "image_count": 50,
        "voice_count": 20,
        "video_count": 15,
        "thumb_count": 15
    })
    
    result = await materials_manager.get_material_count()
    
    assert result["total_count"] == 100
    mock_client.get.assert_called_once()


@pytest.mark.asyncio
async def test_get_material_list(materials_manager, mock_client):
    mock_client.post = AsyncMock(return_value={
        "total_count": 50,
        "item_count": 2,
        "item": [
            {"media_id": "media1", "name": "image1.jpg"},
            {"media_id": "media2", "name": "image2.jpg"}
        ]
    })
    
    result = await materials_manager.get_material_list("image", 0, 20)
    
    assert result["total_count"] == 50
    assert len(result["item"]) == 2
    mock_client.post.assert_called_once()
