# utils.py
from __future__ import annotations

from typing import Iterator
from typing import Mapping
from typing import TypeVar

T = TypeVar('T')
U = TypeVar('U')


def group_into_batches(ids: list[str], batch_size: int) -> Iterator[list[str]]:
    """
    Splits a list into batches of the maximum size allowed by the API.
    """
    for i in range(0, len(ids), batch_size):
        yield ids[i : i + batch_size]


def merge_maps(maptwo: Mapping[str, T], mapone: Mapping[str, U]) -> Mapping[str, T | U]:
    return {**mapone, **{k: v for k, v in maptwo.items() if k not in mapone}}
