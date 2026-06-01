"""Educational math overlay showing powers of 2 and probability info."""

import pygame
from typing import Optional


class MathOverlay:
    """Generates and displays educational math content."""

    # Powers of 2 reference
    POWERS_OF_2 = {i: 2**i for i in range(1, 18)}

    def __init__(self):
        self.visible = False
        self.content_type = "powers"  # "powers", "probability", "score"

    def toggle(self):
        """Toggle overlay visibility."""
        self.visible = not self.visible

    def get_power_info(self, value: int) -> str:
        """Get the power-of-2 representation of a value."""
        if value <= 0:
            return ""
        power = 0
        v = value
        while v > 1:
            v //= 2
            power += 1
        return f"2^{power} = {value}"

    def get_spawn_probability_text(self) -> list[str]:
        """Get spawn probability information."""
        return [
            "Tile Spawn Probabilities:",
            "  Value 2: 90% chance",
            "  Value 4: 10% chance",
            "",
            "Spawn Location:",
            "  Random empty cell",
            "  (uniform distribution)",
        ]

    def get_merge_tree(self, target: int = 2048) -> list[str]:
        """Generate a simple merge tree text representation."""
        lines = [f"How to reach {target}:"]
        value = target
        depth = 0
        while value > 2:
            half = value // 2
            indent = "  " * depth
            lines.append(f"{indent}{value} = {half} + {half}")
            value = half
            depth += 1
        return lines

    def get_score_math(self, merges: list[int]) -> list[str]:
        """Explain how score is calculated from merges."""
        lines = ["Score Calculation:"]
        total = 0
        for merge_value in merges[-5:]:  # Show last 5
            lines.append(f"  Merge → {merge_value} (+{merge_value} pts)")
            total += merge_value
        lines.append(f"  Recent total: +{total}")
        return lines

    def render(self, surface: pygame.Surface, font: pygame.font.Font,
               board_values: Optional[list[list[int]]] = None):
        """Render the math overlay."""
        if not self.visible:
            return

        # Semi-transparent background
        overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        surface.blit(overlay, (0, 0))

        # Content based on type
        if self.content_type == "powers":
            lines = self.get_merge_tree()
        elif self.content_type == "probability":
            lines = self.get_spawn_probability_text()
        else:
            lines = self.get_merge_tree()

        y = 100
        title_color = (237, 194, 46)
        text_color = (249, 246, 242)

        for i, line in enumerate(lines):
            color = title_color if i == 0 else text_color
            text_surf = font.render(line, True, color)
            surface.blit(text_surf, (50, y))
            y += 30

        # Instructions
        hint = font.render("Press M to close", True, (180, 180, 180))
        surface.blit(hint, (50, surface.get_height() - 50))

    def cycle_content(self):
        """Cycle through content types."""
        types = ["powers", "probability", "score"]
        idx = types.index(self.content_type)
        self.content_type = types[(idx + 1) % len(types)]
