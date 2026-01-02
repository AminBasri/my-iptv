from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from contextlib import asynccontextmanager

from app.core import settings, setup_logging, get_logger
from app.services import channel_service, epg_service, favorite_service
from app.api import channels, play, epg, favorites

setup_logging("INFO" if not settings.debug else "DEBUG")
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Malaysian IPTV application...")
    
    await channel_service.load_channels()
    logger.info(f"Loaded {len(channel_service.channels)} channels")
    
    await favorite_service.load_favorites()
    logger.info("Loaded favorites")
    
    await epg_service.start_auto_refresh()
    logger.info("Started EPG auto-refresh")
    
    yield
    
    logger.info("Shutting down Malaysian IPTV application...")
    await epg_service.stop_auto_refresh()


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Malaysian IPTV streaming platform with M3U8 support and EPG integration",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

app.include_router(channels.router)
app.include_router(play.router)
app.include_router(epg.router)
app.include_router(favorites.router)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "app_name": settings.app_name,
        "version": settings.app_version,
        "channels_loaded": len(channel_service.channels),
        "groups_available": len(channel_service.get_all_groups()),
        "epg_channels": len(epg_service.parser.epg_data)
    }


@app.get("/api/info")
async def app_info():
    return {
        "app_name": settings.app_name,
        "version": settings.app_version,
        "total_channels": len(channel_service.channels),
        "total_groups": len(channel_service.get_all_groups()),
        "m3u8_sources": settings.m3u8_sources,
        "epg_enabled": settings.epg_cache_enabled,
        "features": [
            "M3U8 Playlist Parsing",
            "Channel Search & Filtering",
            "EPG (Electronic Program Guide)",
            "Favorites Management",
            "Astro Channel Support",
            "HLS Streaming",
            "Multi-source Support"
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )
