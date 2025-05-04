/**
 * Executes the action associated with the tile the player is currently on.
 * @param {Player} player - The player object.
 * @param {Map} map - The map object containing the tiles.
 */
function executeTile(player, map) 
{
  const playerX = player.coordinates[0];
  const playerY = player.coordinates[1];
  const currentTile = map.tiles.find(tile =>
    tile.coordinates[0] === playerX && tile.coordinates[1] === playerY
  );  // Find the tile the player is on
  if (currentTile)
	  {
    console.log(`Player is on a ${currentTile.name}`);
    switch (currentTile.name) 
	{
      case "Blank":
        player.moves -= 1;
        console.log("Moves reduced by 1.");
        break;
      case "Speeder":
        player.health -= 5;
        console.log("Health reduced by 5.");
        break;
      case "Lava":
        player.health -= 50;
        player.moves -= 10;
        console.log("Health reduced by 50, Moves reduced by 10.");
        break;
      case "Mud":
        player.health -= 10;
        player.moves -= 5;
        console.log("Health reduced by 10, Moves reduced by 5.");
        break;
      case "Victory":
        player.moves -= 1;
        console.log("Moves reduced by 1.");
        if (player.moves >= 0) 
		{
          victory();
        } 
        break;
      default:
        console.log("Player is on an unknown tile type.");
        break;
    }
  } else 
  {
    console.log("Player is not on a recognized tile.");
  }
 updatePlayerStatsDisplay(gamePlayer); // Use the global gamePlayer object
  if (player.health <= 0 || player.moves <= 0) 
  {
    gameOver(player); // Pass player to gameOver function
  }
}

/**
 * Handles the victory condition of the game.
 */
function victory() 
{
   player.activeGame = false;
  alert("Congratulations, you won!");
  setTimeout(() => 
  {
    window.location.reload(); // Refreshes the page
  }, 5000); // 5000 milliseconds = 5 seconds
}
/**
 * Handles the game over condition.
 * @param {Player} player - The player object.
 */
function gameOver(player)
 {
  player.activeGame = false;
  alert("Game Over");
  setTimeout(() => 
  {
    window.location.reload(); // Refreshes the page
  }, 5000); // 5000 milliseconds = 5 seconds
}

/**
 * Generates a 50x50 game map with a start and end tile.
 * @param {number} seed - The seed for random map generation.
 * @returns {Map} The generated map object.
 */
function generateMap(seed)
 {
  const width = 50;
  const height = 50;
  const map = new Map(seed, width, height);
const random = (max) => {seed = (seed * 9301 + 49297) % 233280; return Math.floor((seed / 233280) * max); }; //LCG Formula.
  for (let y = 0; y < height; y++) 
  {
    for (let x = 0; x < width; x++) 
	{
      let tileName = "Blank"; // Default tile
      if (x === 0 && y === 0) 
	  {
        tileName = "Blank"; // Start tile is always blank
      } else if (x === width - 1 && y === height - 1) 
	  {
        tileName = "Victory"; // End tile is always Victory
      } else 
	  {
        const tileType = random(100);
        if (tileType <= 24) 
		{
          tileName = "Blank";
        } else if (tileType > 24 && tileType < 50) //25-49
		{
          tileName = "Speeder";
        } else if (tileType > 49 && tileType < 75) //50-74
		{
          tileName = "Mud";
        }
		else
		{
			tileName = "Lava"; //Fallback tile.
		}
      }
      map.addTile(new Tile(tileName, [x, y]));
    }
  }
  return map;
}

/**
 * Initializes a new player with starting stats and position.
 * @returns {Player} The initialized player object.
 */
function initializePlayer() {
  return new Player(200, 450, [0, 0], true);
}