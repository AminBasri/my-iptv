import aiohttp
from lxml import etree
from typing import List, Dict
from datetime import datetime
from dateutil import parser as date_parser
from app.models import EPGProgram
from app.core import get_logger

logger = get_logger(__name__)


class EPGParser:
    def __init__(self):
        self.epg_data: Dict[str, List[EPGProgram]] = {}
    
    def parse_xmltv(self, content: str) -> Dict[str, List[EPGProgram]]:
        try:
            root = etree.fromstring(content.encode('utf-8'))
            programs_by_channel = {}
            
            for programme in root.xpath('//programme'):
                try:
                    channel_id = programme.get('channel')
                    start = programme.get('start')
                    stop = programme.get('stop')
                    
                    if not all([channel_id, start, stop]):
                        continue
                    
                    title_elem = programme.find('title')
                    title = title_elem.text if title_elem is not None and title_elem.text else "Unknown"
                    
                    desc_elem = programme.find('desc')
                    description = desc_elem.text if desc_elem is not None and desc_elem.text else None
                    
                    category_elem = programme.find('category')
                    category = category_elem.text if category_elem is not None and category_elem.text else None
                    
                    icon_elem = programme.find('icon')
                    icon = icon_elem.get('src') if icon_elem is not None else None
                    
                    start_time = self._parse_xmltv_time(start)
                    end_time = self._parse_xmltv_time(stop)
                    
                    if start_time and end_time:
                        program = EPGProgram(
                            channel_id=channel_id,
                            title=title,
                            description=description,
                            start_time=start_time,
                            end_time=end_time,
                            category=category,
                            icon=icon
                        )
                        
                        if channel_id not in programs_by_channel:
                            programs_by_channel[channel_id] = []
                        programs_by_channel[channel_id].append(program)
                
                except Exception as e:
                    logger.warning(f"Error parsing programme element: {e}")
                    continue
            
            logger.info(f"Parsed EPG data for {len(programs_by_channel)} channels")
            return programs_by_channel
            
        except Exception as e:
            logger.error(f"Error parsing XMLTV content: {e}")
            return {}
    
    def _parse_xmltv_time(self, time_str: str) -> datetime:
        try:
            if '+' in time_str or '-' in time_str[-5:]:
                return date_parser.parse(time_str)
            else:
                base_time = time_str[:14]
                return datetime.strptime(base_time, '%Y%m%d%H%M%S')
        except Exception as e:
            logger.warning(f"Error parsing time {time_str}: {e}")
            return None
    
    async def fetch_and_parse(self, url: str) -> Dict[str, List[EPGProgram]]:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=60)) as response:
                    if response.status == 200:
                        content = await response.text()
                        return self.parse_xmltv(content)
                    else:
                        logger.error(f"Failed to fetch EPG from {url}: HTTP {response.status}")
                        return {}
        except Exception as e:
            logger.error(f"Error fetching EPG from {url}: {e}")
            return {}
    
    def get_current_program(self, channel_id: str, now: datetime = None) -> EPGProgram:
        if now is None:
            now = datetime.utcnow()
        
        programs = self.epg_data.get(channel_id, [])
        for program in programs:
            if program.start_time <= now <= program.end_time:
                return program
        return None
    
    def get_upcoming_programs(self, channel_id: str, limit: int = 5, now: datetime = None) -> List[EPGProgram]:
        if now is None:
            now = datetime.utcnow()
        
        programs = self.epg_data.get(channel_id, [])
        upcoming = [p for p in programs if p.start_time > now]
        upcoming.sort(key=lambda x: x.start_time)
        return upcoming[:limit]
    
    def update_epg_data(self, epg_data: Dict[str, List[EPGProgram]]):
        self.epg_data = epg_data
        logger.info(f"Updated EPG data with {len(epg_data)} channels")
