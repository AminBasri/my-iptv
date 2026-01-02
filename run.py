#!/usr/bin/env python3

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

if __name__ == "__main__":
    import uvicorn
    from app.core.config import settings
    
    print(f"""
    ╔═══════════════════════════════════════════════════════╗
    ║        Malaysian IPTV Application Starting...        ║
    ╚═══════════════════════════════════════════════════════╝
    
    🌐 Web UI:      http://{settings.host}:{settings.port}
    📚 API Docs:    http://{settings.host}:{settings.port}/docs
    🔧 Health:      http://{settings.host}:{settings.port}/health
    
    Press Ctrl+C to stop the server
    """)
    
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level="info"
    )
