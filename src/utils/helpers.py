import json
import logging
from typing import Any, Dict
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


def format_timestamp(timestamp: int) -> str:
    return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")


def is_token_expired(expires_in: int, refresh_time: datetime) -> bool:
    expiry_time = refresh_time + timedelta(seconds=expires_in)
    return datetime.now() >= expiry_time


def load_json_file(file_path: str) -> Dict[str, Any]:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        logger.warning(f"File {file_path} not found")
        return {}
    except json.JSONDecodeError:
        logger.error(f"Invalid JSON in file {file_path}")
        return {}


def save_json_file(file_path: str, data: Dict[str, Any]) -> None:
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def validate_media_type(media_type: str) -> bool:
    valid_types = ["image", "voice", "video", "thumb"]
    return media_type in valid_types


def build_file_extension(media_type: str, filename: str) -> str:
    extensions = {
        "image": [".jpg", ".jpeg", ".png", ".gif"],
        "voice": [".mp3", ".wma", ".wav", ".amr"],
        "video": [".mp4"],
        "thumb": [".jpg", ".jpeg", ".png", ".gif"]
    }
    
    for ext in extensions.get(media_type, []):
        if filename.lower().endswith(ext):
            return ext
    
    return extensions.get(media_type, [".jpg"])[0]
