# twitch.models.category.py

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Game:
    id: str
    name: str
    box_art_url: str
    igdb_id: str | None = None
