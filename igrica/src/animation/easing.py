"""Easing functions for animations."""

import math


def linear(t: float) -> float:
    """Linear interpolation (no easing)."""
    return t


def ease_out_quad(t: float) -> float:
    """Quadratic ease out - decelerating."""
    return 1 - (1 - t) * (1 - t)


def ease_in_quad(t: float) -> float:
    """Quadratic ease in - accelerating."""
    return t * t


def ease_in_out_quad(t: float) -> float:
    """Quadratic ease in/out."""
    if t < 0.5:
        return 2 * t * t
    else:
        return 1 - (-2 * t + 2) ** 2 / 2


def ease_out_back(t: float) -> float:
    """Overshoot ease out - slight bounce past target."""
    c1 = 1.70158
    c3 = c1 + 1
    return 1 + c3 * (t - 1) ** 3 + c1 * (t - 1) ** 2


def ease_out_elastic(t: float) -> float:
    """Elastic ease out - spring-like bounce."""
    if t == 0 or t == 1:
        return t
    c4 = (2 * math.pi) / 3
    return 2 ** (-10 * t) * math.sin((t * 10 - 0.75) * c4) + 1


def ease_out_bounce(t: float) -> float:
    """Bounce ease out."""
    n1 = 7.5625
    d1 = 2.75
    if t < 1 / d1:
        return n1 * t * t
    elif t < 2 / d1:
        t -= 1.5 / d1
        return n1 * t * t + 0.75
    elif t < 2.5 / d1:
        t -= 2.25 / d1
        return n1 * t * t + 0.9375
    else:
        t -= 2.625 / d1
        return n1 * t * t + 0.984375


def ease_out_cubic(t: float) -> float:
    """Cubic ease out."""
    return 1 - (1 - t) ** 3
