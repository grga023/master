"""Unit tests for the Board class."""

import sys
import unittest

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[1]))

from src.core.board import Board


class TestBoardInit(unittest.TestCase):
    """Tests for Board initialization."""

    def test_default_size(self):
        """Board defaults to 4x4 grid."""
        board = Board()
        self.assertEqual(board.size, 4)
        self.assertEqual(len(board.grid), 4)
        self.assertEqual(len(board.grid[0]), 4)

    def test_all_zeros(self):
        """New board is initialized with all zeros."""
        board = Board()
        for row in board.grid:
            for cell in row:
                self.assertEqual(cell, 0)

    def test_custom_size(self):
        """Board supports custom sizes."""
        board = Board(size=3)
        self.assertEqual(board.size, 3)
        self.assertEqual(len(board.grid), 3)


class TestSpawnTile(unittest.TestCase):
    """Tests for tile spawning."""

    def test_spawn_places_tile_on_empty_cell(self):
        """spawn_tile places a 2 or 4 on an empty cell."""
        board = Board()
        pos = board.spawn_tile()
        self.assertIsNotNone(pos)
        row, col = pos
        self.assertIn(board.grid[row][col], (2, 4))

    def test_spawn_returns_none_on_full_board(self):
        """spawn_tile returns None when no empty cells exist."""
        board = Board()
        board.grid = [[2, 4, 2, 4] for _ in range(4)]
        self.assertIsNone(board.spawn_tile())

    def test_spawn_only_fills_empty(self):
        """spawn_tile only places a tile where the cell was 0."""
        board = Board()
        # Fill all but one cell
        board.grid = [[8] * 4 for _ in range(4)]
        board.grid[2][3] = 0
        pos = board.spawn_tile()
        self.assertEqual(pos, (2, 3))


class TestGetEmptyCells(unittest.TestCase):
    """Tests for get_empty_cells."""

    def test_empty_board(self):
        """Empty board has 16 empty cells."""
        board = Board()
        self.assertEqual(len(board.get_empty_cells()), 16)

    def test_partial_board(self):
        """Returns correct positions for partially filled board."""
        board = Board()
        board.grid[0][0] = 2
        board.grid[1][1] = 4
        empty = board.get_empty_cells()
        self.assertEqual(len(empty), 14)
        self.assertNotIn((0, 0), empty)
        self.assertNotIn((1, 1), empty)

    def test_full_board(self):
        """Full board has no empty cells."""
        board = Board()
        board.grid = [[2] * 4 for _ in range(4)]
        self.assertEqual(board.get_empty_cells(), [])


class TestCanMove(unittest.TestCase):
    """Tests for can_move."""

    def test_stuck_board(self):
        """can_move returns False on a board with no valid moves."""
        board = Board()
        # Checkerboard pattern with no adjacent equal values
        board.grid = [
            [2, 4, 2, 4],
            [4, 2, 4, 2],
            [2, 4, 2, 4],
            [4, 2, 4, 2],
        ]
        self.assertFalse(board.can_move())

    def test_moves_available_with_empty(self):
        """can_move returns True when empty cells exist."""
        board = Board()
        board.grid[0][0] = 2
        self.assertTrue(board.can_move())

    def test_moves_available_with_adjacent_equal(self):
        """can_move returns True when adjacent equal tiles exist."""
        board = Board()
        board.grid = [
            [2, 4, 2, 4],
            [4, 2, 4, 2],
            [2, 4, 2, 4],
            [4, 2, 4, 4],  # last two are equal
        ]
        self.assertTrue(board.can_move())


class TestHasWon(unittest.TestCase):
    """Tests for has_won."""

    def test_no_win(self):
        """has_won returns False when no tile reaches 2048."""
        board = Board()
        board.grid[0][0] = 1024
        self.assertFalse(board.has_won())

    def test_win_with_2048(self):
        """has_won returns True when a tile reaches 2048."""
        board = Board()
        board.grid[1][2] = 2048
        self.assertTrue(board.has_won())

    def test_win_with_higher_tile(self):
        """has_won returns True for tiles beyond 2048."""
        board = Board()
        board.grid[0][0] = 4096
        self.assertTrue(board.has_won())


