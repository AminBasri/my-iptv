# Quick Start Guide

Get your Malaysian IPTV application running in 5 minutes!

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Installation (Automated)

```bash
# Run the setup script
./setup.sh

# Activate virtual environment
source venv/bin/activate

# Start the application
python run.py
```

## Installation (Manual)

### 1. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
cp .env.example .env
# Edit .env if needed
```

### 4. Start the Application

```bash
# Option 1: Using run.py
python run.py

# Option 2: Using uvicorn directly
uvicorn app.main:app --reload

# Option 3: Using Python module
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Access the Application

Once started, open your browser and navigate to:

- **Web UI**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## Using the Application

### 1. Browse Channels

The home page displays all available channels in a grid layout.

### 2. Search for Channels

Use the search box at the top to find specific channels by name.

### 3. Filter by Category

Click on a category in the sidebar or use the dropdown menu to filter channels.

### 4. Play a Channel

Click on any channel card to open the video player and start streaming.

### 5. Add to Favorites

Click the heart icon on any channel card to add it to your favorites.

## Adding Your M3U8 Playlist

### Method 1: Environment Variable

Edit `.env` and add your M3U8 playlist URL:

```env
M3U8_SOURCES=https://example.com/playlist.m3u,/path/to/local/playlist.m3u8
```

### Method 2: Use Example Playlist

Use the included example playlist:

```env
M3U8_SOURCES=./data/example_channels.m3u8
```

### Method 3: Via API

After starting the app, refresh channels with a new source:

```bash
# Edit the config and restart, or use local file
```

## Testing the API

### Get Channel List

```bash
curl http://localhost:8000/api/channels
```

### Search Channels

```bash
curl "http://localhost:8000/api/channels/search?q=tv3"
```

### Get Channel Groups

```bash
curl http://localhost:8000/api/channels/groups
```

### Play a Channel

```bash
curl http://localhost:8000/api/play/{channel_id}
```

## Common Issues

### Port Already in Use

Change the port in `.env`:

```env
PORT=8001
```

Or specify when running:

```bash
uvicorn app.main:app --port 8001
```

### No Channels Loading

1. Check your M3U8 source URL is accessible
2. Verify the M3U8 format is correct
3. Try the example playlist: `./data/example_channels.m3u8`
4. Check logs for errors

### Stream Not Playing

1. Verify stream URL is accessible
2. Check browser console for errors
3. Ensure HLS.js is loaded
4. Try a different browser

## Development Mode

For development with auto-reload:

```bash
uvicorn app.main:app --reload --log-level debug
```

## Docker Deployment

### Using Docker Compose

```bash
# Build and start
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

### Using Docker

```bash
# Build
docker build -t my-iptv .

# Run
docker run -p 8000:8000 -v $(pwd)/data:/app/data my-iptv
```

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check [CONTRIBUTING.md](CONTRIBUTING.md) if you want to contribute
- Customize the frontend in `app/static/`
- Add your own M3U8 playlists
- Configure EPG sources

## Support

If you encounter issues:

1. Check the logs for error messages
2. Verify your Python version: `python --version`
3. Ensure all dependencies are installed
4. Try the example playlist first
5. Open an issue on GitHub

## Quick Reference

### Useful Commands

```bash
# Start server
python run.py

# Check health
curl http://localhost:8000/health

# Refresh channels
curl -X POST http://localhost:8000/api/channels/refresh

# View logs
tail -f logs/app.log

# Stop server
# Press Ctrl+C in the terminal
```

### Directory Structure

```
my-iptv/
├── app/           # Application code
├── data/          # Data storage (channels, favorites)
├── venv/          # Virtual environment
└── *.py           # Scripts
```

## Tips

- Keep your `.env` file secure (don't commit it)
- Regularly refresh channels to get updates
- Use favorites to organize your channels
- Check `/docs` for complete API documentation
- Monitor `/health` endpoint for system status

---

Enjoy your Malaysian IPTV experience! 🇲🇾📺
