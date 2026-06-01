"""Board logic for the 2048 game."""

from __future__ import annotations

import copy
import random
from typing import List, Optional, Tuple

from .move_result import MoveResult, TileMerge, TileMovement


class Board:
    """Represents the 2048 game board and handles move logic."""

    def __init__(self, size: int = 4):
        self.size = size
        self.grid: List[List[int]] = [[0] * size for _ in range(size)]

    def move(self, direction: str) -> MoveResult:
        """Process a move in the given direction.

        Normalizes all directions to a left-slide by rotating the grid,
        then rotates back. Tracks tile movements and merges with correct
        positions accounting for rotations.
        """
        old_grid = [row[:] for row in self.grid]

        # Determine CW rotations needed to normalize direction to "left"
        rotations_before = {"left": 0, "right": 2, "up": 3, "down": 1}
        rotations_after = {"left": 0, "right": 2, "up": 1, "down": 3}

        n_before = rotations_before[direction]
        n_after = rotations_after[direction]

        # Rotate grid so we can always slide left
        working = [row[:] for row in self.grid]
        for _ in range(n_before):
            working = self._rotate_90_cw(working)

        # Slide each row left and collect movements/merges in rotated space
        all_movements: list[TileMovement] = []
        all_merges: list[TileMerge] = []
        total_score = 0

        for r in range(self.size):
            new_row, score, movements, merges = self._slide_row_left(working[r], r)
            working[r] = new_row
            total_score += score
            all_movements.extend(movements)
            all_merges.extend(merges)

        # Rotate grid back
        for _ in range(n_after):
            working = self._rotate_90_cw(working)

        # Transform movement/merge positions back from rotated space
        transformed_movements = []
        for m in all_movements:
            from_pos = self._unrotate_pos(m.from_pos, n_before)
            to_pos = self._unrotate_pos(m.to_pos, n_before)
            transformed_movements.append(TileMovement(from_pos, to_pos, m.value))

        transformed_merges = []
        for mg in all_merges:
            pos = self._unrotate_pos(mg.pos, n_before)
            transformed_merges.append(TileMerge(pos, mg.new_value))

        board_changed = working != old_grid
        self.grid = working

        return MoveResult(
            movements=transformed_movements,
            merges=transformed_merges,
            score_gained=total_score,
            board_changed=board_changed,
        )

    def spawn_tile(self) -> Optional[Tuple[int, int]]:
        """Place a 2 (90% chance) or 4 (10% chance) on a random empty cell."""
        empty = self.get_empty_cells()
        if not empty:
            return None
        row, col = random.choice(empty)
        self.grid[row][col] = 2 if random.random() < 0.9 else 4
        return (row, col)

    def can_move(self) -> bool:
        """Check if any valid move exists."""
        if self.get_empty_cells():
            return True
        # Check for adjacent equal tiles
        for r in range(self.size):
            for c in range(self.size):
                val = self.grid[r][c]
                if c + 1 < self.size and self.grid[r][c + 1] == val:
                    return True
                if r + 1 < self.size and self.grid[r + 1][c] == val:
                    return True
        return False

    def has_won(self) -> bool:
        """Check if any cell has reached 2048."""
        for row in self.grid:
            for val in row:
                if val >= 2048:
                    return True
        return False

    def clone(self) -> "Board":
        """Return a deep copy of this board."""
        new_board = Board(self.size)
        new_board.grid = copy.deepcopy(self.grid)
        return new_board

    def get_empty_cells(self) -> List[Tuple[int, int]]:
        """Return positions of all empty cells."""
        return [
            (r, c)
            for r in range(self.size)
            for c in range(self.size)
            if self.grid[r][c] == 0
        ]

    def _slide_row_left(
        self, row: List[int], row_idx: int
    ) -> Tuple[List[int], int, List[TileMovement], List[TileMerge]]:
        """Slide a row left: compress, merge, compress.

        Returns (new_row, score, movements, merges) where positions are
        in the rotated coordinate space (row_idx, col).
        """
        movements: list[TileMovement] = []
        merges: list[TileMerge] = []

        # Collect non-zero tiles with their original columns
        non_zero = [(val, col) for col, val in enumerate(row) if val != 0]

        merged: list[int] = []
        score = 0
        skip = False
        dest_col = 0

        for i in range(len(non_zero)):
            if skip:
                skip = False
                dest_col += 1
                continue

            val, orig_col = non_zero[i]

            if i + 1 < len(non_zero) and non_zero[i][0] == non_zero[i + 1][0]:
                # Merge: both tiles move to dest_col
                val2, orig_col2 = non_zero[i + 1]
                new_val = val * 2
                merged.append(new_val)
                score += new_val
                skip = True

                movements.append(TileMovement(
                    from_pos=(row_idx, orig_col),
                    to_pos=(row_idx, dest_col),
                    value=val,
                ))
                movements.append(TileMovement(
                    from_pos=(row_idx, orig_col2),
                    to_pos=(row_idx, dest_col),
                    value=val2,
                ))
                merges.append(TileMerge(
                    pos=(row_idx, dest_col),
                    new_value=new_val,
                ))
            else:
                # Simple slide
                merged.append(val)
                if orig_col != dest_col:
                    movements.append(TileMovement(
                        from_pos=(row_idx, orig_col),
                        to_pos=(row_idx, dest_col),
                        value=val,
                    ))

            dest_col += 1

        merged += [0] * (self.size - len(merged))
        return merged, score, movements, merges

    def _rotate_90_cw(self, grid: List[List[int]]) -> List[List[int]]:
        """Rotate grid 90 degrees clockwise."""
        n = len(grid)
        return [[grid[n - 1 - j][i] for j in range(n)] for i in range(n)]

    def _rotate_90_ccw(self, grid: List[List[int]]) -> List[List[int]]:
        """Rotate grid 90 degrees counter-clockwise."""
        n = len(grid)
        return [[grid[j][n - 1 - i] for j in range(n)] for i in range(n)]

    def _unrotate_pos(self, pos: Tuple[int, int], n_rotations_cw: int) -> Tuple[int, int]:
        """Transform a position from rotated space back to original space.

        Undoes n_rotations_cw clockwise rotations by applying the same
        number of counter-clockwise rotations.
        """
        r, c = pos
        n = self.size
        for _ in range(n_rotations_cw):
            # One CCW rotation of a point
            r, c = n - 1 - c, r
        return (r, c)
