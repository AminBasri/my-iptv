from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.models import FavoriteRequest, FavoriteResponse, FavoriteListsResponse, Channel
from app.services import favorite_service, channel_service
from app.core import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/api/favorites", tags=["favorites"])


@router.get("", response_model=FavoriteResponse)
async def get_favorites(list_name: str = Query("default", description="Favorites list name")):
    try:
        favorite_ids = favorite_service.get_favorites(list_name)
        return FavoriteResponse(
            favorites=favorite_ids,
            total=len(favorite_ids),
            list_name=list_name
        )
    except Exception as e:
        logger.error(f"Error getting favorites: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve favorites")


@router.get("/channels", response_model=List[Channel])
async def get_favorite_channels(list_name: str = Query("default", description="Favorites list name")):
    try:
        favorite_ids = favorite_service.get_favorites(list_name)
        channels = []
        for channel_id in favorite_ids:
            channel = channel_service.get_channel_by_id(channel_id)
            if channel:
                channels.append(channel)
        return channels
    except Exception as e:
        logger.error(f"Error getting favorite channels: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve favorite channels")


@router.post("", response_model=dict)
async def add_favorite(request: FavoriteRequest):
    try:
        channel = channel_service.get_channel_by_id(request.channel_id)
        if not channel:
            raise HTTPException(status_code=404, detail="Channel not found")
        
        added = await favorite_service.add_favorite(request.channel_id, request.list_name)
        if added:
            return {
                "message": "Channel added to favorites",
                "channel_id": request.channel_id,
                "list_name": request.list_name
            }
        else:
            return {
                "message": "Channel already in favorites",
                "channel_id": request.channel_id,
                "list_name": request.list_name
            }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error adding favorite: {e}")
        raise HTTPException(status_code=500, detail="Failed to add favorite")


@router.delete("/{channel_id}")
async def remove_favorite(
    channel_id: str,
    list_name: str = Query("default", description="Favorites list name")
):
    try:
        removed = await favorite_service.remove_favorite(channel_id, list_name)
        if removed:
            return {
                "message": "Channel removed from favorites",
                "channel_id": channel_id,
                "list_name": list_name
            }
        else:
            raise HTTPException(status_code=404, detail="Channel not in favorites")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error removing favorite: {e}")
        raise HTTPException(status_code=500, detail="Failed to remove favorite")


@router.get("/lists", response_model=FavoriteListsResponse)
async def get_favorite_lists():
    try:
        lists = favorite_service.get_all_lists()
        return FavoriteListsResponse(
            lists=lists,
            total=len(lists)
        )
    except Exception as e:
        logger.error(f"Error getting favorite lists: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve favorite lists")


@router.post("/lists")
async def create_favorite_list(list_name: str = Query(..., description="List name")):
    try:
        created = await favorite_service.create_list(list_name)
        if created:
            return {"message": "List created successfully", "list_name": list_name}
        else:
            return {"message": "List already exists", "list_name": list_name}
    except Exception as e:
        logger.error(f"Error creating favorite list: {e}")
        raise HTTPException(status_code=500, detail="Failed to create favorite list")


@router.delete("/lists/{list_name}")
async def delete_favorite_list(list_name: str):
    try:
        if list_name == "default":
            raise HTTPException(status_code=400, detail="Cannot delete default list")
        
        deleted = await favorite_service.delete_list(list_name)
        if deleted:
            return {"message": "List deleted successfully", "list_name": list_name}
        else:
            raise HTTPException(status_code=404, detail="List not found")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting favorite list: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete favorite list")


@router.get("/{channel_id}/check")
async def check_favorite(
    channel_id: str,
    list_name: str = Query("default", description="Favorites list name")
):
    try:
        is_fav = favorite_service.is_favorite(channel_id, list_name)
        return {
            "channel_id": channel_id,
            "is_favorite": is_fav,
            "list_name": list_name
        }
    except Exception as e:
        logger.error(f"Error checking favorite: {e}")
        raise HTTPException(status_code=500, detail="Failed to check favorite status")
