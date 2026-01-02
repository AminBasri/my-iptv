import re
import aiohttp
import hashlib
from typing import List, Dict, Optional
from app.models import Channel
from app.core import get_logger

logger = get_logger(__name__)


class M3U8Parser:
    def __init__(self):
        self.astro_keywords = ['astro', 'njoi', 'mytv']
        
    def _generate_channel_id(self, name: str, url: str) -> str:
        unique_string = f"{name}_{url}"
        return hashlib.md5(unique_string.encode()).hexdigest()[:12]
    
    def _is_astro_channel(self, name: str, group: str = "") -> bool:
        text = f"{name} {group}".lower()
        return any(keyword in text for keyword in self.astro_keywords)
    
    def _parse_extinf_line(self, line: str) -> Dict[str, Optional[str]]:
        metadata = {}
        
        tvg_id_match = re.search(r'tvg-id="([^"]*)"', line)
        metadata['tvg_id'] = tvg_id_match.group(1) if tvg_id_match else None
        
        tvg_name_match = re.search(r'tvg-name="([^"]*)"', line)
        metadata['tvg_name'] = tvg_name_match.group(1) if tvg_name_match else None
        
        tvg_logo_match = re.search(r'tvg-logo="([^"]*)"', line)
        metadata['logo'] = tvg_logo_match.group(1) if tvg_logo_match else None
        
        group_title_match = re.search(r'group-title="([^"]*)"', line)
        metadata['group'] = group_title_match.group(1) if group_title_match else None
        
        radio_match = re.search(r'radio="([^"]*)"', line)
        metadata['radio'] = radio_match.group(1).lower() == "true" if radio_match else False
        
        language_match = re.search(r'tvg-language="([^"]*)"', line)
        if not language_match:
            language_match = re.search(r'language="([^"]*)"', line)
        metadata['language'] = language_match.group(1) if language_match else None
        
        country_match = re.search(r'tvg-country="([^"]*)"', line)
        metadata['country'] = country_match.group(1) if country_match else "MY"
        
        name_match = re.search(r',(.+)$', line)
        metadata['name'] = name_match.group(1).strip() if name_match else "Unknown"
        
        return metadata
    
    def parse_m3u8_content(self, content: str) -> List[Channel]:
        channels = []
        lines = content.strip().split('\n')
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            if line.startswith('#EXTINF:'):
                metadata = self._parse_extinf_line(line)
                
                if i + 1 < len(lines):
                    url_line = lines[i + 1].strip()
                    
                    if url_line and not url_line.startswith('#'):
                        channel_id = self._generate_channel_id(metadata['name'], url_line)
                        
                        is_astro = self._is_astro_channel(
                            metadata['name'],
                            metadata.get('group', '')
                        )
                        
                        channel = Channel(
                            id=channel_id,
                            name=metadata['name'],
                            logo=metadata.get('logo'),
                            group=metadata.get('group'),
                            url=url_line,
                            epg_id=metadata.get('tvg_id'),
                            language=metadata.get('language'),
                            country=metadata.get('country', 'MY'),
                            tvg_id=metadata.get('tvg_id'),
                            tvg_name=metadata.get('tvg_name'),
                            radio=metadata.get('radio', False),
                            is_astro=is_astro
                        )
                        channels.append(channel)
                        logger.debug(f"Parsed channel: {channel.name}")
                
                i += 2
            else:
                i += 1
        
        logger.info(f"Parsed {len(channels)} channels from M3U8 content")
        return channels
    
    async def fetch_and_parse(self, source: str) -> List[Channel]:
        try:
            if source.startswith('http://') or source.startswith('https://'):
                return await self._fetch_remote(source)
            else:
                return await self._read_local(source)
        except Exception as e:
            logger.error(f"Error parsing M3U8 source {source}: {e}")
            return []
    
    async def _fetch_remote(self, url: str) -> List[Channel]:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=30)) as response:
                    if response.status == 200:
                        content = await response.text()
                        return self.parse_m3u8_content(content)
                    else:
                        logger.error(f"Failed to fetch {url}: HTTP {response.status}")
                        return []
        except Exception as e:
            logger.error(f"Error fetching remote M3U8 {url}: {e}")
            return []
    
    async def _read_local(self, filepath: str) -> List[Channel]:
        try:
            import aiofiles
            async with aiofiles.open(filepath, 'r', encoding='utf-8') as f:
                content = await f.read()
                return self.parse_m3u8_content(content)
        except Exception as e:
            logger.error(f"Error reading local M3U8 {filepath}: {e}")
            return []
