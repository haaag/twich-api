# twitch.py

from __future__ import annotations

import logging
from typing import TYPE_CHECKING
from typing import Iterable

from twitchAPI.models.category import Game
from twitchAPI.models.channels import Channel
from twitchAPI.models.channels import ChannelInfo
from twitchAPI.models.content import FollowedContentClip
from twitchAPI.models.content import FollowedContentVideo
from twitchAPI.models.streams import FollowedStream

if TYPE_CHECKING:
    from twitchAPI.api_helix import HelixAPI

logger = logging.getLogger(__name__)


class Twitch:
    def __init__(self, api: HelixAPI) -> None:
        self.api = api
        self._online: int = 0

    @property
    def online(self) -> int:
        return self._online

    async def channels(self) -> list[ChannelInfo]:
        """Fetches information about all channels that the user follows."""
        data = await self.api.channels.all()
        return [ChannelInfo(**c) for c in data]

    async def streams(self) -> list[FollowedStream]:
        """Fetches information about all streams that the user follows."""
        data = await self.api.channels.streams()
        if len(data) > 0:
            self._online = len(data)
        return [FollowedStream(**c) for c in data]

    async def clips(self, user_id: str) -> Iterable[FollowedContentClip]:
        """Fetches all clips from the given user_id."""
        data = await self.api.content.clips(user_id=user_id)
        return (FollowedContentClip(**clip) for clip in data)

    async def videos(self, user_id: str) -> Iterable[FollowedContentVideo]:
        """Fetches all videos from the given user_id."""
        data = await self.api.content.videos(user_id=user_id)
        return (FollowedContentVideo(**video) for video in data)

    async def games_by_query(self, query: str) -> Iterable[Game]:
        """Fetches all games that match the given query."""
        data = await self.api.content.search_categories(query)
        return (Game(**item) for item in data)

    async def streams_by_game_id(self, game_id: int) -> Iterable[FollowedStream]:
        """Fetches all streams that match the given game_id."""
        logger.debug('getting streams by game_id: %s', game_id)
        data = await self.api.channels.streams_by_game_id(game_id)
        return (FollowedStream(**stream) for stream in data)

    async def channels_by_query(self, query: str, live_only: bool = True) -> Iterable[Channel]:
        data = await self.api.channels.search(query, live_only=live_only)
        data_sorted_by_live = sorted(data, key=lambda c: c['is_live'], reverse=True)
        return (Channel(**item) for item in data_sorted_by_live if item['game_name'])
