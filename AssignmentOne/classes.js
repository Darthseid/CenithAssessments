class Player 
{
  /**
   * Creates an instance of Player.
   * @param {number} health - The initial health of the player.
   * @param {number} moves - The initial number of moves the player has.
   * @param {number[]} coordinates - The initial [x, y] coordinates of the player.
   */
  constructor(health, moves, coordinates)
  {
    this.health = health;
    this.moves = moves;
    this.coordinates = coordinates; // [x, y]
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
   * Creates an instance of Map.
   * @param {number} seed - The seed used for map generation.
   */
  constructor(seed)
  {
    this.seed = seed;
    this.tiles = []; // An array to hold Tile objects
  }

  /**
   * Adds a tile to the map.
   * @param {Tile} tile - The tile to add to the map.
   */
  addTile(tile) 
  {
    if (tile instanceof Tile) 
	{
      this.tiles.push(tile);
    } else 
	{
      console.error("Invalid object. Only Tile instances can be added to the map's tiles array.");
    }
  }
}