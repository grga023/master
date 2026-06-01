"""Main Game class — state machine and game loop."""

import pygame
import sys
from src.constants import WINDOW_WIDTH, WINDOW_HEIGHT, FPS
from src.rendering.renderer import Renderer
from src.systems.save_manager import SaveManager
from src.systems.stats_manager import StatsManager
from src.systems.theme_manager import ThemeManager
from src.systems.audio_manager import AudioManager
from src.states.menu_state import MenuState
from src.states.play_state import PlayState
from src.states.pause_state import PauseState
from src.states.gameover_state import GameOverState
from src.states.victory_state import VictoryState
from src.states.tutorial_state import TutorialState
from src.states.learn_state import LearnState
from src.states.settings_state import SettingsState
from src.states.replay_state import ReplayState
from src.constants import MODE_CLASSIC


class Game:
    """Main game class managing the game loop and state machine."""

    def __init__(self):
        # Display
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("2048")
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_mode = MODE_CLASSIC
        self.last_game_history = None

        # Systems
        self.save_manager = SaveManager()
        self.stats_manager = StatsManager()
        self.theme_manager = ThemeManager()
        self.audio_manager = AudioManager()
        self.renderer = Renderer(self.theme_manager)

        # Load settings
        settings = self.save_manager.load_settings()
        if settings:
            self.theme_manager.load_from_dict(settings.get("theme", {}))
            if settings.get("muted"):
                self.audio_manager.toggle_mute()

        # Load stats
        saved_stats = self.save_manager.load_game()
        if saved_stats and "stats" in saved_stats:
            self.stats_manager.load_from_dict(saved_stats["stats"])

        # State machine
        self.states: dict = {}
        self.state_stack: list = []
        self.current_state = None
        self._init_states()
        self.change_state("menu")

    def _init_states(self):
        """Initialize all game states."""
        self.states = {
            "menu": MenuState(self),
            "play": PlayState(self),
            "pause": PauseState(self),
            "gameover": GameOverState(self),
            "victory": VictoryState(self),
            "tutorial": TutorialState(self),
            "learn": LearnState(self),
            "settings": SettingsState(self),
            "replay": ReplayState(self),
        }

    def change_state(self, state_name: str):
        """Change to a new state, replacing current."""
        if self.current_state:
            self.current_state.exit()
        self.state_stack.clear()
        self.current_state = self.states.get(state_name)
        if self.current_state:
            self.current_state.enter()

    def push_state(self, state_name: str):
        """Push a state on top (overlay)."""
        if self.current_state:
            self.state_stack.append(self.current_state)
        self.current_state = self.states.get(state_name)
        if self.current_state:
            self.current_state.enter()

    def pop_state(self):
        """Pop the current state, return to previous."""
        if self.current_state:
            self.current_state.exit()
        if self.state_stack:
            self.current_state = self.state_stack.pop()
        else:
            self.current_state = self.states.get("menu")
            if self.current_state:
                self.current_state.enter()

    def run(self):
        """Main game loop."""
        self.stats_manager.start_session()

        while self.running:
            dt = self.clock.tick(FPS)  # dt in milliseconds

            # Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    break
                if self.current_state:
                    self.current_state.handle_event(event)

            # Update
            if self.current_state:
                self.current_state.update(dt)

            # Render
            if self.current_state:
                self.current_state.render(self.screen)

            pygame.display.flip()

        # Cleanup
        self.stats_manager.end_session()
        self._save_all()

    def _save_all(self):
        """Save all persistent data."""
        settings = {
            "theme": self.theme_manager.to_dict(),
            "muted": self.audio_manager.muted,
        }
        self.save_manager.save_settings(settings)

    def quit(self):
        """Quit the game."""
        self.running = False
