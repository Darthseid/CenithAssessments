function updatePlayerStatsDisplay(player) 
{
    document.getElementById('player-health').textContent = player.health;
    document.getElementById('player-moves').textContent = player.moves;
    document.getElementById('player-coords').textContent = `[${player.coordinates[0]}, ${player.coordinates[1]}]`;
}

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
        playSound('movement.mp3');
        player.moves = Math.max(0, player.moves - 1); // Ensure moves don't go below zero
        console.log("Moves reduced by 1.");
        break;
      case "Speeder": 
        playSound('speeding.mp3'); 
        player.health = Math.max(0, player.health - 5); // Ensure health doesn't go below zero
        console.log("Health reduced by 5.");
        break;
      case "Lava": 
        playSound('lava.mp3'); 
        player.health = Math.max(0, player.health - 50);
        player.moves = Math.max(0, player.moves - 10);
        console.log("Health reduced by 50, Moves reduced by 10.");
        break;
      case "Mud": 
        playSound('dirtpath.mp3'); 
        player.health = Math.max(0, player.health - 10);
        player.moves = Math.max(0, player.moves - 5);
        console.log("Health reduced by 10, Moves reduced by 5.");
        break;
      case "Victory": 
         player.moves = Math.max(0, player.moves - 1); // Reduce moves for the tile
        console.log("Moved to Victory."); // Check victory condition AFTER reducing moves for the tile
        if (player.moves > 0) 
		{
          victory(gamePlayer); // Use the global gamePlayer object
          return; // Stop further execution in this call if won
        } else 
		{
             console.log("Reached Victory Tile but not enough moves left for the tile's effect.");
        }
        break;
    }
  } else 
  {
    console.log("Player is not on a recognized tile.");
  }
 updatePlayerStatsDisplay(gamePlayer); 
  if (player.health <= 0 || player.moves <= 0) 
  {
    gameOver(player); // Pass player to gameOver function
  }
}

/**
 * Handles the victory condition of the game.
 */
function victory(player) 
{
   player.activeGame = false;
   playSound('congratulations.mp3'); // Play victory sound
  alert("Congratulations, you won!");
  setTimeout(() => 
  {
    StartGame(); // Refreshes the page
  }, 5000); // 5000 milliseconds = 5 seconds
}
/**
 * Handles the game over condition.
 * @param {Player} player - The player object.
 */
function gameOver(player)
 {
  player.activeGame = false;
  playSound('failure.mp3'); 
  alert("Game Over");
  setTimeout(() => 
  {
	StartGame();
  }, 5000); 
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
function initializePlayer() 
{
  return new Player(200, 450, [0, 0], true);
}

function playSound(soundFile) 
{
    const audio = new Audio(soundFile);
    audio.play().catch(error => 
	{
        console.error("Error playing sound:", soundFile, error); // This catch is important because browsers might block autoplay until the user interacts with the page.
    });
}
