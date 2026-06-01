"""JSON save/load system for game state and highscores."""

import json
import os
from typing import Any, Optional


class SaveManager:
    """Manages saving and loading game data."""

    def __init__(self, save_dir: str = "data"):
        self.save_dir = save_dir
        self.save_file = os.path.join(save_dir, "save.json")
        self.highscore_file = os.path.join(save_dir, "highscores.json")
        self.settings_file = os.path.join(save_dir, "settings.json")
        self._ensure_dir()

    def _ensure_dir(self):
        """Ensure save directory exists."""
        os.makedirs(self.save_dir, exist_ok=True)

    def save_game(self, data: dict[str, Any]) -> bool:
        """Save current game state."""
        try:
            with open(self.save_file, "w") as f:
                json.dump(data, f, indent=2)
            return True
        except (IOError, OSError):
            return False

    def load_game(self) -> Optional[dict[str, Any]]:
        """Load saved game state. Returns None if no save exists."""
        if not os.path.exists(self.save_file):
            return None
        try:
            with open(self.save_file, "r") as f:
                return json.load(f)
        except (IOError, json.JSONDecodeError):
            return None

    def delete_save(self) -> bool:
        """Delete the save file."""
        if os.path.exists(self.save_file):
            try:
                os.remove(self.save_file)
                return True
            except OSError:
                return False
        return True

    def has_save(self) -> bool:
        """Check if a save file exists."""
        return os.path.exists(self.save_file)

    def save_highscore(self, score: int, highest_tile: int = 0) -> bool:
        """Save a highscore entry."""
        highscores = self.get_highscores()
        import time
        entry = {
            "score": score,
            "highest_tile": highest_tile,
            "timestamp": time.time(),
        }
        highscores.append(entry)
        highscores.sort(key=lambda x: x["score"], reverse=True)
        highscores = highscores[:10]  # Keep top 10
        try:
            with open(self.highscore_file, "w") as f:
                json.dump(highscores, f, indent=2)
            return True
        except (IOError, OSError):
            return False

    def get_highscores(self) -> list[dict[str, Any]]:
        """Get list of highscores."""
        if not os.path.exists(self.highscore_file):
            return []
        try:
            with open(self.highscore_file, "r") as f:
                return json.load(f)
        except (IOError, json.JSONDecodeError):
            return []

    def get_best_score(self) -> int:
        """Get the highest score."""
        highscores = self.get_highscores()
        return highscores[0]["score"] if highscores else 0

    def save_settings(self, settings: dict[str, Any]) -> bool:
        """Save game settings."""
        try:
            with open(self.settings_file, "w") as f:
                json.dump(settings, f, indent=2)
            return True
        except (IOError, OSError):
            return False

    def load_settings(self) -> dict[str, Any]:
        """Load game settings."""
        if not os.path.exists(self.settings_file):
            return {}
        try:
            with open(self.settings_file, "r") as f:
                return json.load(f)
        except (IOError, json.JSONDecodeError):
            return {}
