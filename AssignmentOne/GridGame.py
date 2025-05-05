# file: grid_game.py

import tkinter as tk
import random
import os
from PIL import Image, ImageTk
from playsound import playsound
import threading

GRID_SIZE = 50
TILE_SIZE = 10
HEALTH_INIT = 200
MOVES_INIT = 450

TILE_TYPES = ["Blank", "Speeder", "Lava", "Mud"]
TILE_COLORS = {
    "Blank": "white",
    "Speeder": "blue",
    "Lava": "red",
    "Mud": "brown",
    "Player": "green",
    "Goal": "gold",
}

TILE_EFFECTS = {
    "Blank": {"Health": 0, "Moves": -1},
    "Speeder": {"Health": -5, "Moves": 0},
    "Lava": {"Health": -50, "Moves": -10},
    "Mud": {"Health": -10, "Moves": -5},
}

IMG_CACHE = {}

def load_image(name):
    try:
        if name in IMG_CACHE:
            return IMG_CACHE[name]
        path = os.path.join("assets", "img", f"{name}.png")
        img = Image.open(path).resize((TILE_SIZE, TILE_SIZE))
        tk_img = ImageTk.PhotoImage(img)
        IMG_CACHE[name] = tk_img
        return tk_img
    except:
        return None

def play_sound(name):
    def inner():
        try:
            path = os.path.join("assets", "snd", f"{name}.mp3")
            playsound(path)
        except:
            pass
    threading.Thread(target=inner, daemon=True).start()

class GridGame:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=GRID_SIZE*TILE_SIZE, height=GRID_SIZE*TILE_SIZE)
        self.canvas.pack()

        self.restart_button = tk.Button(root, text="Restart Game", command=self.restart_game)
        self.restart_button.pack(pady=5)

        self.init_game()

        self.root.bind("<KeyPress>", self.handle_key)

    def init_game(self):
        self.health = HEALTH_INIT
        self.moves = MOVES_INIT
        self.player_pos = [0, GRID_SIZE // 2]
        self.goal_pos = [GRID_SIZE - 1, GRID_SIZE // 2]

        self.grid = [[random.choice(TILE_TYPES) for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.grid[self.player_pos[1]][self.player_pos[0]] = "Blank"
        self.grid[self.goal_pos[1]][self.goal_pos[0]] = "Goal"

        self.draw_grid()
        self.update_status()

    def restart_game(self):
        self.init_game()

    def draw_grid(self):
        self.canvas.delete("all")
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                tile = self.grid[y][x]
                img = load_image(tile)
                if img:
                    self.canvas.create_image(x*TILE_SIZE, y*TILE_SIZE, anchor='nw', image=img)
                else:
                    color = TILE_COLORS.get(tile, "white")
                    self.canvas.create_rectangle(
                        x*TILE_SIZE, y*TILE_SIZE,
                        (x+1)*TILE_SIZE, (y+1)*TILE_SIZE,
                        fill=color, outline="gray"
                    )

        px, py = self.player_pos
        self.canvas.create_rectangle(
            px*TILE_SIZE, py*TILE_SIZE,
            (px+1)*TILE_SIZE, (py+1)*TILE_SIZE,
            fill=TILE_COLORS["Player"]
        )

    def update_status(self):
        self.root.title(f"Health: {self.health} | Moves: {self.moves}")

    def handle_key(self, event):
        dx, dy = 0, 0
        if event.keysym == "Up": dy = -1
        elif event.keysym == "Down": dy = 1
        elif event.keysym == "Left": dx = -1
        elif event.keysym == "Right": dx = 1

        if dx != 0:
            if event.state & 0x0001:  # Shift held
                dy = -1
            elif event.state & 0x0004:  # Ctrl held
                dy = 1

        self.move(dx, dy)

    def move(self, dx, dy):
        if self.health <= 0 or self.moves <= 0:
            return

        new_x = self.player_pos[0] + dx
        new_y = self.player_pos[1] + dy

        if not (0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE):
            return

        tile = self.grid[new_y][new_x]
        effects = TILE_EFFECTS.get(tile, {"Health": 0, "Moves": 0})
        self.health += effects["Health"]
        self.moves += effects["Moves"]
        self.player_pos = [new_x, new_y]

        play_sound(tile)

        self.update_status()
        self.draw_grid()

        if self.player_pos == self.goal_pos:
            play_sound("Goal")
            self.end_game("You Win!")
        elif self.health <= 0 or self.moves <= 0:
            play_sound("Failure")
            self.end_game("Game Over!")

    def end_game(self, message):
        self.canvas.create_text(
            GRID_SIZE * TILE_SIZE // 2,
            GRID_SIZE * TILE_SIZE // 2,
            text=message,
            font=("Arial", 32),
            fill="black"
        )
        self.root.after(5000, self.restart_game)
