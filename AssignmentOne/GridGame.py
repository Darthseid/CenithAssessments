import tkinter as tk
import random
import os
import json
from PIL import Image, ImageTk
import pygame.mixer
import heapq

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
    "Goal": "gold",
}

TILE_EFFECTS = {
    "Blank": {"Health": 0, "Moves": -1},
    "Speeder": {"Health": -5, "Moves": 0},
    "Lava": {"Health": -50, "Moves": -10},
    "Mud": {"Health": -10, "Moves": -5},
}

IMG_CACHE = {}
SOUND_CACHE = {}

def load_image(name):
    try:
        if name in IMG_CACHE:
            return IMG_CACHE[name]
        path = os.path.join("assets", "img", f"{name}.png")
        if not os.path.exists(path):
            return None
        img = Image.open(path).resize((TILE_SIZE, TILE_SIZE))
        tk_img = ImageTk.PhotoImage(img)
        IMG_CACHE[name] = tk_img
        return tk_img
    except Exception:
        return None

def load_sound(name):
    if name in SOUND_CACHE:
        return SOUND_CACHE[name]
    try:
        path = os.path.join("assets", "snd", f"{name}.mp3")
        if not os.path.exists(path):
            return None
        sound = pygame.mixer.Sound(path)
        SOUND_CACHE[name] = sound
        return sound
    except Exception:
        return None

def play_sound(name):
    sound = load_sound(name)
    if sound:
        sound.play()

