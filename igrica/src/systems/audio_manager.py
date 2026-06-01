"""Sound effects and music management."""

import os
import pygame
from typing import Optional


class AudioManager:
    """Manages game audio including sound effects and music."""

    def __init__(self, sounds_dir: str = "assets/sounds"):
        self.sounds_dir = sounds_dir
        self.sounds: dict[str, Optional[pygame.mixer.Sound]] = {}
        self.music_playing = False
        self.muted = False
        self.sfx_volume = 0.7
        self.music_volume = 0.3
        self._initialized = False
        self._init_audio()

    def _init_audio(self):
        """Initialize the audio system."""
        try:
            if pygame.mixer.get_init():
                self._initialized = True
        except Exception:
            self._initialized = False

    def load_sound(self, name: str, filename: str) -> bool:
        """Load a sound effect from file."""
        if not self._initialized:
            return False
        path = os.path.join(self.sounds_dir, filename)
        if os.path.exists(path):
            try:
                self.sounds[name] = pygame.mixer.Sound(path)
                self.sounds[name].set_volume(self.sfx_volume)
                return True
            except Exception:
                pass
        self.sounds[name] = None
        return False

    def play_sfx(self, name: str):
        """Play a sound effect by name."""
        if self.muted or not self._initialized:
            return
        sound = self.sounds.get(name)
        if sound:
            sound.play()

    def play_music(self, filename: str = "background.ogg", loop: bool = True):
        """Start playing background music."""
        if not self._initialized:
            return
        path = os.path.join(self.sounds_dir, filename)
        if os.path.exists(path):
            try:
                pygame.mixer.music.load(path)
                pygame.mixer.music.set_volume(self.music_volume)
                pygame.mixer.music.play(-1 if loop else 0)
                self.music_playing = True
            except Exception:
                pass

    def stop_music(self):
        """Stop background music."""
        if self._initialized:
            try:
                pygame.mixer.music.stop()
                self.music_playing = False
            except Exception:
                pass

    def set_volume(self, volume: float):
        """Set master volume (0.0 to 1.0)."""
        self.sfx_volume = max(0.0, min(1.0, volume))
        self.music_volume = max(0.0, min(1.0, volume * 0.5))
        for sound in self.sounds.values():
            if sound:
                sound.set_volume(self.sfx_volume)
        if self._initialized:
            try:
                pygame.mixer.music.set_volume(self.music_volume)
            except Exception:
                pass

    def toggle_mute(self) -> bool:
        """Toggle mute state. Returns new mute state."""
        self.muted = not self.muted
        if self.muted:
            if self._initialized:
                try:
                    pygame.mixer.music.set_volume(0)
                except Exception:
                    pass
        else:
            if self._initialized:
                try:
                    pygame.mixer.music.set_volume(self.music_volume)
                except Exception:
                    pass
        return self.muted
