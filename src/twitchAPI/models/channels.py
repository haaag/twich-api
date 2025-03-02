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
    """
    Represents data for a Twitch channel.

    Attributes:
        broadcaster_language (str): The language of the broadcaster.
        broadcaster_login (str): The login name of the broadcaster.
        display_name (str): The display name of the channel.
        game_id (str): The unique identifier of the game being played on the channel.
        game_name (str): The name of the game being played.
        id (str): The unique identifier of the channel.
        is_live (bool): Indicates if the channel is currently live.
        started_at (str): The timestamp when the channel started streaming (ISO 8601 format).
        tag_ids (List[str]): A list of tag IDs associated with the channel.
        tags (List[str]): A list of tag names associated with the channel.
        thumbnail_url (str): The URL of the channel's thumbnail image.
        title (str): The title of the channel's current stream.

    https://dev.twitch.tv/docs/api/reference/#search-channels
    """

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
    """
    Represents information about a Twitch channel that a user follows.

    Attributes:
        broadcaster_id (str): The unique identifier of the broadcaster.
        broadcaster_name (str): The display name of the broadcaster.
        broadcaster_login (str): The login name of the broadcaster.
        followed_at (str): The timestamp when the user started following the channel (ISO 8601 format).
        live (bool): Indicates if the channel is currently live. Defaults to False.

    https://dev.twitch.tv/docs/api/reference/#get-followed-channels
    """

    broadcaster_id: str
    broadcaster_name: str
    broadcaster_login: str
    followed_at: str
    live: bool = False

    @property
    def name(self) -> str:
        return self.broadcaster_name


@dataclass
class ChannelUser:
    """
    Represents information about a Twitch channel user.

    Attributes:
        broadcaster_type (str): The type of broadcaster (e.g., "partner", "affiliate").
        created_at (str): The timestamp when the user account was created (ISO 8601 format).
        description (str): The description of the user's channel.
        display_name (str): The display name of the user.
        id (str): The unique identifier of the user.
        login (str): The login name of the user.
        offline_image_url (str): The URL of the image displayed when the channel is offline.
        profile_image_url (str): The URL of the user's profile image.
        type (str): The type of user (e.g., "staff", "admin", "global_mod").
        view_count (str): The number of views the user's channel has received.

    https://dev.twitch.tv/docs/api/reference/#get-users
    """

    broadcaster_type: str
    created_at: str
    description: str
    display_name: str
    id: str
    login: str
    offline_image_url: str
    profile_image_url: str
    type: str
    view_count: str
