"""Hint system that suggests optimal moves using heuristics."""

from typing import Optional
import copy


class HintSystem:
    """Evaluates board positions and suggests the best move."""

    # Weights for the evaluation heuristic
    WEIGHTS = {
        "monotonicity": 1.0,
        "smoothness": 0.5,
        "free_cells": 2.7,
        "max_tile": 1.0,
        "corner_bonus": 1.5,
    }

    def __init__(self):
        self.last_hint: Optional[str] = None
        self.hint_count = 0

    def get_best_move(self, grid: list[list[int]], size: int = 4) -> Optional[str]:
        """Evaluate all 4 moves and return the best direction."""
        directions = ["up", "down", "left", "right"]
        best_score = float("-inf")
        best_dir = None

        for direction in directions:
            # Simulate the move
            new_grid, score_gained, changed = self._simulate_move(grid, direction, size)
            if not changed:
                continue

            # Evaluate the resulting position
            eval_score = self._evaluate(new_grid, size) + score_gained * 0.1
            if eval_score > best_score:
                best_score = eval_score
                best_dir = direction

        self.last_hint = best_dir
        if best_dir:
            self.hint_count += 1
        return best_dir

    def get_hint_explanation(self, grid: list[list[int]], size: int = 4) -> str:
        """Get an explanation of why a move is recommended."""
        direction = self.get_best_move(grid, size)
        if not direction:
            return "No good moves available."

        explanations = {
            "up": "Moving up keeps your structure organized.",
            "down": "Moving down builds toward your corner strategy.",
            "left": "Moving left maintains your edge chain.",
            "right": "Moving right aligns tiles for merges.",
        }
        return f"Hint: Move {direction}. {explanations.get(direction, '')}"

    def _evaluate(self, grid: list[list[int]], size: int) -> float:
        """Evaluate a board position using multiple heuristics."""
        score = 0.0
        score += self._monotonicity(grid, size) * self.WEIGHTS["monotonicity"]
        score += self._smoothness(grid, size) * self.WEIGHTS["smoothness"]
        score += self._free_cells(grid, size) * self.WEIGHTS["free_cells"]
        score += self._max_tile_score(grid, size) * self.WEIGHTS["max_tile"]
        score += self._corner_bonus(grid, size) * self.WEIGHTS["corner_bonus"]
        return score

    def _monotonicity(self, grid: list[list[int]], size: int) -> float:
        """Evaluate how monotonically ordered the grid is."""
        score = 0.0
        for row in grid:
            for i in range(len(row) - 1):
                if row[i] >= row[i + 1]:
                    score += 1
                if row[i] <= row[i + 1]:
                    score += 1
        for col in range(size):
            for row in range(size - 1):
                if grid[row][col] >= grid[row + 1][col]:
                    score += 1
                if grid[row][col] <= grid[row + 1][col]:
                    score += 1
        return score

    def _smoothness(self, grid: list[list[int]], size: int) -> float:
        """Evaluate how similar adjacent tiles are (lower diff = smoother)."""
        score = 0.0
        for r in range(size):
            for c in range(size):
                if grid[r][c] == 0:
                    continue
                # Check right neighbor
                if c + 1 < size and grid[r][c + 1] != 0:
                    diff = abs(grid[r][c] - grid[r][c + 1])
                    score -= diff
                # Check bottom neighbor
                if r + 1 < size and grid[r + 1][c] != 0:
                    diff = abs(grid[r][c] - grid[r + 1][c])
                    score -= diff
        return score / 100.0

    def _free_cells(self, grid: list[list[int]], size: int) -> float:
        """Count free cells (more = better)."""
        count = sum(1 for r in range(size) for c in range(size) if grid[r][c] == 0)
        return float(count)

    def _max_tile_score(self, grid: list[list[int]], size: int) -> float:
        """Bonus for having a high max tile."""
        max_val = max(grid[r][c] for r in range(size) for c in range(size))
        return max_val / 100.0

    def _corner_bonus(self, grid: list[list[int]], size: int) -> float:
        """Bonus if the max tile is in a corner."""
        max_val = max(grid[r][c] for r in range(size) for c in range(size))
        corners = [
            grid[0][0], grid[0][size - 1],
            grid[size - 1][0], grid[size - 1][size - 1]
        ]
        if max_val in corners:
            return max_val / 50.0
        return 0.0

    def _simulate_move(self, grid: list[list[int]], direction: str,
                       size: int) -> tuple[list[list[int]], int, bool]:
        """Simulate a move and return (new_grid, score, changed)."""
        # Deep copy
        new_grid = [row[:] for row in grid]

        # Rotate to normalize to left
        if direction == "right":
            new_grid = [row[::-1] for row in new_grid]
        elif direction == "up":
            new_grid = self._transpose(new_grid, size)
        elif direction == "down":
            new_grid = self._transpose(new_grid, size)
            new_grid = [row[::-1] for row in new_grid]

        # Slide left
        total_score = 0
        for i in range(size):
            new_grid[i], score = self._slide_row_left(new_grid[i], size)
            total_score += score

        # Rotate back
        if direction == "right":
            new_grid = [row[::-1] for row in new_grid]
        elif direction == "up":
            new_grid = self._transpose(new_grid, size)
        elif direction == "down":
            new_grid = [row[::-1] for row in new_grid]
            new_grid = self._transpose(new_grid, size)

        changed = new_grid != grid
        return new_grid, total_score, changed

    def _slide_row_left(self, row: list[int], size: int) -> tuple[list[int], int]:
        """Slide a row left with merging."""
        non_zero = [x for x in row if x != 0]
        merged = []
        skip = False
        score = 0
        for i in range(len(non_zero)):
            if skip:
                skip = False
                continue
            if i + 1 < len(non_zero) and non_zero[i] == non_zero[i + 1]:
                merged.append(non_zero[i] * 2)
                score += non_zero[i] * 2
                skip = True
            else:
                merged.append(non_zero[i])
        merged += [0] * (size - len(merged))
        return merged, score

    def _transpose(self, grid: list[list[int]], size: int) -> list[list[int]]:
        """Transpose a grid."""
        return [[grid[r][c] for r in range(size)] for c in range(size)]
