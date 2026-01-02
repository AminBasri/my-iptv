# Malaysian IPTV API Reference

Complete API documentation for the Malaysian IPTV application.

## Base URL

```
http://localhost:8000
```

## Authentication

Currently, the API does not require authentication. This is suitable for personal use or internal networks.

---

## Channels API

### List Channels

Retrieve a paginated list of all channels.

**Endpoint:** `GET /api/channels`

**Query Parameters:**
- `page` (integer, default: 1) - Page number
- `page_size` (integer, default: 50, max: 200) - Items per page
- `group` (string, optional) - Filter by channel group

**Response:**
```json
{
  "channels": [
    {
      "id": "abc123",
      "name": "TV3",
      "logo": "https://example.com/tv3.png",
      "group": "News",
      "url": "https://stream.example.com/tv3.m3u8",
      "epg_id": "TV3.my",
      "language": "Malay",
      "country": "MY",
      "tvg_id": "TV3.my",
      "tvg_name": "TV3",
      "radio": false,
      "is_astro": false
    }
  ],
  "total": 100,
  "page": 1,
  "page_size": 50
}
```

**Example:**
```bash
curl "http://localhost:8000/api/channels?page=1&page_size=20&group=News"
```

---

### Search Channels

Search for channels by name or group.

**Endpoint:** `GET /api/channels/search`

**Query Parameters:**
- `q` (string, required) - Search query
- `page` (integer, default: 1) - Page number
- `page_size` (integer, default: 50, max: 200) - Items per page

**Response:** Same as List Channels

**Example:**
```bash
curl "http://localhost:8000/api/channels/search?q=tv3"
```

---

### Get Channel Details

Retrieve details for a specific channel.

**Endpoint:** `GET /api/channels/{channel_id}`

**Path Parameters:**
- `channel_id` (string, required) - Channel ID

**Response:**
```json
{
  "id": "abc123",
  "name": "TV3",
  "logo": "https://example.com/tv3.png",
  "group": "News",
  "url": "https://stream.example.com/tv3.m3u8",
  "epg_id": "TV3.my",
  "language": "Malay",
  "country": "MY",
  "tvg_id": "TV3.my",
  "tvg_name": "TV3",
  "radio": false,
  "is_astro": false
}
```

**Example:**
```bash
curl "http://localhost:8000/api/channels/abc123"
```

**Error Response:**
```json
{
  "detail": "Channel not found"
}
```
Status: 404

---

### List Channel Groups

Get all available channel groups/categories.

**Endpoint:** `GET /api/channels/groups`

**Response:**
```json
{
  "groups": ["News", "Entertainment", "Sports", "Education"],
  "total": 4
}
```

**Example:**
```bash
curl "http://localhost:8000/api/channels/groups"
```

---

### List Astro Channels

Get all Astro-specific channels.

**Endpoint:** `GET /api/channels/astro`

**Query Parameters:**
- `page` (integer, default: 1) - Page number
- `page_size` (integer, default: 50, max: 200) - Items per page

**Response:** Same as List Channels

**Example:**
```bash
curl "http://localhost:8000/api/channels/astro"
```

---

### Refresh Channels

Refresh the channel list from M3U8 sources.

**Endpoint:** `POST /api/channels/refresh`

**Response:**
```json
{
  "message": "Channels refreshed successfully",
  "total": 100
}
```

**Example:**
```bash
curl -X POST "http://localhost:8000/api/channels/refresh"
```

---

## Playback API

### Get Stream URL

Get the stream URL for a channel.

**Endpoint:** `GET /api/play/{channel_id}`

**Path Parameters:**
- `channel_id` (string, required) - Channel ID

**Query Parameters:**
- `redirect` (boolean, default: false) - Redirect to stream URL

**Response:**
```json
{
  "channel_id": "abc123",
  "channel_name": "TV3",
  "stream_url": "https://stream.example.com/tv3.m3u8",
  "stream_type": "hls",
  "logo": "https://example.com/tv3.png",
  "group": "News"
}
```

**Example:**
```bash
curl "http://localhost:8000/api/play/abc123"
```

---

### Get Stream Information

Get detailed information about a stream.

**Endpoint:** `GET /api/play/{channel_id}/info`

**Path Parameters:**
- `channel_id` (string, required) - Channel ID

**Response:**
```json
{
  "channel_id": "abc123",
  "channel_name": "TV3",
  "stream_url": "https://stream.example.com/tv3.m3u8",
  "stream_type": "hls",
  "is_valid": true,
  "supports_hls": true,
  "supports_dash": false
}
```

**Example:**
```bash
curl "http://localhost:8000/api/play/abc123/info"
```

