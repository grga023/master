"""Strategy tips database for 2048."""

from typing import Optional


# Tips categorized by context
BEGINNER_TIPS = [
    "Keep your highest tile in a corner!",
    "Try to build a chain of decreasing values along an edge.",
    "Avoid moving up if your highest tile is in the bottom-left corner.",
    "Focus on keeping one row or column full to maintain control.",
    "Don't chase small merges — think two steps ahead.",
]

INTERMEDIATE_TIPS = [
    "The snake pattern: build values in a zigzag along the edges.",
    "Try to merge tiles in a cascade for combo points.",
    "Keep the board as organized as possible — chaos leads to game over.",
    "When stuck, look for moves that don't displace your largest tile.",
    "Monotonically increasing/decreasing rows are your friend.",
]

ADVANCED_TIPS = [
    "Optimal play reaches 2048 in about 80% of games.",
    "The theoretical maximum tile is 131072 (2^17) on a 4x4 board.",
    "Monotonicity + smoothness + free cells = best heuristic.",
    "Sometimes sacrificing a merge now enables a better one later.",
    "Edge control: keep high values along edges, never in the center.",
]

MATH_FACTS = [
    "2048 = 2^11. Each tile value is a power of 2!",
    "The probability of spawning a 4 is only 10%.",
    "Maximum possible score on 4x4: approximately 3,932,156.",
    "To get 2048, you need at minimum 11 merges of new tiles.",
    "The game board has 16 cells — efficiency is key!",
]

ALL_TIPS = BEGINNER_TIPS + INTERMEDIATE_TIPS + ADVANCED_TIPS + MATH_FACTS


def get_tip_for_context(score: int = 0, highest_tile: int = 0,
                        moves_made: int = 0) -> str:
    """Get a contextually appropriate tip."""
    import random

    if moves_made < 20:
        pool = BEGINNER_TIPS
    elif highest_tile < 256:
        pool = BEGINNER_TIPS + INTERMEDIATE_TIPS
    elif highest_tile < 1024:
        pool = INTERMEDIATE_TIPS + ADVANCED_TIPS
    else:
        pool = ADVANCED_TIPS + MATH_FACTS

    return random.choice(pool)


def get_random_tip() -> str:
    """Get a random tip from all categories."""
    import random
    return random.choice(ALL_TIPS)


def get_math_fact() -> str:
    """Get a random math fact."""
    import random
    return random.choice(MATH_FACTS)
