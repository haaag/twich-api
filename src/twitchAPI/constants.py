# constants.py
from __future__ import annotations

import httpx

# Twitch
TWITCH_STREAM_BASE_URL = httpx.URL('https://www.twitch.tv/')
TWITCH_CHAT_BASE_URL = httpx.URL('https://www.twitch.tv/popout/')

# Helix
TWITCH_HELIX_BASE_URL = httpx.URL('https://api.twitch.tv/helix/')

# API
MAX_RETRY_ATTEMPTS = 3
RETRY_DELAY = 1
MAX_ITEMS_PER_REQUEST = 100
DEFAULT_REQUESTED_ITEMS = 200
