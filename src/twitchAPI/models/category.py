# twitch.models.category.py

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Game:
    """
    Represents data for a game.

    Attributes:
        id (str): The unique identifier of the game.
        name (str): The name of the game.
        box_art_url (str): The URL of the game's box art image.
        igdb_id (Optional[str]): The unique identifier of the game in the IGDB (Internet Games Database),
        if available. Defaults to None.

    https://dev.twitch.tv/docs/api/reference/#search-categories
    """

    id: str
    name: str
    box_art_url: str
    igdb_id: str | None = None
