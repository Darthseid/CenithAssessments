 /**
 * Renders a basic text representation of the map, including player position.
 * @param {Map} map - The map object.
 * @param {Player} player - The player object.
 */
function renderMap(map, player) {
    const container = document.getElementById('map-representation');
    container.innerHTML = '';

    for (let y = 0; y < map.height; y++) {
        const row = document.createElement('div');
        row.style.display = 'flex';

        for (let x = 0; x < map.width; x++) {
            const img = document.createElement('img');
            img.width = 16;
            img.height = 16;
            img.id = `tile-${x}-${y}`;

            if (player.coordinates[0] === x && player.coordinates[1] === y) 
			{
                img.src = 'Car.jpg';
                img.alt = 'P';
            } else 
			{
                const tile = map.getTileAt(x, y);
                img.src = getTileImage(tile.name);
                img.alt = tile?.name?.[0] ?? '?';
            }
            row.appendChild(img);
        }
        container.appendChild(row);
    }
}

function getTileImage(tileName) 
{
    switch (tileName) {
        case "Blank": return 'Blank.jpg';
        case "Speeder": return 'Speeder.png';
        case "Lava": return 'lava.png';
        case "Mud": return 'Mud.jpg';
        case "Victory": return 'Finish.png';
        default: return 'unknown.png';
    }
}

let gameMap;
let seed;
let gamePlayer; // Global game objects 

function StartGame() 
{
    seed = Date.now(); // Use fresh seed based on current system time.
    gameMap = generateMap(seed);
    gamePlayer = initializePlayer();
    renderMap(gameMap, gamePlayer);
    updatePlayerStatsDisplay(gamePlayer);
}

window.addEventListener('DOMContentLoaded', () => {
    StartGame();
    document.getElementById('restart-button').addEventListener('click', StartGame);
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

    
    if (isShift && key === 'ArrowRight')  // Determine movement direction based on key and modifiers
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
       
        if (key === 'ArrowUp')   // Orthogonal Movement
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
    const oldX = gamePlayer.coordinates[0];
    const oldY = gamePlayer.coordinates[1];
    const newX = oldX + deltaX;
    const newY = oldY + deltaY;
    const isMoveValid = newX >= 0 && newX < gameMap.width &&
                        newY >= 0 && newY < gameMap.height;
    if (isMoveValid) 
	{
        gamePlayer.coordinates = [newX, newY];
        executeTile(gamePlayer, gameMap);
        updatePlayerPosition(oldX, oldY, newX, newY, gameMap);
    } else 
	{
        console.log("Cannot move off the map.");
    }
    event.preventDefault();
}
    }
window.addEventListener('keydown', handlePlayerMovement); // Add event listener for player movement

function updatePlayerPosition(oldX, oldY, newX, newY, map)
 {
    const oldTile = map.getTileAt(oldX, oldY);
    const oldImg = document.getElementById(`tile-${oldX}-${oldY}`);
    if (oldImg && oldTile) {
        oldImg.src = getTileImage(oldTile.name);
        oldImg.alt = oldTile.name[0];
    }

    const newImg = document.getElementById(`tile-${newX}-${newY}`);
    if (newImg) {
        newImg.src = 'Car.jpg';
        newImg.alt = 'P';
    }
}
