"""Records game history for replay functionality."""
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class HistoryEntry:
    """A single recorded move in game history."""
    grid: list  # board snapshot BEFORE the move
    direction: str
    score_before: int
    score_after: int
    move_num: int
    max_tile: int
    is_milestone: bool = False  # True if max_tile increased this move


class GameHistory:
    """Records all moves during a game for replay."""

    def __init__(self):
        self.entries: list[HistoryEntry] = []
        self._prev_max_tile = 0

    def record(self, grid: list, direction: str, score_before: int,
               score_after: int, move_num: int):
        """Record a move. Grid should be the state BEFORE the move."""
        grid_copy = [row[:] for row in grid]
        max_tile = max(max(row) for row in grid_copy) if grid_copy else 0
        is_milestone = max_tile > self._prev_max_tile
        
        self.entries.append(HistoryEntry(
            grid=grid_copy,
            direction=direction,
            score_before=score_before,
            score_after=score_after,
            move_num=move_num,
            max_tile=max_tile,
            is_milestone=is_milestone,
        ))
        
        if is_milestone:
            self._prev_max_tile = max_tile

    def get_entries(self) -> list:
        return self.entries

    def get_milestones(self) -> list:
        return [e for e in self.entries if e.is_milestone]

    def clear(self):
        self.entries = []
        self._prev_max_tile = 0

    @property
    def total_moves(self) -> int:
        return len(self.entries)
