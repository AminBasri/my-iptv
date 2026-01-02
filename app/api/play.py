from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
from app.services import channel_service
from app.core import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/api/play", tags=["playback"])


@router.get("/{channel_id}")
async def play_channel(channel_id: str, redirect: bool = False):
    try:
        channel = channel_service.get_channel_by_id(channel_id)
        if not channel:
            raise HTTPException(status_code=404, detail="Channel not found")
        
        if not channel_service.validate_stream_url(channel.url):
            raise HTTPException(status_code=400, detail="Invalid stream URL")
        
        if redirect:
            return RedirectResponse(url=channel.url)
        
        return JSONResponse({
            "channel_id": channel.id,
            "channel_name": channel.name,
            "stream_url": channel.url,
            "stream_type": "hls" if channel.url.endswith('.m3u8') else "unknown",
            "logo": channel.logo,
            "group": channel.group
        })
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting stream for channel {channel_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve stream")


@router.get("/{channel_id}/info")
async def get_stream_info(channel_id: str):
    try:
        channel = channel_service.get_channel_by_id(channel_id)
        if not channel:
            raise HTTPException(status_code=404, detail="Channel not found")
        
        stream_type = "hls"
        if channel.url.endswith('.m3u8') or channel.url.endswith('.m3u'):
            stream_type = "hls"
        elif channel.url.endswith('.mpd'):
            stream_type = "dash"
        else:
            stream_type = "unknown"
        
        return {
            "channel_id": channel.id,
            "channel_name": channel.name,
            "stream_url": channel.url,
            "stream_type": stream_type,
            "is_valid": channel_service.validate_stream_url(channel.url),
            "supports_hls": stream_type == "hls",
            "supports_dash": stream_type == "dash"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting stream info for channel {channel_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve stream info")
