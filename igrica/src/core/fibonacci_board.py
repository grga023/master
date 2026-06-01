"""Fibonacci board logic for 2048-Fibonacci mode."""
import random
from typing import List, Optional, Tuple
from src.core.board import Board
from src.core.move_result import MoveResult, TileMovement, TileMerge

# Pre-computed Fibonacci sequence
FIBONACCI_SEQUENCE = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987]
FIBONACCI_SET = set(FIBONACCI_SEQUENCE)

# Valid merge pairs: maps (a, b) -> merged_value
FIBONACCI_MERGES = {}
# Special case: 1+1=2
FIBONACCI_MERGES[(1, 1)] = 2
# Adjacent pairs
for i in range(1, len(FIBONACCI_SEQUENCE) - 1):
    a = FIBONACCI_SEQUENCE[i]
    b = FIBONACCI_SEQUENCE[i + 1]
    if a != b:  # skip second (1,1) duplicate  
        FIBONACCI_MERGES[(a, b)] = a + b
        FIBONACCI_MERGES[(b, a)] = a + b  # order-independent


def can_fibonacci_merge(a: int, b: int) -> Optional[int]:
    """Returns merged value if a and b are adjacent Fibonacci numbers, else None."""
    if a == 0 or b == 0:
        return None
    return FIBONACCI_MERGES.get((a, b))


class FibonacciBoard(Board):
    """Board with Fibonacci merge rules. Adjacent Fibonacci numbers merge into their sum."""

    def __init__(self, size: int = 4, win_target: int = 610):
        super().__init__(size)
        self.win_target = win_target

    def spawn_tile(self) -> Optional[Tuple[int, int]]:
        """Spawn 1 (90%) or 2 (10%) on random empty cell."""
        empty = self.get_empty_cells()
        if not empty:
            return None
        row, col = random.choice(empty)
        self.grid[row][col] = 1 if random.random() < 0.9 else 2
        return (row, col)

    def can_move(self) -> bool:
        """Check if any valid move exists."""
        if self.get_empty_cells():
            return True
        for r in range(self.size):
            for c in range(self.size):
                val = self.grid[r][c]
                if c + 1 < self.size and can_fibonacci_merge(val, self.grid[r][c + 1]) is not None:
                    return True
                if r + 1 < self.size and can_fibonacci_merge(val, self.grid[r + 1][c]) is not None:
                    return True
        return False

    def has_won(self) -> bool:
        """Check if win target reached."""
        for row in self.grid:
            for val in row:
                if val >= self.win_target:
                    return True
        return False

    def _slide_row_left(self, row: list, row_idx: int):
        """Slide with Fibonacci merge rules: adjacent Fib numbers merge."""
        movements = []
        merges = []
        non_zero = [(val, col) for col, val in enumerate(row) if val != 0]
        
        merged = []
        score = 0
        skip = False
        dest_col = 0

        for i in range(len(non_zero)):
            if skip:
                skip = False
                dest_col += 1
                continue

            val, orig_col = non_zero[i]

            if i + 1 < len(non_zero):
                val2, orig_col2 = non_zero[i + 1]
                new_val = can_fibonacci_merge(val, val2)
                if new_val is not None:
                    merged.append(new_val)
                    score += new_val
                    skip = True
                    movements.append(TileMovement(from_pos=(row_idx, orig_col), to_pos=(row_idx, dest_col), value=val))
                    movements.append(TileMovement(from_pos=(row_idx, orig_col2), to_pos=(row_idx, dest_col), value=val2))
                    merges.append(TileMerge(pos=(row_idx, dest_col), new_value=new_val))
                    dest_col += 1
                    continue

            merged.append(val)
            if orig_col != dest_col:
                movements.append(TileMovement(from_pos=(row_idx, orig_col), to_pos=(row_idx, dest_col), value=val))
            dest_col += 1

        merged += [0] * (self.size - len(merged))
        return merged, score, movements, merges
