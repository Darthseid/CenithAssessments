 /**
 * Renders a basic text representation of the map, including player position.
 * @param {Map} map - The map object.
 * @param {Player} player - The player object.
 */
function renderMap(map, player) 
{
    const container = document.getElementById('map-representation');
    container.innerHTML = ''; // Clear old map
    for (let y = 0; y < map.height; y++) 
	{
        const row = document.createElement('div');
        row.style.display = 'flex';
        for (let x = 0; x < map.width; x++) 
		{
            const img = document.createElement('img');
            img.width = 16;
            img.height = 16;
            if (player.coordinates[0] === x && player.coordinates[1] === y) {
                img.src = 'Car.jpg'; // Player image
                img.alt = 'P';
            } else 
			{
                const tile = map.getTileAt(x, y);
                if (tile) 
				{
                    switch (tile.name) 
					{
                        case "Blank":
                            img.src = 'Blank.jpg';
                            img.alt = '.';
                            break;
                        case "Speeder":
                            img.src = 'Speeder.png';
                            img.alt = 'S';
                            break;
                        case "Lava":
                            img.src = 'lava.png';
                            img.alt = 'L';
                            break;
                        case "Mud":
                            img.src = 'Mud.jpg';
                            img.alt = 'M';
                            break;
                        case "Victory":
                            img.src = 'Finish.png';
                            img.alt = 'V';
                            break;
                        default:
                            img.src = 'unknown.png';
                            img.alt = '?';
                            break;
                    }
                } else 
				{
                    img.src = 'unknown.png';
                    img.alt = '?';
                }
            }
            row.appendChild(img);
        }
        container.appendChild(row);
    }
}


let gameMap;
let gamePlayer; // Global game objects 


window.addEventListener('DOMContentLoaded', () => {
    gameMap = generateMap(Date.now());
    gamePlayer = initializePlayer();
    renderMap(gameMap, gamePlayer);
    updatePlayerStatsDisplay(gamePlayer);
});


/**
 * Handles player movement based on arrow key presses and modifier keys.
 * @param {Event} event - The keyboard event.
 */
function handlePlayerMovement(event) 
{
    if (!gamePlayer || !gamePlayer.activeGame) 
	{
        return; // Don't process movement if game objects not initialized or game is not active
    }

    const key = event.key;
    const isShift = event.shiftKey;
    const isCtrl = event.ctrlKey;

    let deltaX = 0;
    let deltaY = 0;
    let moved = false;

    // Determine movement direction based on key and modifiers
    if (isShift && key === 'ArrowRight') 
	{
        deltaX = 1;
        deltaY = -1; // Northeast
        moved = true;
    } else if (isShift && key === 'ArrowLeft') 
	{
        deltaX = -1;
        deltaY = -1; // Northwest
        moved = true;
    } else if (isCtrl && key === 'ArrowRight') 
	{
        deltaX = 1;
        deltaY = 1; // Southeast
        moved = true;
    } else if (isCtrl && key === 'ArrowLeft') 
	{
        deltaX = -1;
        deltaY = 1; // Southwest
        moved = true;
    } else if (!isShift && !isCtrl) 
	{
        // Handle cardinal movements only if no Shift or Ctrl is held
        if (key === 'ArrowUp') 
		{
            deltaY = -1;
            moved = true;
        } else if (key === 'ArrowDown') 
		{
            deltaY = 1;
            moved = true;
        } else if (key === 'ArrowLeft') 
		{
            deltaX = -1;
            moved = true;
        } else if (key === 'ArrowRight') 
		{
            deltaX = 1;
            moved = true;
        }
    }

    if (moved) 
	{
        const newX = gamePlayer.coordinates[0] + deltaX;
        const newY = gamePlayer.coordinates[1] + deltaY; // If a valid movement key combination was pressed
        const isMoveValid = newX >= 0 && newX < gameMap.width &&
                             newY >= 0 && newY < gameMap.height; // Check if the new coordinates are within map bounds

        if (isMoveValid) 
		{
            gamePlayer.coordinates = [newX, newY];
            executeTile(gamePlayer, gameMap); // Execute tile effect after moving
            renderMap(gameMap, gamePlayer); // Re-render map after movement
        } else 
		{
            console.log("Cannot move off the map.");
        }
        event.preventDefault(); // Prevent default arrow key scrolling
    }
}
window.addEventListener('keydown', handlePlayerMovement); // Add event listener for player movement
