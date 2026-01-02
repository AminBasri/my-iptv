import asyncio
from typing import List, Optional, Dict
from datetime import datetime
from app.models import EPGProgram, EPGChannelPrograms
from app.parsers import EPGParser
from app.core import settings, get_logger

logger = get_logger(__name__)


class EPGService:
    def __init__(self):
        self.parser = EPGParser()
        self.refresh_task: Optional[asyncio.Task] = None
        self.epg_urls: List[str] = []
    
    def add_epg_url(self, url: str):
        if url not in self.epg_urls:
            self.epg_urls.append(url)
            logger.info(f"Added EPG URL: {url}")
    
    async def start_auto_refresh(self):
        if settings.epg_cache_enabled:
            self.refresh_task = asyncio.create_task(self._auto_refresh_loop())
            logger.info("Started EPG auto-refresh")
    
    async def stop_auto_refresh(self):
        if self.refresh_task:
            self.refresh_task.cancel()
            try:
                await self.refresh_task
            except asyncio.CancelledError:
                pass
            logger.info("Stopped EPG auto-refresh")
    
    async def _auto_refresh_loop(self):
        while True:
            try:
                await self.refresh_epg()
                await asyncio.sleep(settings.epg_refresh_interval)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in EPG auto-refresh: {e}")
                await asyncio.sleep(60)
    
    async def refresh_epg(self):
        logger.info("Refreshing EPG data")
        all_epg_data = {}
        
        for url in self.epg_urls:
            try:
                epg_data = await self.parser.fetch_and_parse(url)
                all_epg_data.update(epg_data)
            except Exception as e:
                logger.error(f"Error fetching EPG from {url}: {e}")
        
        self.parser.update_epg_data(all_epg_data)
        logger.info(f"Refreshed EPG data for {len(all_epg_data)} channels")
    
    def get_channel_programs(self, channel_id: str, channel_name: str = None) -> EPGChannelPrograms:
        now = datetime.utcnow()
        current = self.parser.get_current_program(channel_id, now)
        upcoming = self.parser.get_upcoming_programs(channel_id, limit=10, now=now)
        
        return EPGChannelPrograms(
            channel_id=channel_id,
            channel_name=channel_name or channel_id,
            current_program=current,
            upcoming_programs=upcoming
        )
    
    def get_all_programs(self, channel_id: Optional[str] = None) -> List[EPGProgram]:
        if channel_id:
            return self.parser.epg_data.get(channel_id, [])
        
        all_programs = []
        for programs in self.parser.epg_data.values():
            all_programs.extend(programs)
        return all_programs
    
    def search_programs(self, query: str) -> List[EPGProgram]:
        query_lower = query.lower()
        all_programs = self.get_all_programs()
        return [
            p for p in all_programs
            if query_lower in p.title.lower() or
               (p.description and query_lower in p.description.lower())
        ]


epg_service = EPGService()
