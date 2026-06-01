"""Particle system for merge effects."""

import random
import math
from typing import Optional
import pygame


class Particle:
    """A single particle with position, velocity, color, and lifetime."""

    def __init__(self, x: float, y: float, color: tuple[int, int, int],
                 speed: float = 100.0, lifetime_ms: float = 400.0):
        self.x = x
        self.y = y
        self.color = color
        angle = random.uniform(0, 2 * math.pi)
        self.vx = math.cos(angle) * speed * random.uniform(0.5, 1.5)
        self.vy = math.sin(angle) * speed * random.uniform(0.5, 1.5)
        self.lifetime_ms = lifetime_ms
        self.elapsed_ms = 0.0
        self.alpha = 255.0
        self.size = random.uniform(3.0, 8.0)
        self.alive = True

    @property
    def progress(self) -> float:
        return min(1.0, self.elapsed_ms / self.lifetime_ms)

    def update(self, dt_ms: float):
        """Update particle position and state."""
        if not self.alive:
            return
        self.elapsed_ms += dt_ms
        dt_sec = dt_ms / 1000.0
        self.x += self.vx * dt_sec
        self.y += self.vy * dt_sec
        # Slow down
        self.vx *= 0.95
        self.vy *= 0.95
        # Fade out
        self.alpha = 255.0 * (1.0 - self.progress)
        self.size *= 0.98
        if self.progress >= 1.0:
            self.alive = False

    def render(self, surface: pygame.Surface):
        """Draw the particle."""
        if not self.alive or self.alpha <= 0:
            return
        s = max(1, int(self.size))
        particle_surf = pygame.Surface((s * 2, s * 2), pygame.SRCALPHA)
        color_with_alpha = (*self.color, int(self.alpha))
        pygame.draw.circle(particle_surf, color_with_alpha, (s, s), s)
        surface.blit(particle_surf, (int(self.x) - s, int(self.y) - s))


class ParticleSystem:
    """Manages collections of particles for visual effects."""

    def __init__(self):
        self.particles: list[Particle] = []

    def emit(self, x: float, y: float, color: tuple[int, int, int],
             count: int = 12, speed: float = 100.0, lifetime_ms: float = 400.0):
        """Emit particles at a position."""
        for _ in range(count):
            self.particles.append(Particle(x, y, color, speed, lifetime_ms))

    def update(self, dt_ms: float):
        """Update all particles and remove dead ones."""
        for p in self.particles:
            p.update(dt_ms)
        self.particles = [p for p in self.particles if p.alive]

    def render(self, surface: pygame.Surface):
        """Render all active particles."""
        for p in self.particles:
            p.render(surface)

    @property
    def is_active(self) -> bool:
        """True if there are living particles."""
        return len(self.particles) > 0

    def clear(self):
        """Remove all particles."""
        self.particles.clear()
