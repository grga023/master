"""Statistics tracking for game metrics."""

import time
from typing import Any


class StatsManager:
    """Tracks and manages game statistics."""

    def __init__(self):
        self.stats: dict[str, Any] = {
            "games_played": 0,
            "games_won": 0,
            "best_score": 0,
            "highest_tile": 0,
            "total_merges": 0,
            "total_moves": 0,
            "total_play_time": 0.0,
            "current_streak": 0,
            "best_streak": 0,
        }
        self._session_start: float = 0.0
        self._session_active = False

    def start_session(self):
        """Mark the start of a play session."""
        self._session_start = time.time()
        self._session_active = True

    def end_session(self):
        """End the current play session."""
        if self._session_active:
            elapsed = time.time() - self._session_start
            self.stats["total_play_time"] += elapsed
            self._session_active = False

    def record_game_start(self):
        """Record that a new game has started."""
        self.stats["games_played"] += 1

    def record_game_won(self):
        """Record a game win."""
        self.stats["games_won"] += 1
        self.stats["current_streak"] += 1
        self.stats["best_streak"] = max(
            self.stats["best_streak"], self.stats["current_streak"]
        )

    def record_game_lost(self):
        """Record a game loss."""
        self.stats["current_streak"] = 0

    def record_move(self):
        """Record a move was made."""
        self.stats["total_moves"] += 1

    def record_merge(self, count: int = 1):
        """Record merges."""
        self.stats["total_merges"] += count

    def record_score(self, score: int):
        """Update best score if this is higher."""
        self.stats["best_score"] = max(self.stats["best_score"], score)

    def get_best_score(self) -> int:
        """Get the best score achieved."""
        return self.stats["best_score"]

    def set_best_score(self, score: int):
        """Set the best score."""
        self.stats["best_score"] = max(self.stats["best_score"], score)

    def record_tile(self, value: int):
        """Update highest tile if this is higher."""
        self.stats["highest_tile"] = max(self.stats["highest_tile"], value)

    def get_stats(self) -> dict[str, Any]:
        """Get all stats."""
        stats = self.stats.copy()
        if self._session_active:
            stats["total_play_time"] += time.time() - self._session_start
        return stats

    def load_from_dict(self, data: dict[str, Any]):
        """Load stats from a dictionary."""
        for key in self.stats:
            if key in data:
                self.stats[key] = data[key]

    def to_dict(self) -> dict[str, Any]:
        """Export stats to a dictionary."""
        return self.stats.copy()

    @property
    def win_rate(self) -> float:
        """Calculate win rate percentage."""
        if self.stats["games_played"] == 0:
            return 0.0
        return (self.stats["games_won"] / self.stats["games_played"]) * 100
