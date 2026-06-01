"""Data classes representing the result of a board move."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Tuple


@dataclass
class TileMovement:
    """Represents a tile sliding from one position to another."""
    from_pos: Tuple[int, int]  # (row, col)
    to_pos: Tuple[int, int]
    value: int


@dataclass
class TileMerge:
    """Represents two tiles merging into one."""
    pos: Tuple[int, int]  # final position
    new_value: int


@dataclass
class MoveResult:
    """Complete result of a move operation."""
    movements: List[TileMovement] = field(default_factory=list)
    merges: List[TileMerge] = field(default_factory=list)
    score_gained: int = 0
    board_changed: bool = False
    new_tile_pos: Optional[Tuple[int, int]] = None
