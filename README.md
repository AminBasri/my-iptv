# Malaysian IPTV Web Application

A full-stack Malaysian IPTV web application built with FastAPI backend and modern web frontend. Stream Malaysian TV channels with support for M3U8 playlists, EPG (Electronic Program Guide), and Astro channel integration.

## 🚀 Features

- **M3U8 Playlist Parsing**: Support for local and remote M3U8 playlists
- **Channel Management**: Browse, search, and filter channels by category
- **Video Playback**: HLS streaming with adaptive bitrate support
- **EPG Integration**: Electronic Program Guide with XMLTV format support
- **Favorites System**: Save and organize your favorite channels
- **Astro Channel Support**: Dedicated support for Astro Malaysian channels
- **Responsive Web UI**: Modern, mobile-friendly interface
- **Multi-source Support**: Load channels from multiple M3U8 sources
- **Real-time Search**: Fast channel search with debouncing
- **Category Filtering**: Browse channels by group/category

## 📋 Requirements

- Python 3.8+
- Modern web browser with HLS support

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd my-iptv
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configuration

Copy the example environment file and configure:

```bash
cp .env.example .env
```

Edit `.env` to customize settings:

```env
# Application Settings
APP_NAME=Malaysian IPTV
DEBUG=True
HOST=0.0.0.0
PORT=8000

# M3U8 Sources (comma-separated)
M3U8_SOURCES=https://raw.githubusercontent.com/MIFNtechnology/siaranMy/main/channels.m3u

# EPG Settings
EPG_REFRESH_INTERVAL=3600
EPG_CACHE_ENABLED=True
```

## 🚀 Running the Application

### Development Mode

```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Or simply:

```bash
python app/main.py
```

### Production Mode

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

The application will be available at:
- **Web UI**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **API Alternative Docs**: http://localhost:8000/redoc

## 📖 API Documentation

### Channel Endpoints

#### List All Channels
```http
GET /api/channels?page=1&page_size=50&group=News
```

#### Search Channels
```http
GET /api/channels/search?q=tv3
```

#### Get Channel Details
```http
GET /api/channels/{channel_id}
```

#### List Channel Groups
```http
GET /api/channels/groups
```

#### List Astro Channels
```http
GET /api/channels/astro
```

#### Refresh Channels
```http
POST /api/channels/refresh
```

### Playback Endpoints

#### Get Stream URL
```http
GET /api/play/{channel_id}
```

#### Get Stream Info
```http
GET /api/play/{channel_id}/info
```

### EPG Endpoints

#### Get All EPG Data
```http
GET /api/epg?channel_id=tv3
```

#### Get Channel EPG
```http
GET /api/epg/{channel_id}
```

#### Refresh EPG Data
```http
POST /api/epg/refresh
```

#### Add EPG Source
```http
POST /api/epg/sources?url=https://example.com/epg.xml
```

#### Search Programs
```http
GET /api/epg/search?q=news
```

### Favorites Endpoints

#### Get Favorites
```http
GET /api/favorites?list_name=default
```

#### Get Favorite Channels
```http
GET /api/favorites/channels?list_name=default
```

#### Add Favorite
```http
POST /api/favorites
Content-Type: application/json

