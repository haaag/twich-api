# twitch.models.content.py

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class FollowedContentClip:
    """
    Represents data for a Twitch Clip that a user follows.

    Attributes:
        broadcaster_id (str): The unique identifier of the broadcaster.
        broadcaster_name (str): The name of the broadcaster.
        created_at (str): The timestamp when the clip was created, in ISO 8601 format.
        creator_id (str): The unique identifier of the clip creator.
        creator_name (str): The name of the clip creator.
        duration (float): The duration of the clip in seconds.
        embed_url (str): The URL to embed the clip.
        game_id (str): The unique identifier of the game associated with the clip.
        id (str): The unique identifier of the clip.
        language (str): The language of the clip.
        thumbnail_url (str): The URL of the clip's thumbnail image.
        title (str): The title of the clip.
        url (str): The URL of the clip.
        video_id (str): The unique identifier of the video associated with the clip.
        view_count (int): The number of views the clip has received.
        vod_offset (Optional[int]): The offset in seconds where the clip starts in the VOD, if available.
        is_featured (bool): A flag indicating whether the clip is featured. Defaults to False.

    https://dev.twitch.tv/docs/api/reference#get-clips
    """

    broadcaster_id: str
    broadcaster_name: str
    created_at: str
    creator_id: str
    creator_name: str
    duration: float
    embed_url: str
    game_id: str
    id: str
    language: str
    thumbnail_url: str
    title: str
    url: str
    video_id: str
    view_count: int
    vod_offset: int | None
    is_featured: bool = False


@dataclass(frozen=True)
class FollowedContentVideo:
    """
    Represents data for a video content that a user follows.

    Attributes:
        user_id (str): The unique identifier of the user who created the video.
        user_login (str): The login name of the user who created the video.
        user_name (str): The display name of the user who created the video.
        view_count (int): The number of views the video has received.
        viewable (str): The viewability status of the video (e.g., "public").
        url (str): The URL of the video.
        type (str): The type of the video (e.g., "upload", "archive").
        title (str): The title of the video.
        thumbnail_url (str): The URL of the video's thumbnail image.
        stream_id (str): The unique identifier of the stream associated with the video, if applicable.
        published_at (str): The timestamp when the video was published (ISO 8601 format).
        muted_segments (Any): Information about muted segments in the video, if any.
        language (str): The language of the video.
        id (str): The unique identifier of the video.
        duration (str): The duration of the video in ISO 8601 duration format.
        description (str): The description of the video.
        created_at (str): The timestamp when the video was created (ISO 8601 format).

    https://dev.twitch.tv/docs/api/reference#get-videos
    """

    user_id: str
    user_login: str
    user_name: str
    view_count: int
    viewable: str
    url: str
    type: str
    title: str
    thumbnail_url: str
    stream_id: str
    published_at: str
    muted_segments: Any
    language: str
    id: str
    duration: str
    description: str
    created_at: str
