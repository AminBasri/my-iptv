from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from app.models import EPGResponse, EPGChannelPrograms
from app.services import epg_service, channel_service
from app.core import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/api/epg", tags=["epg"])


@router.get("", response_model=EPGResponse)
async def get_all_epg(
    channel_id: Optional[str] = Query(None, description="Filter by channel ID")
):
    try:
        programs = epg_service.get_all_programs(channel_id)
        return EPGResponse(
            programs=programs,
            channel_id=channel_id,
            total=len(programs)
        )
    except Exception as e:
        logger.error(f"Error getting EPG data: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve EPG data")


@router.get("/{channel_id}", response_model=EPGChannelPrograms)
async def get_channel_epg(channel_id: str):
    try:
        channel = channel_service.get_channel_by_id(channel_id)
        channel_name = channel.name if channel else channel_id
        
        epg_id = channel_id
        if channel and channel.epg_id:
            epg_id = channel.epg_id
        
        epg_data = epg_service.get_channel_programs(epg_id, channel_name)
        return epg_data
    
    except Exception as e:
        logger.error(f"Error getting EPG for channel {channel_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve channel EPG")


@router.post("/refresh")
async def refresh_epg():
    try:
        await epg_service.refresh_epg()
        total_channels = len(epg_service.parser.epg_data)
        return {
            "message": "EPG data refreshed successfully",
            "total_channels": total_channels
        }
    except Exception as e:
        logger.error(f"Error refreshing EPG: {e}")
        raise HTTPException(status_code=500, detail="Failed to refresh EPG data")


@router.post("/sources")
async def add_epg_source(url: str = Query(..., description="EPG XML URL")):
    try:
        epg_service.add_epg_url(url)
        return {"message": "EPG source added successfully", "url": url}
    except Exception as e:
        logger.error(f"Error adding EPG source: {e}")
        raise HTTPException(status_code=500, detail="Failed to add EPG source")


@router.get("/search", response_model=EPGResponse)
async def search_programs(q: str = Query(..., min_length=1, description="Search query")):
    try:
        programs = epg_service.search_programs(q)
        return EPGResponse(
            programs=programs,
            channel_id=None,
            total=len(programs)
        )
    except Exception as e:
        logger.error(f"Error searching programs: {e}")
        raise HTTPException(status_code=500, detail="Failed to search programs")