{
  "channel_id": "tv3",
  "list_name": "default"
}
```

#### Remove Favorite
```http
DELETE /api/favorites/{channel_id}?list_name=default
```

#### List Favorite Lists
```http
GET /api/favorites/lists
```

#### Create Favorite List
```http
POST /api/favorites/lists?list_name=my_list
```

#### Delete Favorite List
```http
DELETE /api/favorites/lists/{list_name}
```

#### Check Favorite Status
```http
GET /api/favorites/{channel_id}/check?list_name=default
```

## 📁 Project Structure

```
my-iptv/
├── app/
│   ├── api/                    # API routes
│   │   ├── channels.py        # Channel endpoints
│   │   ├── play.py            # Playback endpoints
│   │   ├── epg.py             # EPG endpoints
│   │   └── favorites.py       # Favorites endpoints
│   ├── core/                   # Core configuration
│   │   ├── config.py          # Settings management
│   │   └── logging.py         # Logging setup
│   ├── models/                 # Pydantic models
│   │   ├── channel.py         # Channel models
│   │   ├── epg.py             # EPG models
│   │   └── favorite.py        # Favorite models
│   ├── parsers/                # Parsers
│   │   ├── m3u8_parser.py     # M3U8 playlist parser
│   │   └── epg_parser.py      # EPG XML parser
│   ├── services/               # Business logic
│   │   ├── channel_service.py # Channel management
│   │   ├── epg_service.py     # EPG management
│   │   └── favorite_service.py # Favorites management
│   ├── static/                 # Static files
│   │   ├── css/
│   │   │   └── styles.css     # Application styles
│   │   └── js/
│   │       └── app.js         # Frontend JavaScript
│   ├── templates/              # HTML templates
│   │   └── index.html         # Main page
│   └── main.py                 # Application entry point
├── data/                       # Data storage
│   ├── channels_cache.json    # Cached channels
│   └── favorites.json         # User favorites
├── requirements.txt            # Python dependencies
├── .env.example               # Example environment file
├── .gitignore                 # Git ignore rules
└── README.md                  # This file
```

## 🎯 Usage Guide

### Web Interface

1. **Browse Channels**: View all available channels in a grid layout
2. **Search**: Use the search box to find specific channels
3. **Filter by Category**: Click on categories in the sidebar or use the dropdown
4. **Add to Favorites**: Click the heart icon on any channel card
5. **Play Channel**: Click on a channel card to open the player
6. **View EPG**: Program guide is displayed when playing a channel

### Adding M3U8 Sources

You can add multiple M3U8 sources in your `.env` file:

```env
M3U8_SOURCES=https://example.com/playlist1.m3u,https://example.com/playlist2.m3u,/path/to/local/playlist.m3u
```

### Adding EPG Sources

EPG sources can be added via API:

```bash
curl -X POST "http://localhost:8000/api/epg/sources?url=https://example.com/epg.xml"
```

## 🔧 Configuration Options

| Variable | Default | Description |
|----------|---------|-------------|
| APP_NAME | Malaysian IPTV | Application name |
| DEBUG | True | Enable debug mode |
| HOST | 0.0.0.0 | Server host |
| PORT | 8000 | Server port |
| M3U8_SOURCES | (see .env.example) | M3U8 playlist URLs |
| EPG_REFRESH_INTERVAL | 3600 | EPG refresh interval (seconds) |
| EPG_CACHE_ENABLED | True | Enable EPG caching |
| DATA_DIR | ./data | Data storage directory |

## 🧪 Example M3U8 Format

See `data/example_channels.m3u8` for a sample playlist format.

## 📝 M3U8 Playlist Format

The application supports standard M3U8 format with extended attributes:

```m3u8
#EXTM3U
#EXTINF:-1 tvg-id="TV3.my" tvg-name="TV3" tvg-logo="https://example.com/tv3.png" group-title="News",TV3
https://stream.example.com/tv3/index.m3u8

#EXTINF:-1 tvg-id="Astro1.my" tvg-name="Astro Ria" tvg-logo="https://example.com/astro.png" group-title="Entertainment",Astro Ria
https://stream.example.com/astro/index.m3u8
```

Supported attributes:
- `tvg-id`: EPG channel identifier
- `tvg-name`: Channel name for EPG
- `tvg-logo`: Channel logo URL
- `group-title`: Channel category/group
- `tvg-language`: Channel language
- `tvg-country`: Country code
- `radio`: Set to "true" for radio channels

## 🐛 Troubleshooting

### Channels Not Loading

1. Check M3U8 source URLs are accessible
2. Verify network connectivity
3. Check logs for parsing errors
4. Try refreshing channels via API: `POST /api/channels/refresh`

### Stream Not Playing

1. Ensure HLS.js is loaded (check browser console)
2. Verify stream URL is valid and accessible
3. Check CORS settings if streaming from external sources
4. Try playing in VLC to verify stream validity

### EPG Not Showing

1. Add EPG source URL via API
2. Trigger EPG refresh: `POST /api/epg/refresh`
3. Verify EPG XML format is XMLTV compatible
4. Check channel IDs match between M3U8 and EPG

## 🚀 Deployment

### Docker Deployment (Optional)

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:

```bash
docker build -t my-iptv .
docker run -p 8000:8000 -v $(pwd)/data:/app/data my-iptv
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- [MIFNtechnology/siaranMy](https://github.com/MIFNtechnology/siaranMy) - Malaysian channels reference
- [iptv-org/iptv](https://github.com/iptv-org/iptv) - IPTV resources
- [HLS.js](https://github.com/video-dev/hls.js/) - HLS player library
- FastAPI - Modern Python web framework

## 📞 Support

For issues and questions, please open an issue on the GitHub repository.

## 🔄 Updates

To update channels:
- Web UI: Click the "Refresh" button
- API: `POST /api/channels/refresh`

To update EPG:
- API: `POST /api/epg/refresh`
- Auto-refresh: Configured via `EPG_REFRESH_INTERVAL`

## 🎨 Customization

### Custom Styling

Edit `app/static/css/styles.css` to customize the appearance.

### Adding Features

1. Create new models in `app/models/`
2. Add business logic in `app/services/`
3. Create API endpoints in `app/api/`
4. Update frontend in `app/static/js/app.js`

## 📊 Performance

- Channels are cached in memory for fast access
- EPG data is cached and refreshed periodically
- Pagination reduces initial load time
- Async operations for better concurrency

## 🔒 Security Notes

- No authentication is implemented (add if deploying publicly)
- CORS is configured for specified origins
- Input validation on all API endpoints
- No sensitive data stored

---

**Enjoy streaming Malaysian TV channels! 🇲🇾📺**
