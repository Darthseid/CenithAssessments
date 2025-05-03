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
  console.log(`Player Stats: Health = ${player.health}, Moves = ${player.moves}`);
   // Check for game over condition at the end of tile execution
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