# test_grid_game.py

import unittest
from unittest.mock import patch, MagicMock
import tkinter as tk

from GridGame import GridGame

class GridGameTest(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()  # Don't show GUI

        # Patch image loading and canvas methods that require a real GUI
        patcher_img = patch('tkinter.PhotoImage', return_value=MagicMock())
        patcher_canvas_img = patch.object(tk.Canvas, 'create_image', return_value=None)
        patcher_canvas_create = patch.object(tk.Canvas, 'create_rectangle', return_value=None)
        patcher_canvas_text = patch.object(tk.Canvas, 'create_text', return_value=None)
        patcher_canvas_delete = patch.object(tk.Canvas, 'delete', return_value=None)

        self.addCleanup(patcher_img.stop)
        self.addCleanup(patcher_canvas_img.stop)
        self.addCleanup(patcher_canvas_create.stop)
        self.addCleanup(patcher_canvas_text.stop)
        self.addCleanup(patcher_canvas_delete.stop)

        patcher_img.start()
        patcher_canvas_img.start()
        patcher_canvas_create.start()
        patcher_canvas_text.start()
        patcher_canvas_delete.start()

        self.game = GridGame(self.root)

    def test_initial_state(self):
        self.assertEqual(self.game.player_pos, [0, 0])
        self.assertEqual(self.game.health, 100)
        self.assertEqual(self.game.moves, 100)

    def test_move_valid(self):
        self.game.move_player(1, 0)
        self.assertEqual(self.game.player_pos, [1, 0])
        self.assertEqual(self.game.moves, 99)

    def test_move_out_of_bounds(self):
        self.game.player_pos = [0, 0]
        self.game.move_player(-1, 0)
        self.assertEqual(self.game.player_pos, [0, 0])  # No move
        self.assertEqual(self.game.moves, 100)  # No move cost

    def test_health_and_moves_effect(self):
        self.game.grid[1][0] = 'lava'  # Force harmful tile
        self.game.move_player(1, 0)
        self.assertLess(self.game.health, 100)
        self.assertLess(self.game.moves, 100)

    def test_save_and_load_game(self):
        self.game.player_pos = [2, 3]
        self.game.health = 75
        self.game.moves = 80
        self.game.save_game()
        self.game.player_pos = [0, 0]
        self.game.health = 100
        self.game.moves = 100
        self.game.load_game()
        self.assertEqual(self.game.player_pos, [2, 3])
        self.assertEqual(self.game.health, 75)
        self.assertEqual(self.game.moves, 80)

    def test_game_over_moves(self):
        self.game.moves = 1
        self.game.move_player(1, 0)
        self.assertTrue(self.game.game_over)

    def test_victory_condition(self):
        self.game.player_pos = [9, 8]
        self.game.move_player(0, 1)
        self.assertTrue(self.game.victory)

if __name__ == '__main__':
    unittest.main()
