"""Entry point for the 2048 game."""

import pygame
from src.game import Game


def main():
    """Initialize and run the game."""
    pygame.init()
    pygame.mixer.init()

    game = Game()
    game.run()

    pygame.quit()


if __name__ == "__main__":
    main()
