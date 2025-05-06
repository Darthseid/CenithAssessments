import unittest
import json
import os
from GridGame import GridGame, GRID_SIZE, HEALTH_INIT, MOVES_INIT, TILE_EFFECTS
import tkinter as tk

class MockRoot(tk.Tk):
    def __init__(self):
        super().__init__()
        self.withdraw()

class GridGameTest(unittest.TestCase):
    def setUp(self):
        self.root = MockRoot()
        self.game = GridGame(self.root)

    def tearDown(self):
        self.root.destroy()
        if os.path.exists("GridSave.json"):
            os.remove("GridSave.json")

    def test_initial_state(self):
        self.assertEqual(self.game.health, HEALTH_INIT)
        self.assertEqual(self.game.moves, MOVES_INIT)
        self.assertEqual(self.game.player_pos, [0, 0])

    def test_move_valid(self):
        # Force all right tiles to be "Blank" for predictable test
        for x in range(1, 5):
            self.game.grid[0][x] = "Blank"

        for x in range(1, 5):
            self.game.move(1, 0)
            self.assertEqual(self.game.player_pos[0], x)
            self.assertEqual(self.game.player_pos[1], 0)

    def test_move_out_of_bounds(self):
        self.game.move(-1, 0)
        self.assertEqual(self.game.player_pos, [0, 0])

        self.game.move(0, -1)
        self.assertEqual(self.game.player_pos, [0, 0])

    def test_health_and_moves_effect(self):
        self.game.grid[0][1] = "Lava"
        self.game.move(1, 0)
        self.assertEqual(self.game.player_pos, [1, 0])
        self.assertEqual(self.game.health, HEALTH_INIT + TILE_EFFECTS["Lava"]["Health"])
        self.assertEqual(self.game.moves, MOVES_INIT + TILE_EFFECTS["Lava"]["Moves"])

    def test_save_and_load_game(self):
        self.game.grid[1][0] = "Speeder"
        self.game.move(0, 1)
        state_before = (self.game.grid, self.game.player_pos, self.game.health, self.game.moves)

        self.game.save_game()
        self.assertTrue(os.path.exists("GridSave.json"))

        self.game.player_pos = [0, 0]
        self.game.load_game()

        self.assertEqual(self.game.grid, state_before[0])
        self.assertEqual(self.game.player_pos, state_before[1])
        self.assertEqual(self.game.health, state_before[2])
        self.assertEqual(self.game.moves, state_before[3])

    def test_victory_condition(self):
        self.game.player_pos = self.game.goal_pos[:]
        self.game.moves = 10
        self.game.health = 100
        self.game.move(0, 0)  # triggers check
        self.assertFalse(self.game.game_active)

    def test_game_over_health(self):
        self.game.health = 1
        self.game.grid[0][1] = "Lava"
        self.game.move(1, 0)
        self.assertFalse(self.game.game_active)

    def test_game_over_moves(self):
        self.game.moves = 1
        self.game.grid[0][1] = "Blank"
        self.game.move(1, 0)
        self.assertFalse(self.game.game_active)

if __name__ == "__main__":
    unittest.main()
