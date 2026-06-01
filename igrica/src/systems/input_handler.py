"""Keyboard and mouse input processing."""

import pygame
from typing import Optional


class InputHandler:
    """Processes pygame events and maps them to game actions."""

    # Key mappings for movement
    MOVE_KEYS = {
        pygame.K_UP: "up",
        pygame.K_DOWN: "down",
        pygame.K_LEFT: "left",
        pygame.K_RIGHT: "right",
        pygame.K_w: "up",
        pygame.K_s: "down",
        pygame.K_a: "left",
        pygame.K_d: "right",
    }

    def __init__(self):
        self.blocked = False
        self._queued_direction: Optional[str] = None
        self._last_direction: Optional[str] = None

    @property
    def queued_direction(self) -> Optional[str]:
        """Get and consume the queued direction."""
        direction = self._queued_direction
        self._queued_direction = None
        return direction

    def process_event(self, event: pygame.event.Event) -> Optional[str]:
        """Process a single event. Returns action string or None.
        
        Actions: "move_up", "move_down", "move_left", "move_right",
                 "undo", "pause", "quit", "restart", "escape"
        """
        if event.type == pygame.KEYDOWN:
            # Movement keys
            if event.key in self.MOVE_KEYS:
                direction = self.MOVE_KEYS[event.key]
                if self.blocked:
                    self._queued_direction = direction
                    return None
                self._last_direction = direction
                return f"move_{direction}"

            # Other actions
            if event.key == pygame.K_u or (event.key == pygame.K_z and event.mod & pygame.KMOD_CTRL):
                return "undo"
            if event.key == pygame.K_p:
                return "pause"
            if event.key == pygame.K_r:
                return "restart"
            if event.key == pygame.K_ESCAPE:
                return "escape"
            if event.key == pygame.K_n:
                return "new_game"

        return None

    def block(self):
        """Block input (during animations)."""
        self.blocked = True

    def unblock(self):
        """Unblock input after animations complete."""
        self.blocked = False

    def reset(self):
        """Reset input state."""
        self.blocked = False
        self._queued_direction = None
        self._last_direction = None
