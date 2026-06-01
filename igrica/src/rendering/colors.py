"""Color utilities and palette helpers."""

from typing import Optional


def lerp_color(color1: tuple[int, int, int], color2: tuple[int, int, int],
               t: float) -> tuple[int, int, int]:
    """Linear interpolation between two colors."""
    t = max(0.0, min(1.0, t))
    return (
        int(color1[0] + (color2[0] - color1[0]) * t),
        int(color1[1] + (color2[1] - color1[1]) * t),
        int(color1[2] + (color2[2] - color1[2]) * t),
    )


def darken(color: tuple[int, int, int], amount: float = 0.2) -> tuple[int, int, int]:
    """Darken a color by a percentage."""
    return (
        int(color[0] * (1 - amount)),
        int(color[1] * (1 - amount)),
        int(color[2] * (1 - amount)),
    )


def lighten(color: tuple[int, int, int], amount: float = 0.2) -> tuple[int, int, int]:
    """Lighten a color by a percentage."""
    return (
        min(255, int(color[0] + (255 - color[0]) * amount)),
        min(255, int(color[1] + (255 - color[1]) * amount)),
        min(255, int(color[2] + (255 - color[2]) * amount)),
    )


def with_alpha(color: tuple[int, int, int], alpha: int) -> tuple[int, int, int, int]:
    """Add alpha channel to a color."""
    return (color[0], color[1], color[2], alpha)


def get_particle_color(tile_value: int) -> tuple[int, int, int]:
    """Get a particle color based on the tile that was merged."""
    from src.constants import TILE_COLORS
    base = TILE_COLORS.get(tile_value, (237, 194, 46))
    return lighten(base, 0.3)
