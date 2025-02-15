# twitch.models.channels.py

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FollowedChannelInfo:
    broadcaster_id: str
    broadcaster_login: str
    broadcaster_name: str
    broadcaster_language: str
    tags: list[str] | None
    game_id: str
    game_name: str
    title: str
    delay: int
    content_classification_labels: list[str] | None = None
    is_branded_content: bool = False
    viewer_count: int = 0


@dataclass(frozen=True)
class FollowedChannel:
    broadcaster_id: str
    broadcaster_login: str
    broadcaster_name: str
    followed_at: str


@dataclass(frozen=True)
class Channel:
    broadcaster_language: str
    broadcaster_login: str
    display_name: str
    game_id: str
    game_name: str
    id: str
    is_live: bool
    started_at: str
    tag_ids: list[str]
    tags: list[str]
    thumbnail_url: str
    title: str


@dataclass(frozen=True)
class ChannelInfo:
    broadcaster_id: str
    broadcaster_name: str
    broadcaster_login: str
    followed_at: str
    live: bool = False


    @property
    def name(self) -> str:
        return self.broadcaster_name
