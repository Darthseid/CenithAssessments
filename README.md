# CenithAssessments
This Repository was created by Jared McVey to fulfill the Assignments given by Cenith Innovations. Technically, only one assignment was necessary; but I loved the challenge so I took the extra time to perform all three of them. Assignment One was completed in HTML/Javascript while Assignment Two & Three used Python. Stock tile images and sound effects were used to enhance the fun.

To play each game, download the repo and use the arrow keys as instructed. GridGame.py and McVeyAssignmentOne.html are the executable files. Holding Shift and loving left and right also moves the player (car icon) upward. Holding Ctrl while moving left or right also moves the player (car) downward. The Python game requires Python 3. Also check the console when using the Solver for the Python game.

Below is a copy of the problems to solve: 

PROBLEM:
In a 50 by 50 2-D grid world, you are given a starting point A on one side of the grid, and an ending point B on the other side of the grid.  Your objective is to get from point A to point B.  Each grid space can be in a state of [“Blank”, “Speeder”, “Lava”, “Mud”].  You start out with 200 points of health and 450 moves.  Below is a mapping of how much your health and moves are affected by landing on a grid space.

[
  “Blank”: {“Health”: 0, “Moves”: -1},
  “Speeder”: {“Health”: -5, “Moves”: 0},
  “Lava”: {“Health”: -50, “Moves”: -10},
  “Mud”: {“Health”: -10, “Moves”: -5},
]

Assignment 1
Build a front end application, in any modern front end language or framework, that allows a player to use the arrow keys to play this game.

Assignment 2
Build a back end API using Node.js (w/ Typescript), or Python, or something similar, that allows a player to save the game and come back to it later.  As well as returns any relevant data to the front end such as where the player is on the board, what the board is configured like, how much health or moves are left, etc.  Try to include business logic such as logic on how the board is initially configured and the change of state of the board / players as well.  We expect to be able to play the game over your API.

Assignment 3
Build an application in any language (no UI necessary, terminal output is great), that checks whether (a) The grid world level is solvable for a given grid world level to get from point A to point B, and (b) What the most efficient route is to get across if it is solvable, in order to minimize health damage and moves it takes to get from point A to point B.

