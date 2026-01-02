from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from app.models import ChannelResponse, ChannelGroupsResponse, Channel
from app.services import channel_service
from app.core import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/api/channels", tags=["channels"])


@router.get("", response_model=ChannelResponse)
async def list_channels(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(50, ge=1, le=200, description="Items per page"),
    group: Optional[str] = Query(None, description="Filter by group")
):
    try:
        if group:
            filtered_channels = channel_service.get_channels_by_group(group)
            start = (page - 1) * page_size
            end = start + page_size
            channels = filtered_channels[start:end]
            total = len(filtered_channels)
        else:
            channels, total = channel_service.get_all_channels(page, page_size)
        
        return ChannelResponse(
            channels=channels,
            total=total,
            page=page,
            page_size=page_size
        )
    except Exception as e:
        logger.error(f"Error listing channels: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve channels")


@router.get("/search", response_model=ChannelResponse)
async def search_channels(
    q: str = Query(..., min_length=1, description="Search query"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(50, ge=1, le=200, description="Items per page")
):
    try:
        all_results = channel_service.search_channels(q)
        start = (page - 1) * page_size
        end = start + page_size
        channels = all_results[start:end]
        
        return ChannelResponse(
            channels=channels,
            total=len(all_results),
            page=page,
            page_size=page_size
        )
    except Exception as e:
        logger.error(f"Error searching channels: {e}")
        raise HTTPException(status_code=500, detail="Failed to search channels")


@router.get("/groups", response_model=ChannelGroupsResponse)
async def list_groups():
    try:
        groups = channel_service.get_all_groups()
        return ChannelGroupsResponse(
            groups=groups,
            total=len(groups)
        )
    except Exception as e:
        logger.error(f"Error listing groups: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve groups")


@router.get("/astro", response_model=ChannelResponse)
async def list_astro_channels(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(50, ge=1, le=200, description="Items per page")
):
    try:
        astro_channels = channel_service.get_astro_channels()
        start = (page - 1) * page_size
        end = start + page_size
        channels = astro_channels[start:end]
        
        return ChannelResponse(
            channels=channels,
            total=len(astro_channels),
            page=page,
            page_size=page_size
        )
    except Exception as e:
        logger.error(f"Error listing Astro channels: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve Astro channels")


@router.get("/{channel_id}", response_model=Channel)
async def get_channel(channel_id: str):
    try:
        channel = channel_service.get_channel_by_id(channel_id)
        if not channel:
            raise HTTPException(status_code=404, detail="Channel not found")
        return channel
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting channel {channel_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve channel")


@router.post("/refresh")
async def refresh_channels():
    try:
        await channel_service.refresh_channels()
        return {"message": "Channels refreshed successfully", "total": len(channel_service.channels)}
    except Exception as e:
        logger.error(f"Error refreshing channels: {e}")
        raise HTTPException(status_code=500, detail="Failed to refresh channels")
