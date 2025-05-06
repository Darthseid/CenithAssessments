import heapq #Algorithm import
from typing import List, Tuple

tile_cost = {
    "Blank": {"Health": 0, "Moves": -1},
    "Speeder": {"Health": -5, "Moves": 0},
    "Lava": {"Health": -50, "Moves": -10},
    "Mud": {"Health": -10, "Moves": -5}, # Constants
}


directions = [ # Directions: 8-connected (vertical, horizontal, diagonal)
    (-1,  0), (1,  0), (0, -1), (0, 1),
    (-1, -1), (-1, 1), (1, -1), (1, 1)
]

def is_within_bounds(x: int, y: int) -> bool:
    return 0 <= x < 50 and 0 <= y < 50

def find_best_path(grid: List[List[str]]) -> None: #Modified Djikstra's Algorithm.
    start = (0, 0)
    goal = (49, 49)
    heap = []
    heapq.heappush(heap, (-200, -450, 0, 0, [(0, 0)]))  # Maximize health+move, so negate for minheap
    visited = set() #Sets don't allow duplicates
    while heap:
        neg_health, neg_moves, x, y, path = heapq.heappop(heap)
        health = -neg_health
        moves = -neg_moves

        if (x, y) == goal:
            print("Path to goal:")
            print(path)
            print(f"Health remaining: {health}")
            print(f"Moves remaining: {moves}")
            return

        if (x, y) in visited:
            continue #Don't go back to a previously visited tile. That isn't optimal.
        visited.add((x, y))

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if not is_within_bounds(nx, ny): #Stay within the grid.
                continue
            tile = grid[nx][ny]
            cost = tile_cost[tile]
            new_health = health + cost["Health"]
            new_moves = moves + cost["Moves"]

            if new_health <= 0 or new_moves <= 0:
                continue
            heapq.heappush(heap, (-new_health, -new_moves, nx, ny, path + [(nx, ny)]))
    print("Victory is Impossible") #You won't make it to the finish line.

if __name__ == "__main__":
    test_grid = [["Blank"] * 50 for _ in range(50)]
    test_grid[0][1] = "Mud"
    test_grid[1][1] = "Speeder"
    test_grid[49][49] = "Blank"
    find_best_path(test_grid)
