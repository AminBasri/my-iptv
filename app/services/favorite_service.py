import json
import aiofiles
from typing import List, Dict, Set
from datetime import datetime
from app.models import Favorite
from app.core import settings, get_logger

logger = get_logger(__name__)


class FavoriteService:
    def __init__(self):
        self.favorites: Dict[str, List[Favorite]] = {"default": []}
        self.favorites_file = settings.favorites_file
    
    async def load_favorites(self):
        try:
            async with aiofiles.open(self.favorites_file, 'r') as f:
                content = await f.read()
                data = json.loads(content)
                self.favorites = {}
                for list_name, favs in data.items():
                    self.favorites[list_name] = [Favorite(**fav) for fav in favs]
                logger.info(f"Loaded favorites from file")
        except FileNotFoundError:
            logger.info("No favorites file found, starting fresh")
            self.favorites = {"default": []}
        except Exception as e:
            logger.error(f"Error loading favorites: {e}")
            self.favorites = {"default": []}
    
    async def save_favorites(self):
        try:
            data = {}
            for list_name, favs in self.favorites.items():
                data[list_name] = [fav.model_dump(mode='json') for fav in favs]
            
            async with aiofiles.open(self.favorites_file, 'w') as f:
                await f.write(json.dumps(data, indent=2, default=str))
            logger.info("Saved favorites to file")
        except Exception as e:
            logger.error(f"Error saving favorites: {e}")
    
    async def add_favorite(self, channel_id: str, list_name: str = "default") -> bool:
        if list_name not in self.favorites:
            self.favorites[list_name] = []
        
        if not any(fav.channel_id == channel_id for fav in self.favorites[list_name]):
            favorite = Favorite(
                channel_id=channel_id,
                added_at=datetime.utcnow(),
                list_name=list_name
            )
            self.favorites[list_name].append(favorite)
            await self.save_favorites()
            logger.info(f"Added channel {channel_id} to favorites list '{list_name}'")
            return True
        return False
    
    async def remove_favorite(self, channel_id: str, list_name: str = "default") -> bool:
        if list_name in self.favorites:
            original_count = len(self.favorites[list_name])
            self.favorites[list_name] = [
                fav for fav in self.favorites[list_name]
                if fav.channel_id != channel_id
            ]
            
            if len(self.favorites[list_name]) < original_count:
                await self.save_favorites()
                logger.info(f"Removed channel {channel_id} from favorites list '{list_name}'")
                return True
        return False
    
    def get_favorites(self, list_name: str = "default") -> List[str]:
        if list_name in self.favorites:
            return [fav.channel_id for fav in self.favorites[list_name]]
        return []
    
    def get_all_lists(self) -> List[str]:
        return list(self.favorites.keys())
    
    def is_favorite(self, channel_id: str, list_name: str = "default") -> bool:
        if list_name in self.favorites:
            return any(fav.channel_id == channel_id for fav in self.favorites[list_name])
        return False
    
    async def create_list(self, list_name: str) -> bool:
        if list_name not in self.favorites:
            self.favorites[list_name] = []
            await self.save_favorites()
            logger.info(f"Created new favorites list: {list_name}")
            return True
        return False
    
    async def delete_list(self, list_name: str) -> bool:
        if list_name in self.favorites and list_name != "default":
            del self.favorites[list_name]
            await self.save_favorites()
            logger.info(f"Deleted favorites list: {list_name}")
            return True
        return False


favorite_service = FavoriteService()
