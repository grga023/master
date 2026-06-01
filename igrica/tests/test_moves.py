"""Unit tests for move mechanics and MoveResult details."""

import sys
import unittest

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[1]))

from src.core.board import Board
from src.core.move_result import MoveResult, TileMerge, TileMovement


class TestSlideRowLeft(unittest.TestCase):
    """Tests for left-slide row behavior via board.move('left')."""

    def setUp(self):
        """Create a fresh board for each test."""
        self.board = Board()

    def test_merge_with_gaps(self):
        """[2,0,2,0] slides and merges to [4,0,0,0]."""
        self.board.grid[0] = [2, 0, 2, 0]
        self.board.move("left")
        self.assertEqual(self.board.grid[0], [4, 0, 0, 0])

    def test_double_merge(self):
        """[2,2,4,4] merges to [4,8,0,0]."""
        self.board.grid[0] = [2, 2, 4, 4]
        self.board.move("left")
        self.assertEqual(self.board.grid[0], [4, 8, 0, 0])

    def test_slide_from_end(self):
        """[0,0,0,2] slides to [2,0,0,0]."""
        self.board.grid[0] = [0, 0, 0, 2]
        self.board.move("left")
        self.assertEqual(self.board.grid[0], [2, 0, 0, 0])

    def test_no_merge_distinct(self):
        """[2,4,8,16] stays [2,4,8,16] (no merge possible)."""
        self.board.grid[0] = [2, 4, 8, 16]
        result = self.board.move("left")
        self.assertEqual(self.board.grid[0], [2, 4, 8, 16])
        self.assertFalse(result.board_changed)


class TestMoveResultMovements(unittest.TestCase):
    """Tests that MoveResult correctly tracks tile movements."""

    def test_movements_on_slide(self):
        """Sliding [0,0,0,2] left produces a movement from col 3 to col 0."""
        board = Board()
        board.grid[0] = [0, 0, 0, 2]
        result = board.move("left")
        self.assertTrue(len(result.movements) > 0)
        # The tile at (0,3) should move to (0,0)
        moved = [m for m in result.movements if m.from_pos == (0, 3)]
        self.assertEqual(len(moved), 1)
        self.assertEqual(moved[0].to_pos, (0, 0))
        self.assertEqual(moved[0].value, 2)

    def test_movements_on_merge(self):
        """Merging [2,2,0,0] left produces two movements to col 0."""
        board = Board()
        board.grid[0] = [2, 2, 0, 0]
        result = board.move("left")
        # Both tiles move to column 0
        to_zero = [m for m in result.movements if m.to_pos == (0, 0)]
        self.assertEqual(len(to_zero), 2)


class TestMoveResultMerges(unittest.TestCase):
    """Tests that MoveResult correctly tracks merges."""

    def test_merge_info(self):
        """Merging [2,2,0,0] left produces a merge at (0,0) with value 4."""
        board = Board()
        board.grid[0] = [2, 2, 0, 0]
        result = board.move("left")
        self.assertEqual(len(result.merges), 1)
        self.assertEqual(result.merges[0].pos, (0, 0))
        self.assertEqual(result.merges[0].new_value, 4)

    def test_double_merge_info(self):
        """[2,2,4,4] left produces two merges."""
        board = Board()
        board.grid[0] = [2, 2, 4, 4]
        result = board.move("left")
        self.assertEqual(len(result.merges), 2)
        values = sorted(m.new_value for m in result.merges)
        self.assertEqual(values, [4, 8])


class TestStuckDetection(unittest.TestCase):
    """Tests for full-board stuck detection."""

    def test_full_board_stuck(self):
        """Full board with no adjacent equals is stuck."""
        board = Board()
        board.grid = [
            [2, 4, 8, 16],
            [16, 8, 4, 2],
            [2, 4, 8, 16],
            [16, 8, 4, 2],
        ]
        self.assertFalse(board.can_move())

    def test_full_board_not_stuck(self):
        """Full board with adjacent equals is not stuck."""
        board = Board()
        board.grid = [
            [2, 4, 8, 16],
            [16, 8, 4, 2],
            [2, 4, 8, 16],
            [16, 8, 4, 4],  # adjacent 4s
        ]
        self.assertTrue(board.can_move())


class TestMultipleMergeScoring(unittest.TestCase):
    """Tests for score accumulation across multiple merges."""

    def test_two_merges_one_row(self):
        """[2,2,4,4] gives score 4+8=12."""
        board = Board()
        board.grid[0] = [2, 2, 4, 4]
        result = board.move("left")
        self.assertEqual(result.score_gained, 12)

    def test_multiple_rows_scoring(self):
        """Merges across multiple rows accumulate score."""
        board = Board()
        board.grid[0] = [2, 2, 0, 0]
        board.grid[1] = [4, 4, 0, 0]
        result = board.move("left")
        self.assertEqual(result.score_gained, 12)  # 4 + 8

    def test_large_merge_score(self):
        """Merging [1024, 1024, 0, 0] gives 2048 points."""
        board = Board()
        board.grid[0] = [1024, 1024, 0, 0]
        result = board.move("left")
        self.assertEqual(result.score_gained, 2048)
        self.assertEqual(board.grid[0], [2048, 0, 0, 0])


if __name__ == "__main__":
    unittest.main()
