"""Progress Tree widget showing merge tier visualization."""
import pygame
import math


class ProgressTree:
    """Visual tree showing progress toward the goal tile."""

    def __init__(self, mode: str = "classic"):
        self.mode = mode
        if mode == "fibonacci":
            self.tiers = [1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610]
        else:
            self.tiers = [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048]
        
        self.max_reached = 0
        self.glow_timer = 0.0
        self.font = pygame.font.Font(None, 22)
        self.title_font = pygame.font.Font(None, 28)
        self.small_font = pygame.font.Font(None, 18)

    def update(self, dt_ms: float, grid: list):
        """Update max reached tile and glow animation."""
        self.glow_timer += dt_ms
        max_tile = max(max(row) for row in grid) if grid else 0
        if max_tile > self.max_reached:
            self.max_reached = max_tile

    def render(self, surface: pygame.Surface, x: int, y: int, width: int, height: int):
        """Render the progress tree in the given area."""
        # Title
        title = "Progress" if self.mode == "classic" else "Fibonacci Progress"
        title_surf = self.title_font.render(title, True, (119, 110, 101))
        surface.blit(title_surf, (x + 10, y))

        # Calculate tier display
        tier_height = min(35, (height - 80) // len(self.tiers))
        start_y = y + 40
        
        # Find frontier (highest tier reached)
        frontier_idx = -1
        for i, tier in enumerate(self.tiers):
            if tier <= self.max_reached:
                frontier_idx = i

        # Progress info
        reached_count = frontier_idx + 1 if frontier_idx >= 0 else 0
        total_tiers = len(self.tiers)
        progress_pct = int((reached_count / total_tiers) * 100)
        
        pct_text = f"{progress_pct}% ({reached_count}/{total_tiers})"
        pct_surf = self.small_font.render(pct_text, True, (119, 110, 101))
        surface.blit(pct_surf, (x + 10, y + 22))

        # Render tiers from top (highest) to bottom (lowest)
        for i, tier in enumerate(reversed(self.tiers)):
            tier_idx = len(self.tiers) - 1 - i
            ty = start_y + i * tier_height
            
            reached = tier <= self.max_reached
            is_frontier = tier_idx == frontier_idx
            
            # Background box
            box_rect = pygame.Rect(x + 10, ty, width - 20, tier_height - 4)
            
            if reached:
                color = (143, 195, 143)  # green-ish
                if is_frontier:
                    # Animated glow
                    glow = int(abs(math.sin(self.glow_timer / 500.0)) * 40)
                    color = (100 + glow, 200 + glow // 2, 100 + glow)
            else:
                color = (220, 220, 220)  # gray
            
            pygame.draw.rect(surface, color, box_rect, border_radius=4)
            
            # Tier value text
            text = str(tier)
            if is_frontier:
                text += " <- YOU"
            elif tier == self.tiers[-1]:
                text += " (GOAL)"
                
            text_surf = self.font.render(text, True, (60, 60, 60) if reached else (160, 160, 160))
            text_rect = text_surf.get_rect(midleft=(x + 18, ty + tier_height // 2 - 2))
            surface.blit(text_surf, text_rect)
            
            # Checkmark for reached
            if reached:
                check_surf = self.font.render("v", True, (40, 120, 40))
                surface.blit(check_surf, (x + width - 35, ty + 2))

        # "Merges away" info at bottom
        if frontier_idx < total_tiers - 1:
            remaining = total_tiers - reached_count
            goal_text = f"{remaining} tiers to goal!"
            goal_surf = self.small_font.render(goal_text, True, (119, 110, 101))
            surface.blit(goal_surf, (x + 10, start_y + len(self.tiers) * tier_height + 5))