class TestClone(unittest.TestCase):
    """Tests for clone."""

    def test_clone_is_equal(self):
        """Cloned board has same grid contents."""
        board = Board()
        board.grid[0][0] = 2
        board.grid[3][3] = 4
        clone = board.clone()
        self.assertEqual(board.grid, clone.grid)

    def test_clone_is_independent(self):
        """Modifying clone doesn't affect original."""
        board = Board()
        board.grid[0][0] = 2
        clone = board.clone()
        clone.grid[0][0] = 8
        self.assertEqual(board.grid[0][0], 2)


class TestMoveLeft(unittest.TestCase):
    """Tests for left moves."""

    def test_simple_merge(self):
        """[2,2,0,0] merges to [4,0,0,0] on left move."""
        board = Board()
        board.grid[0] = [2, 2, 0, 0]
        result = board.move("left")
        self.assertEqual(board.grid[0], [4, 0, 0, 0])
        self.assertTrue(result.board_changed)

    def test_cascade_merge(self):
        """[2,2,2,2] merges to [4,4,0,0] on left move."""
        board = Board()
        board.grid[0] = [2, 2, 2, 2]
        result = board.move("left")
        self.assertEqual(board.grid[0], [4, 4, 0, 0])
        self.assertEqual(result.score_gained, 8)

    def test_merge_scoring(self):
        """Merging two 2s gives 4 points."""
        board = Board()
        board.grid[0] = [2, 2, 0, 0]
        result = board.move("left")
        self.assertEqual(result.score_gained, 4)


class TestMoveRight(unittest.TestCase):
    """Tests for right moves."""

    def test_simple_merge(self):
        """[0,0,2,2] merges to [0,0,0,4] on right move."""
        board = Board()
        board.grid[0] = [0, 0, 2, 2]
        result = board.move("right")
        self.assertEqual(board.grid[0], [0, 0, 0, 4])
        self.assertTrue(result.board_changed)

    def test_slide_right(self):
        """[2,0,0,0] slides to [0,0,0,2] on right move."""
        board = Board()
        board.grid[0] = [2, 0, 0, 0]
        result = board.move("right")
        self.assertEqual(board.grid[0], [0, 0, 0, 2])
        self.assertTrue(result.board_changed)


class TestMoveUp(unittest.TestCase):
    """Tests for up moves."""

    def test_simple_merge(self):
        """Column with [2,2,0,0] merges to [4,0,0,0] on up move."""
        board = Board()
        board.grid[0][0] = 2
        board.grid[1][0] = 2
        result = board.move("up")
        self.assertEqual(board.grid[0][0], 4)
        self.assertEqual(board.grid[1][0], 0)
        self.assertTrue(result.board_changed)


class TestMoveDown(unittest.TestCase):
    """Tests for down moves."""

    def test_simple_merge(self):
        """Column with [2,2,0,0] merges to [0,0,0,4] on down move."""
        board = Board()
        board.grid[0][0] = 2
        board.grid[1][0] = 2
        result = board.move("down")
        self.assertEqual(board.grid[3][0], 4)
        self.assertEqual(board.grid[0][0], 0)
        self.assertTrue(result.board_changed)


class TestNoOpMove(unittest.TestCase):
    """Tests for moves that have no effect."""

    def test_no_change(self):
        """Move that doesn't change the board sets board_changed=False."""
        board = Board()
        board.grid[0] = [2, 4, 8, 16]
        result = board.move("left")
        self.assertFalse(result.board_changed)
        self.assertEqual(result.score_gained, 0)

    def test_all_left_already(self):
        """Board already slid left returns board_changed=False."""
        board = Board()
        board.grid = [
            [2, 4, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ]
        result = board.move("left")
        self.assertFalse(result.board_changed)


if __name__ == "__main__":
    unittest.main()
