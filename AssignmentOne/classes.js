class Player 
{
  /**
   * Creates an instance of Player.
   * @param {number} health - The initial health of the player.
   * @param {number} moves - The initial number of moves the player has.
   * @param {number[]} coordinates - The initial [x, y] coordinates of the player.
   */
  constructor(health, moves, coordinates, activeGame)
  {
    this.health = health;
    this.moves = moves;
    this.coordinates = coordinates; // [x, y]
	this.activeGame = activeGame;
  }
}

class Tile 
{
  /**
   * Creates an instance of Tile.
   * @param {string} name - The name of the tile (e.g., "grass", "water", "wall").
   * @param {number[]} coordinates - The [x, y] coordinates of the tile.
   */
  constructor(name, coordinates)
  {
    this.name = name;
    this.coordinates = coordinates; // [x, y]
  }
}

class Map 
{
  /**
   * @param {number} seed
   * @param {number} width
   * @param {number} height
   */
  constructor(seed, width, height) 
  {
    this.seed = seed;
    this.width = width;
    this.height = height;
    this.tiles = [];
  }

  addTile(tile) 
  {
    if (tile instanceof Tile)
		{
      this.tiles.push(tile);
    } else {
      console.error("Only Tile instances allowed.");
    }
  }

  getTileAt(x, y) 
  {
    return this.tiles.find(tile => 
      tile.coordinates[0] === x && tile.coordinates[1] === y
    );
  }
}

