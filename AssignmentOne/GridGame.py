# tkinter_version.py
import tkinter as tk
from tkinter import messagebox
import random

TILE_SIZE = 16
TILE_IMAGES = {
    "Blank": "Blank.gif",
    "Speeder": "Speeder.gif",
    "Lava": "Lava.gif",
    "Mud": "Mud.gif",
    "Victory": "Finish.gif",
    "Player": "Car.gif"
}

class Player:
    def __init__(self, health, moves, coordinates):
        self.health = health
        self.moves = moves
        self.coordinates = coordinates
        self.active_game = True

class Tile:
    def __init__(self, name, coordinates):
        self.name = name
        self.coordinates = coordinates

class Map:
    def __init__(self, seed, width, height):
        self.seed = seed
        self.width = width
        self.height = height
        self.tiles = []
        random.seed(seed)

    def add_tile(self, tile):
        if isinstance(tile, Tile):
            self.tiles.append(tile)

    def get_tile_at(self, x, y):
        for tile in self.tiles:
            if tile.coordinates == [x, y]:
                return tile
        return None

def generate_map(seed):
    width = 50
    height = 50
    game_map = Map(seed, width, height)
    for y in range(height):
        for x in range(width):
            if x == 0 and y == 0:
                tile_name = "Blank"
            elif x == width - 1 and y == height - 1:
                tile_name = "Victory"
            else:
                roll = random.randint(0, 99)
                tile_name = ("Blank" if roll <= 24 else
                             "Speeder" if roll < 50 else
                             "Mud" if roll < 75 else
                             "Lava")
            game_map.add_tile(Tile(tile_name, [x, y]))
    return game_map

def execute_tile(player, game_map):
    x, y = player.coordinates
    tile = game_map.get_tile_at(x, y)
    if tile:
        if tile.name == "Blank":
            player.moves = max(0, player.moves - 1)
        elif tile.name == "Speeder":
            player.health = max(0, player.health - 5)
        elif tile.name == "Mud":
            player.health = max(0, player.health - 10)
            player.moves = max(0, player.moves - 5)
        elif tile.name == "Lava":
            player.health = max(0, player.health - 50)
            player.moves = max(0, player.moves - 10)
        elif tile.name == "Victory":
            player.moves = max(0, player.moves - 1)
            if player.moves > 0:
                messagebox.showinfo("Victory", "You won!")
                player.active_game = False
            else:
                print("Victory tile, but not enough moves.")

    if player.health <= 0 or player.moves <= 0:
        messagebox.showerror("Game Over", "You lost!")
        player.active_game = False

class GameApp:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=800, height=800)
        self.canvas.pack()

        self.health_var = tk.StringVar()
        self.moves_var = tk.StringVar()
        self.coords_var = tk.StringVar()

        tk.Label(root, textvariable=self.health_var).pack()
        tk.Label(root, textvariable=self.moves_var).pack()
        tk.Label(root, textvariable=self.coords_var).pack()
        tk.Button(root, text="Restart", command=self.start_game).pack()

        self.images = {k: tk.PhotoImage(file=v) for k, v in TILE_IMAGES.items()}

        self.canvas.bind_all('<Key>', self.handle_key)
        self.start_game()

    def start_game(self):
        self.seed = random.randint(0, 999999)
        self.map = generate_map(self.seed)
        self.player = Player(200, 450, [0, 0])
        self.render_map()
        self.update_ui()

    def update_ui(self):
        self.health_var.set(f"Health: {self.player.health}")
        self.moves_var.set(f"Moves: {self.player.moves}")
        x, y = self.player.coordinates
        self.coords_var.set(f"Coordinates: [{x}, {y}]")

    def render_map(self):
        self.canvas.delete("all")
        for tile in self.map.tiles:
            x, y = tile.coordinates
            img = self.images[tile.name]
            self.canvas.create_image(x * TILE_SIZE, y * TILE_SIZE, anchor='nw', image=img)
        px, py = self.player.coordinates
        self.canvas.create_image(px * TILE_SIZE, py * TILE_SIZE, anchor='nw', image=self.images['Player'])

    def handle_key(self, event):
        if not self.player.active_game:
            return
        dx, dy = 0, 0
        key = event.keysym
        shift = bool(event.state & 0x1)
        ctrl = bool(event.state & 0x4)

        if shift and key == 'Right': dx, dy = 1, -1
        elif shift and key == 'Left': dx, dy = -1, -1
        elif ctrl and key == 'Right': dx, dy = 1, 1
        elif ctrl and key == 'Left': dx, dy = -1, 1
        elif key == 'Up': dy = -1
        elif key == 'Down': dy = 1
        elif key == 'Left': dx = -1
        elif key == 'Right': dx = 1

        nx = self.player.coordinates[0] + dx
        ny = self.player.coordinates[1] + dy
        if 0 <= nx < self.map.width and 0 <= ny < self.map.height:
            self.player.coordinates = [nx, ny]
            execute_tile(self.player, self.map)
            self.render_map()
            self.update_ui()

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Assignment One Game - Tkinter Version")
    app = GameApp(root)
    root.mainloop()
