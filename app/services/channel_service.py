import json
import aiofiles
from typing import List, Optional, Dict
from app.models import Channel
from app.parsers import M3U8Parser
from app.core import settings, get_logger

logger = get_logger(__name__)


class ChannelService:
    def __init__(self):
        self.channels: List[Channel] = []
        self.channels_by_id: Dict[str, Channel] = {}
        self.parser = M3U8Parser()
        self.cache_file = settings.channels_cache_file
    
    async def load_channels(self):
        try:
            await self._load_from_cache()
            if not self.channels:
                await self.refresh_channels()
        except Exception as e:
            logger.error(f"Error loading channels: {e}")
            await self.refresh_channels()
    
    async def refresh_channels(self):
        logger.info("Refreshing channels from M3U8 sources")
        all_channels = []
        
        for source in settings.m3u8_sources:
            logger.info(f"Fetching channels from: {source}")
            channels = await self.parser.fetch_and_parse(source)
            all_channels.extend(channels)
        
        self.channels = all_channels
        self.channels_by_id = {ch.id: ch for ch in all_channels}
        
        await self._save_to_cache()
        logger.info(f"Loaded {len(self.channels)} channels")
    
    async def _load_from_cache(self):
        try:
            async with aiofiles.open(self.cache_file, 'r') as f:
                content = await f.read()
                data = json.loads(content)
                self.channels = [Channel(**ch) for ch in data]
                self.channels_by_id = {ch.id: ch for ch in self.channels}
                logger.info(f"Loaded {len(self.channels)} channels from cache")
        except FileNotFoundError:
            logger.info("No cache file found")
        except Exception as e:
            logger.error(f"Error loading from cache: {e}")
    
    async def _save_to_cache(self):
        try:
            data = [ch.model_dump() for ch in self.channels]
            async with aiofiles.open(self.cache_file, 'w') as f:
                await f.write(json.dumps(data, indent=2, default=str))
            logger.info("Saved channels to cache")
        except Exception as e:
            logger.error(f"Error saving to cache: {e}")
    
    def get_all_channels(self, page: int = 1, page_size: int = 50) -> tuple[List[Channel], int]:
        start = (page - 1) * page_size
        end = start + page_size
        return self.channels[start:end], len(self.channels)
    
    def get_channel_by_id(self, channel_id: str) -> Optional[Channel]:
        return self.channels_by_id.get(channel_id)
    
    def search_channels(self, query: str) -> List[Channel]:
        query_lower = query.lower()
        return [
            ch for ch in self.channels
            if query_lower in ch.name.lower() or
               (ch.group and query_lower in ch.group.lower())
        ]
    
    def get_channels_by_group(self, group: str) -> List[Channel]:
        return [ch for ch in self.channels if ch.group and ch.group.lower() == group.lower()]
    
    def get_all_groups(self) -> List[str]:
        groups = set()
        for ch in self.channels:
            if ch.group:
                groups.add(ch.group)
        return sorted(list(groups))
    
    def get_astro_channels(self) -> List[Channel]:
        return [ch for ch in self.channels if ch.is_astro]
    
    def validate_stream_url(self, url: str) -> bool:
        return url.startswith('http://') or url.startswith('https://')


channel_service = ChannelService()
