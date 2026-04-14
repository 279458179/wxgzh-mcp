import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from src.api.client import WeChatClient
from src.utils.exceptions import AuthenticationError, TokenExpiredError


@pytest.fixture
def mock_client():
    client = WeChatClient(app_id="test_app_id", app_secret="test_app_secret")
    return client


@pytest.mark.asyncio
async def test_get_access_token_success(mock_client):
    with patch.object(mock_client._client, 'get', new_callable=AsyncMock) as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "access_token": "test_token",
            "expires_in": 7200
        }
        mock_get.return_value = mock_response
        
        with patch('src.api.client.save_json_file'):
            token = await mock_client.get_access_token()
            
        assert token == "test_token"
        assert mock_client.access_token == "test_token"
        assert mock_client.expires_in == 7200


@pytest.mark.asyncio
async def test_get_access_token_failure(mock_client):
    with patch.object(mock_client._client, 'get', new_callable=AsyncMock) as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "errcode": 40013,
            "errmsg": "invalid appid"
        }
        mock_get.return_value = mock_response
        
        with pytest.raises(AuthenticationError) as exc_info:
            await mock_client.get_access_token()
        
        assert exc_info.value.errcode == 40013


@pytest.mark.asyncio
async def test_make_request_with_retry_on_token_expired(mock_client):
    mock_client.access_token = "expired_token"
    
    mock_response = MagicMock()
    mock_response.json.return_value = {"data": "success"}
    mock_response.raise_for_status = MagicMock()
    
    with patch.object(mock_client._client, 'get', return_value=mock_response, new_callable=AsyncMock):
        with patch.object(mock_client, 'get_access_token', new_callable=AsyncMock) as mock_refresh:
            mock_refresh.return_value = "new_token"
            
            result = await mock_client.get("/test endpoint")
            
            assert result == {"data": "success"}
            assert mock_refresh.called


def test_get_token_status_with_token(mock_client):
    from datetime import datetime
    mock_client.access_token = "test_token"
    mock_client.expires_in = 7200
    mock_client.refresh_time = datetime.now()
    
    status = mock_client._get_token_status()
    
    assert status["has_token"] is True
    assert status["expires_in"] > 0


def test_get_token_status_without_token(mock_client):
    mock_client.access_token = None
    
    status = mock_client._get_token_status()
    
    assert status["has_token"] is False
    assert status["is_expired"] is True


@pytest.mark.asyncio
async def test_load_token_from_cache(mock_client):
    with patch('src.api.client.load_json_file') as mock_load:
        from datetime import datetime, timedelta
        
        mock_load.return_value = {
            "access_token": "cached_token",
            "expires_in": 7200,
            "refresh_time": (datetime.now() - timedelta(hours=1)).isoformat()
        }
        
        result = mock_client._load_token_from_cache()
        
        assert result is True
        assert mock_client.access_token == "cached_token"
