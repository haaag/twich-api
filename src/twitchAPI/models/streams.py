# twitch.models.streams.py

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class FollowedStream:
    """
    Represents data for a Twitch stream that a user follows.

    Attributes:
        id: The stream ID.
        game_id: The game ID being played on the stream.
        game_name: The name of the game being played.
        is_mature: Indicates if the stream is marked as mature content.
        language: The language of the stream.
        started_at: The timestamp when the stream started (ISO 8601 format).
        tag_ids: A list of tag IDs associated with the stream, or None if no tags are present.
        tags: A list of tag names associated with the stream, or None if no tags are present.
        thumbnail_url: URL for the stream's thumbnail image.
        title: The title of the stream.
        type: The type of stream (e.g., "live").
        user_id: The broadcaster's user ID.
        user_login: The broadcaster's user login name.
        user_name: The broadcaster's user display name.
        viewer_count: The current number of viewers watching the stream.
        live: A boolean indicating if the stream is currently live (defaults to True).

    https://dev.twitch.tv/docs/api/reference#get-followed-streams
    """

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
