from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    app_name: str = "Malaysian IPTV"
    app_version: str = "1.0.0"
    debug: bool = True
    host: str = "0.0.0.0"
    port: int = 8000
    
    allowed_origins: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000"
    ]
    
    m3u8_sources: List[str] = [
        "https://raw.githubusercontent.com/MIFNtechnology/siaranMy/main/channels.m3u",
        "./data/example_channels.m3u8"
    ]
    
    epg_refresh_interval: int = 3600
    epg_cache_enabled: bool = True
    
    data_dir: str = "./data"
    favorites_file: str = "./data/favorites.json"
    channels_cache_file: str = "./data/channels_cache.json"
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        
        @classmethod
        def parse_env_var(cls, field_name: str, raw_val: str):
            if field_name in ['allowed_origins', 'm3u8_sources']:
                return [x.strip() for x in raw_val.split(',')]
            return raw_val


settings = Settings()

os.makedirs(settings.data_dir, exist_ok=True)
