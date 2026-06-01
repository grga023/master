"""Tests for Fibonacci board logic."""
import pytest
from src.core.fibonacci_board import FibonacciBoard, can_fibonacci_merge, FIBONACCI_MERGES


class TestFibonacciMerge:
    """Test the can_fibonacci_merge function."""

    def test_1_plus_1_equals_2(self):
        assert can_fibonacci_merge(1, 1) == 2

    def test_1_plus_2_equals_3(self):
        assert can_fibonacci_merge(1, 2) == 3

    def test_2_plus_1_equals_3(self):
        assert can_fibonacci_merge(2, 1) == 3

    def test_2_plus_3_equals_5(self):
        assert can_fibonacci_merge(2, 3) == 5

    def test_3_plus_5_equals_8(self):
        assert can_fibonacci_merge(3, 5) == 8

    def test_2_plus_2_does_not_merge(self):
        assert can_fibonacci_merge(2, 2) is None

    def test_3_plus_3_does_not_merge(self):
        assert can_fibonacci_merge(3, 3) is None

    def test_5_plus_5_does_not_merge(self):
        assert can_fibonacci_merge(5, 5) is None

    def test_zero_does_not_merge(self):
        assert can_fibonacci_merge(0, 1) is None
        assert can_fibonacci_merge(1, 0) is None


class TestFibonacciBoard:
    """Test FibonacciBoard class."""

    def test_slide_row_1_2_merge(self):
        board = FibonacciBoard()
        row = [1, 2, 0, 0]
        new_row, score, movements, merges = board._slide_row_left(row, 0)
        assert new_row == [3, 0, 0, 0]
        assert score == 3

    def test_slide_row_1_2_3_partial_merge(self):
        """[1, 2, 3, 0] -> 1+2=3, then new 3 does NOT merge with old 3."""
        board = FibonacciBoard()
        row = [1, 2, 3, 0]
        new_row, score, movements, merges = board._slide_row_left(row, 0)
        assert new_row == [3, 3, 0, 0]
        assert score == 3

    def test_slide_row_no_merge(self):
        """[2, 2, 0, 0] -> no merge (not adjacent Fib pair)."""
        board = FibonacciBoard()
        row = [2, 2, 0, 0]
        new_row, score, movements, merges = board._slide_row_left(row, 0)
        assert new_row == [2, 2, 0, 0]
        assert score == 0

    def test_spawn_tile_values(self):
        """Spawn should only produce 1 or 2."""
        board = FibonacciBoard()
        values_seen = set()
        for _ in range(200):
            board.grid = [[0] * 4 for _ in range(4)]
            board.spawn_tile()
            for row in board.grid:
                for val in row:
                    if val != 0:
                        values_seen.add(val)
        assert values_seen <= {1, 2}

    def test_can_move_false_no_adjacent_fib(self):
        """Board full with no adjacent Fib pairs -> can't move."""
        board = FibonacciBoard()
        # Fill with pattern that has no adjacent Fibonacci pairs
        board.grid = [
            [2, 8, 2, 8],
            [8, 2, 8, 2],
            [2, 8, 2, 8],
            [8, 2, 8, 2],
        ]
        assert board.can_move() is False

    def test_can_move_true_with_empty(self):
        board = FibonacciBoard()
        board.grid = [
            [2, 8, 2, 8],
            [8, 2, 8, 2],
            [2, 8, 2, 8],
            [8, 2, 8, 0],
        ]
        assert board.can_move() is True

    def test_has_won_true(self):
        board = FibonacciBoard()
        board.grid[0][0] = 610
        assert board.has_won() is True

    def test_has_won_false(self):
        board = FibonacciBoard()
        board.grid[0][0] = 377
        assert board.has_won() is False

    def test_full_move_direction(self):
        """Test a full 'left' move with Fibonacci merging."""
        board = FibonacciBoard()
        board.grid = [
            [0, 1, 1, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ]
        result = board.move("left")
        assert result.board_changed is True
        assert board.grid[0][0] == 2
        assert result.score_gained == 2