---

## EPG API

### Get All EPG Data

Retrieve EPG data for all channels or a specific channel.

**Endpoint:** `GET /api/epg`

**Query Parameters:**
- `channel_id` (string, optional) - Filter by channel ID

**Response:**
```json
{
  "programs": [
    {
      "channel_id": "TV3.my",
      "title": "News at 8",
      "description": "Evening news bulletin",
      "start_time": "2024-01-01T20:00:00",
      "end_time": "2024-01-01T21:00:00",
      "category": "News",
      "icon": null
    }
  ],
  "channel_id": null,
  "total": 1
}
```

**Example:**
```bash
curl "http://localhost:8000/api/epg?channel_id=TV3.my"
```

---

### Get Channel EPG

Get current and upcoming programs for a specific channel.

**Endpoint:** `GET /api/epg/{channel_id}`

**Path Parameters:**
- `channel_id` (string, required) - Channel ID

**Response:**
```json
{
  "channel_id": "abc123",
  "channel_name": "TV3",
  "current_program": {
    "channel_id": "TV3.my",
    "title": "News at 8",
    "description": "Evening news bulletin",
    "start_time": "2024-01-01T20:00:00",
    "end_time": "2024-01-01T21:00:00",
    "category": "News",
    "icon": null
  },
  "upcoming_programs": [
    {
      "channel_id": "TV3.my",
      "title": "Drama Show",
      "description": "Popular drama series",
      "start_time": "2024-01-01T21:00:00",
      "end_time": "2024-01-01T22:00:00",
      "category": "Entertainment",
      "icon": null
    }
  ]
}
```

**Example:**
```bash
curl "http://localhost:8000/api/epg/abc123"
```

---

### Search Programs

Search EPG programs by title or description.

**Endpoint:** `GET /api/epg/search`

**Query Parameters:**
- `q` (string, required) - Search query

**Response:** Same as Get All EPG Data

**Example:**
```bash
curl "http://localhost:8000/api/epg/search?q=news"
```

---

### Refresh EPG Data

Refresh EPG data from configured sources.

**Endpoint:** `POST /api/epg/refresh`

**Response:**
```json
{
  "message": "EPG data refreshed successfully",
  "total_channels": 50
}
```

**Example:**
```bash
curl -X POST "http://localhost:8000/api/epg/refresh"
```

---

### Add EPG Source

Add a new EPG XML source.

**Endpoint:** `POST /api/epg/sources`

**Query Parameters:**
- `url` (string, required) - EPG XML URL

**Response:**
```json
{
  "message": "EPG source added successfully",
  "url": "https://example.com/epg.xml"
}
```

**Example:**
```bash
curl -X POST "http://localhost:8000/api/epg/sources?url=https://example.com/epg.xml"
```

---

## Favorites API

### Get Favorites

Get list of favorite channel IDs.

**Endpoint:** `GET /api/favorites`

**Query Parameters:**
- `list_name` (string, default: "default") - Favorites list name

**Response:**
```json
{
  "favorites": ["abc123", "def456"],
  "total": 2,
  "list_name": "default"
}
```

**Example:**
```bash
curl "http://localhost:8000/api/favorites?list_name=default"
```

---

### Get Favorite Channels

Get full channel details for favorites.

**Endpoint:** `GET /api/favorites/channels`

**Query Parameters:**
- `list_name` (string, default: "default") - Favorites list name

**Response:** Array of Channel objects

**Example:**
```bash
curl "http://localhost:8000/api/favorites/channels?list_name=default"
```

---

### Add Favorite

Add a channel to favorites.

**Endpoint:** `POST /api/favorites`

**Request Body:**
```json
{
  "channel_id": "abc123",
  "list_name": "default"
}
```

**Response:**
```json
{
  "message": "Channel added to favorites",
  "channel_id": "abc123",
  "list_name": "default"
}
```

**Example:**
```bash
curl -X POST "http://localhost:8000/api/favorites" \
  -H "Content-Type: application/json" \
  -d '{"channel_id": "abc123", "list_name": "default"}'
```

---

### Remove Favorite

Remove a channel from favorites.

**Endpoint:** `DELETE /api/favorites/{channel_id}`

**Path Parameters:**
- `channel_id` (string, required) - Channel ID

**Query Parameters:**
- `list_name` (string, default: "default") - Favorites list name

**Response:**
```json
{
  "message": "Channel removed from favorites",
  "channel_id": "abc123",
  "list_name": "default"
}
```

**Example:**
```bash
curl -X DELETE "http://localhost:8000/api/favorites/abc123?list_name=default"
```

---

### List Favorite Lists

