"""Abstract base class for game states."""

from abc import ABC, abstractmethod
import pygame


class BaseState(ABC):
    """Base class for all game states."""

    def __init__(self, game):
        """Initialize state with reference to the game instance."""
        self.game = game

    def enter(self):
        """Called when state becomes active."""
        pass

    def exit(self):
        """Called when state is deactivated."""
        pass

    @abstractmethod
    def handle_event(self, event: pygame.event.Event):
        """Handle a pygame event."""
        pass

    @abstractmethod
    def update(self, dt: float):
        """Update state logic. dt is in milliseconds."""
        pass

    @abstractmethod
    def render(self, surface: pygame.Surface):
        """Render the state to the surface."""
        pass