class GridGame:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=GRID_SIZE*TILE_SIZE, height=GRID_SIZE*TILE_SIZE)
        self.canvas.pack()

        self.restart_button = tk.Button(root, text="Restart Game", command=self.restart_game)
        self.restart_button.pack(pady=2)

        self.save_button = tk.Button(root, text="Save Game", command=self.save_game)
        self.save_button.pack(pady=2)

        self.load_button = tk.Button(root, text="Load Game", command=self.load_game)
        self.load_button.pack(pady=2)

        self.solution_button = tk.Button(root, text="Show Solution", command=self.find_best_path)
        self.solution_button.pack(pady=2)

        try:
            pygame.mixer.init()
        except Exception:
            pass

        self.init_game()
        self.root.bind("<KeyPress>", self.handle_key)

    def init_game(self):
        self.health = HEALTH_INIT
        self.moves = MOVES_INIT
        self.player_pos = [0, 0]
        self.goal_pos = [GRID_SIZE - 1, GRID_SIZE - 1]
        self.game_active = True

        self.grid = [[random.choice(TILE_TYPES) for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.grid[self.player_pos[1]][self.player_pos[0]] = "Blank"
        self.grid[self.goal_pos[1]][self.goal_pos[0]] = "Goal"

        self.draw_grid()
        self.update_status()

    def restart_game(self):
        self.canvas.delete("all")
        self.init_game()

    def save_game(self):
        data = {
            "grid": self.grid,
            "player_pos": self.player_pos,
            "goal_pos": self.goal_pos,
            "health": self.health,
            "moves": self.moves,
        }
        with open("GridSave.json", "w") as f:
            json.dump(data, f)

    def load_game(self):
        try:
            with open("GridSave.json", "r") as f:
                data = json.load(f)
            self.grid = data["grid"]
            self.player_pos = data["player_pos"]
            self.goal_pos = data["goal_pos"]
            self.health = data["health"]
            self.moves = data["moves"]
            self.game_active = True
            self.draw_grid()
            self.update_status()
        except Exception:
            pass

    def draw_grid(self):
        self.canvas.delete("tiles", "player_image")
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                tile_type = self.grid[y][x]
                img = load_image(tile_type)
                if img:
                    self.canvas.create_image(x*TILE_SIZE, y*TILE_SIZE, anchor='nw', image=img, tags="tiles")
                else:
                    color = TILE_COLORS.get(tile_type, "white")
                    self.canvas.create_rectangle(
                        x*TILE_SIZE, y*TILE_SIZE, (x+1)*TILE_SIZE, (y+1)*TILE_SIZE,
                        fill=color, outline="gray", tags="tiles"
                    )
        px, py = self.player_pos
        player_img = load_image("car")
        if player_img:
            self.canvas.create_image(px*TILE_SIZE, py*TILE_SIZE, anchor='nw', image=player_img, tags="player_image")
        else:
            self.canvas.create_rectangle(
                px*TILE_SIZE, py*TILE_SIZE, (px+1)*TILE_SIZE, (py+1)*TILE_SIZE,
                fill="green", tags="player_image"
            )

    def update_status(self):
        self.root.title(f"Health: {self.health} | Moves: {self.moves} | Pos: ({self.player_pos[0]}, {self.player_pos[1]})")

    def move_player(self, dx, dy):
        self.move(dx, dy)

    def handle_key(self, event):
        if not self.game_active:
            return

        dx, dy = 0, 0
        moved = False

        if event.keysym == "Up": dy = -1; moved = True
        elif event.keysym == "Down": dy = 1; moved = True
        elif event.keysym == "Left": dx = -1; moved = True
        elif event.keysym == "Right": dx = 1; moved = True

        if event.state & 0x0001:
            if event.keysym == "Right": dx, dy = 1, -1; moved = True
            elif event.keysym == "Left": dx, dy = -1, -1; moved = True
        elif event.state & 0x0004:
            if event.keysym == "Right": dx, dy = 1, 1; moved = True
            elif event.keysym == "Left": dx, dy = -1, 1; moved = True

        if moved:
            self.move(dx, dy)

    def move(self, dx, dy):
        if not self.game_active:
            return

        new_x = self.player_pos[0] + dx
        new_y = self.player_pos[1] + dy

        if not (0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE):
            return

        tile_type = self.grid[new_y][new_x]
        effects = TILE_EFFECTS.get(tile_type, {"Health": 0, "Moves": 0})
        self.health += effects["Health"]
        self.moves += effects["Moves"]
        self.player_pos = [new_x, new_y]

        play_sound(tile_type)
        self.update_status()
        self.draw_grid()

        if self.player_pos == self.goal_pos:
            if self.moves >= 0:
                self.end_game("You Win!")
            else:
                self.end_game("Game Over! (Out of moves at goal)")
        elif self.health <= 0 or self.moves <= 0:
            self.end_game("Game Over!")

    def end_game(self, message):
        if not self.game_active:
            return

        self.game_active = False
        play_sound("Victory" if "Win" in message else "Failure")
        self.canvas.create_text(
            GRID_SIZE * TILE_SIZE // 2,
            GRID_SIZE * TILE_SIZE // 2,
            text=message,
            font=("Arial", 32),
            fill="black"
        )
        self.root.after(5000, self.restart_game)

    def find_best_path(self):
        start = tuple(self.player_pos)
        goal = tuple(self.goal_pos)
        heap = [(-HEALTH_INIT, -MOVES_INIT, start[0], start[1], [start])]
        visited = set()
        best_score = -1
        best_path = []

        while heap:
            neg_h, neg_m, x, y, path = heapq.heappop(heap)
            h, m = -neg_h, -neg_m

            if (x, y) == goal and h > 0 and m >= 0:
                best_score = h + m
                best_path = path
                break

            if (x, y) in visited:
                continue
            visited.add((x, y))

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, -1), (-1, 1), (1, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE and (nx, ny) not in path:
                    tile = self.grid[ny][nx]
                    cost = TILE_EFFECTS.get(tile, {"Health": 0, "Moves": 0})
                    nh, nm = h + cost["Health"], m + cost["Moves"]
                    if nh > 0 and nm >= 0:
                        heapq.heappush(heap, (-nh, -nm, nx, ny, path + [(nx, ny)]))

        if best_path:
            print("Best path to goal:")
            for step in best_path:
                print(step)
            print(f"Health remaining: {h}, Moves remaining: {m}")
        else:
            print("Victory is Impossible")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Grid Game")
    game = GridGame(root)
    root.mainloop()