Get all favorite list names.

**Endpoint:** `GET /api/favorites/lists`

**Response:**
```json
{
  "lists": ["default", "sports", "news"],
  "total": 3
}
```

**Example:**
```bash
curl "http://localhost:8000/api/favorites/lists"
```

---

### Create Favorite List

Create a new favorites list.

**Endpoint:** `POST /api/favorites/lists`

**Query Parameters:**
- `list_name` (string, required) - List name

**Response:**
```json
{
  "message": "List created successfully",
  "list_name": "sports"
}
```

**Example:**
```bash
curl -X POST "http://localhost:8000/api/favorites/lists?list_name=sports"
```

---

### Delete Favorite List

Delete a favorites list.

**Endpoint:** `DELETE /api/favorites/lists/{list_name}`

**Path Parameters:**
- `list_name` (string, required) - List name (cannot be "default")

**Response:**
```json
{
  "message": "List deleted successfully",
  "list_name": "sports"
}
```

**Example:**
```bash
curl -X DELETE "http://localhost:8000/api/favorites/lists/sports"
```

---

### Check Favorite Status

Check if a channel is in favorites.

**Endpoint:** `GET /api/favorites/{channel_id}/check`

**Path Parameters:**
- `channel_id` (string, required) - Channel ID

**Query Parameters:**
- `list_name` (string, default: "default") - Favorites list name

**Response:**
```json
{
  "channel_id": "abc123",
  "is_favorite": true,
  "list_name": "default"
}
```

**Example:**
```bash
curl "http://localhost:8000/api/favorites/abc123/check?list_name=default"
```

---

## System API

### Home Page

Web UI home page.

**Endpoint:** `GET /`

**Response:** HTML page

---

### Health Check

Check application health and status.

**Endpoint:** `GET /health`

**Response:**
```json
{
  "status": "healthy",
  "app_name": "Malaysian IPTV",
  "version": "1.0.0",
  "channels_loaded": 100,
  "groups_available": 10,
  "epg_channels": 50
}
```

**Example:**
```bash
curl "http://localhost:8000/health"
```

---

### Application Information

Get application information and features.

**Endpoint:** `GET /api/info`

**Response:**
```json
{
  "app_name": "Malaysian IPTV",
  "version": "1.0.0",
  "total_channels": 100,
  "total_groups": 10,
  "m3u8_sources": ["https://example.com/playlist.m3u"],
  "epg_enabled": true,
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
```

**Example:**
```bash
curl "http://localhost:8000/api/info"
```

---

## Error Responses

### Common Error Codes

- **400 Bad Request** - Invalid request parameters
- **404 Not Found** - Resource not found
- **500 Internal Server Error** - Server error

### Error Format

```json
{
  "detail": "Error message description"
}
```

---

## Rate Limiting

Currently, no rate limiting is implemented. For production use, consider implementing rate limiting middleware.

---

## CORS

CORS is configured to allow requests from configured origins in the `.env` file.

---

## API Documentation

Interactive API documentation is available at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## WebSocket Support

WebSocket support is not currently implemented but can be added for real-time updates.

---

## Data Formats

### Channel Object

```json
{
  "id": "string",
  "name": "string",
  "logo": "string|null",
  "group": "string|null",
  "url": "string",
  "epg_id": "string|null",
  "language": "string|null",
  "country": "string",
  "tvg_id": "string|null",
  "tvg_name": "string|null",
  "radio": "boolean",
  "is_astro": "boolean"
}
```

### EPG Program Object

```json
{
  "channel_id": "string",
  "title": "string",
  "description": "string|null",
  "start_time": "datetime",
  "end_time": "datetime",
  "category": "string|null",
  "icon": "string|null"
}
```

---

## Examples Collection

### Complete Workflow Example

```bash
# 1. Check health
curl http://localhost:8000/health

# 2. Get all channels
curl http://localhost:8000/api/channels

# 3. Search for a channel
curl "http://localhost:8000/api/channels/search?q=tv3"

# 4. Get channel details
CHANNEL_ID="abc123"
curl "http://localhost:8000/api/channels/$CHANNEL_ID"

# 5. Get stream URL
curl "http://localhost:8000/api/play/$CHANNEL_ID"

# 6. Add to favorites
curl -X POST "http://localhost:8000/api/favorites" \
  -H "Content-Type: application/json" \
  -d "{\"channel_id\": \"$CHANNEL_ID\"}"

# 7. Get EPG
curl "http://localhost:8000/api/epg/$CHANNEL_ID"

# 8. List favorites
curl "http://localhost:8000/api/favorites"
```

---

For more information, visit the [main documentation](README.md).
