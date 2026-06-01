"""Tile data class for the 2048 game."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Tile:
    """Represents a tile on the board."""
    value: int
    row: int
    col: int
    merged_this_turn: bool = False
    is_new: bool = False

    @property
    def is_empty(self) -> bool:
        return self.value == 0

    def __repr__(self) -> str:
        return f"Tile({self.value} @ ({self.row},{self.col}))"
