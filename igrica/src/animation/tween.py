"""Tween class for value interpolation over time."""

from typing import Callable, Optional
from . import easing as easing_module


class Tween:
    """Interpolates a value from start to end over a duration using an easing function."""

    def __init__(
        self,
        start: float,
        end: float,
        duration_ms: float,
        easing_fn: Callable[[float], float] = None,
        on_complete: Optional[Callable] = None,
        delay_ms: float = 0,
    ):
        self.start = start
        self.end = end
        self.duration_ms = max(1, duration_ms)
        self.easing_fn = easing_fn or easing_module.linear
        self.on_complete = on_complete
        self.delay_ms = delay_ms
        self.elapsed_ms = 0.0
        self.completed = False
        self._value = start

    @property
    def value(self) -> float:
        """Current interpolated value."""
        return self._value

    @property
    def progress(self) -> float:
        """Raw progress 0..1 without easing."""
        if self.elapsed_ms < self.delay_ms:
            return 0.0
        active_time = self.elapsed_ms - self.delay_ms
        return min(1.0, active_time / self.duration_ms)

    def update(self, dt_ms: float) -> bool:
        """Update tween by dt milliseconds. Returns True if still active."""
        if self.completed:
            return False

        self.elapsed_ms += dt_ms

        if self.elapsed_ms < self.delay_ms:
            self._value = self.start
            return True

        t = self.progress
        eased_t = self.easing_fn(t)
        self._value = self.start + (self.end - self.start) * eased_t

        if t >= 1.0:
            self._value = self.end
            self.completed = True
            if self.on_complete:
                self.on_complete()
            return False

        return True

    def reset(self):
        """Reset tween to beginning."""
        self.elapsed_ms = 0.0
        self.completed = False
        self._value = self.start
