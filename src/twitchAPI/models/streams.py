# twitch.models.streams.py

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FollowedStream:
    id: str
    game_id: str
    game_name: str
    is_mature: bool
    language: str
    started_at: str
    tag_ids: list[str] | None
    tags: list[str] | None
    thumbnail_url: str
    title: str
    type: str
    user_id: str
    user_login: str
    user_name: str
    viewer_count: int
    live: bool = True


    @property
    def name(self) -> str:
        return self.user_name
