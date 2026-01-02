#!/usr/bin/env python3
"""
Test script for Malaysian IPTV application
Verifies core functionality without requiring external services
"""

import sys
import asyncio
from app.parsers.m3u8_parser import M3U8Parser
from app.parsers.epg_parser import EPGParser
from app.services.channel_service import ChannelService
from app.services.favorite_service import FavoriteService
from app.core.config import settings

def print_header(text):
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")

async def test_m3u8_parser():
    print_header("Testing M3U8 Parser")
    parser = M3U8Parser()
    
    m3u8_content = """#EXTM3U
#EXTINF:-1 tvg-id="TV3.my" tvg-name="TV3" tvg-logo="http://example.com/tv3.png" group-title="News",TV3
http://example.com/tv3.m3u8
#EXTINF:-1 tvg-id="Astro.my" tvg-name="Astro Ria" group-title="Entertainment",Astro Ria
http://example.com/astro.m3u8
"""
    
    channels = parser.parse_m3u8_content(m3u8_content)
    print(f"✓ Parsed {len(channels)} channels")
    
    for channel in channels:
        print(f"  - {channel.name} ({channel.group})")
        print(f"    URL: {channel.url}")
        print(f"    Astro: {channel.is_astro}")
    
    return len(channels) == 2

async def test_epg_parser():
    print_header("Testing EPG Parser")
    parser = EPGParser()
    
    xmltv_content = """<?xml version="1.0" encoding="UTF-8"?>
<tv>
  <programme start="20240101200000 +0800" stop="20240101210000 +0800" channel="TV3.my">
    <title>News at 8</title>
    <desc>Evening news bulletin</desc>
    <category>News</category>
  </programme>
</tv>
"""
    
    epg_data = parser.parse_xmltv(xmltv_content)
    print(f"✓ Parsed EPG for {len(epg_data)} channels")
    
    for channel_id, programs in epg_data.items():
        print(f"  - {channel_id}: {len(programs)} programs")
        for program in programs:
            print(f"    • {program.title} ({program.category})")
    
    return len(epg_data) > 0

async def test_channel_service():
    print_header("Testing Channel Service")
    service = ChannelService()
    
    test_m3u8 = "./data/example_channels.m3u8"
    try:
        channels = await service.parser.fetch_and_parse(test_m3u8)
        print(f"✓ Loaded {len(channels)} channels from example file")
        
        if channels:
            print(f"\nFirst 5 channels:")
            for channel in channels[:5]:
                print(f"  - {channel.name}")
        
        service.channels = channels
        service.channels_by_id = {ch.id: ch for ch in channels}
        
        groups = service.get_all_groups()
        print(f"\n✓ Found {len(groups)} channel groups:")
        for group in sorted(groups)[:5]:
            print(f"  - {group}")
        
        if channels:
            search_results = service.search_channels("TV")
            print(f"\n✓ Search for 'TV' returned {len(search_results)} results")
        
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

async def test_favorite_service():
    print_header("Testing Favorite Service")
    service = FavoriteService()
    
    await service.add_favorite("test_channel_1", "default")
    print("✓ Added channel to favorites")
    
    favorites = service.get_favorites("default")
    print(f"✓ Retrieved {len(favorites)} favorites")
    
    is_fav = service.is_favorite("test_channel_1", "default")
    print(f"✓ Check favorite status: {is_fav}")
    
    await service.remove_favorite("test_channel_1", "default")
    print("✓ Removed channel from favorites")
    
    return True

async def test_settings():
    print_header("Testing Configuration")
    print(f"App Name: {settings.app_name}")
    print(f"Version: {settings.app_version}")
    print(f"Debug: {settings.debug}")
    print(f"Host: {settings.host}")
    print(f"Port: {settings.port}")
    print(f"M3U8 Sources: {len(settings.m3u8_sources)}")
    for source in settings.m3u8_sources:
        print(f"  - {source}")
    print(f"EPG Enabled: {settings.epg_cache_enabled}")
    print(f"EPG Refresh Interval: {settings.epg_refresh_interval}s")
    return True

async def main():
    print("\n" + "="*60)
    print("  Malaysian IPTV - Application Test Suite")
    print("="*60)
    
    results = []
    
    try:
        results.append(("Settings", await test_settings()))
    except Exception as e:
        print(f"✗ Settings test failed: {e}")
        results.append(("Settings", False))
    
    try:
        results.append(("M3U8 Parser", await test_m3u8_parser()))
    except Exception as e:
        print(f"✗ M3U8 Parser test failed: {e}")
        results.append(("M3U8 Parser", False))
    
    try:
        results.append(("EPG Parser", await test_epg_parser()))
    except Exception as e:
        print(f"✗ EPG Parser test failed: {e}")
        results.append(("EPG Parser", False))
    
    try:
        results.append(("Channel Service", await test_channel_service()))
    except Exception as e:
        print(f"✗ Channel Service test failed: {e}")
        results.append(("Channel Service", False))
    
    try:
        results.append(("Favorite Service", await test_favorite_service()))
    except Exception as e:
        print(f"✗ Favorite Service test failed: {e}")
        results.append(("Favorite Service", False))
    
    print_header("Test Results")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\n{passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Application is ready to use.")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
