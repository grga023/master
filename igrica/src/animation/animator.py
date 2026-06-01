"""Animation manager that coordinates all active tweens and animations."""

from typing import Optional, Callable
from .tween import Tween
from .easing import ease_out_quad, ease_out_back, ease_out_cubic


class Animation:
    """A named animation containing one or more tweens."""

    def __init__(self, name: str, on_complete: Optional[Callable] = None):
        self.name = name
        self.tweens: dict[str, Tween] = {}
        self.on_complete = on_complete
        self.completed = False

    def add_tween(self, key: str, tween: Tween):
        """Add a tween to this animation."""
        self.tweens[key] = tween

    def get_value(self, key: str) -> float:
        """Get current value of a tween by key."""
        if key in self.tweens:
            return self.tweens[key].value
        return 0.0

    def update(self, dt_ms: float) -> bool:
        """Update all tweens. Returns True if any are still active."""
        any_active = False
        for tween in self.tweens.values():
            if tween.update(dt_ms):
                any_active = True

        if not any_active and not self.completed:
            self.completed = True
            if self.on_complete:
                self.on_complete()

        return any_active


class Animator:
    """Manages all active animations."""

    def __init__(self):
        self.animations: dict[str, Animation] = {}
        self._on_all_complete: Optional[Callable] = None

    @property
    def is_animating(self) -> bool:
        """True if any animations are still running."""
        return any(not a.completed for a in self.animations.values())

    def add(self, animation: Animation):
        """Add an animation to the manager."""
        self.animations[animation.name] = animation

    def create_slide(self, tile_id: str, start_x: float, start_y: float,
                     end_x: float, end_y: float, duration_ms: float,
                     on_complete: Optional[Callable] = None) -> Animation:
        """Create a slide animation for a tile."""
        anim = Animation(f"slide_{tile_id}", on_complete=on_complete)
        anim.add_tween("x", Tween(start_x, end_x, duration_ms, ease_out_quad))
        anim.add_tween("y", Tween(start_y, end_y, duration_ms, ease_out_quad))
        self.add(anim)
        return anim

    def create_merge(self, tile_id: str, duration_ms: float,
                     on_complete: Optional[Callable] = None) -> Animation:
        """Create a merge (pop) animation for a tile."""
        anim = Animation(f"merge_{tile_id}", on_complete=on_complete)
        anim.add_tween("scale", Tween(0.0, 1.0, duration_ms, ease_out_back))
        self.add(anim)
        return anim

    def create_spawn(self, tile_id: str, duration_ms: float,
                     on_complete: Optional[Callable] = None) -> Animation:
        """Create a spawn (appear) animation for a tile."""
        anim = Animation(f"spawn_{tile_id}", on_complete=on_complete)
        anim.add_tween("scale", Tween(0.0, 1.0, duration_ms, ease_out_back))
        anim.add_tween("alpha", Tween(0.0, 255.0, duration_ms, ease_out_cubic))
        self.add(anim)
        return anim

    def get_animation(self, name: str) -> Optional[Animation]:
        """Get an animation by name."""
        return self.animations.get(name)

    def update(self, dt_ms: float):
        """Update all animations."""
        completed = []
        for name, anim in self.animations.items():
            if not anim.update(dt_ms):
                completed.append(name)

        # Clean up completed animations
        for name in completed:
            del self.animations[name]

        # Check if all done
        if not self.animations and self._on_all_complete:
            callback = self._on_all_complete
            self._on_all_complete = None
            callback()

    def on_all_complete(self, callback: Callable):
        """Set callback for when all animations finish."""
        if not self.animations:
            callback()
        else:
            self._on_all_complete = callback

    def clear(self):
        """Remove all animations."""
        self.animations.clear()
        self._on_all_complete = None
