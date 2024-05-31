# katomaran

** Drive Link explaining the projects ** : https://drive.google.com/drive/folders/1lJsUjNs51-sjXmRNMkovguT68Fpuz_G_?usp=drive_link


**Pygame Simulation Projects**

This repository contains two Python applications using Pygame. Each application demonstrates different aspects of robotic simulation and pathfinding within a grid environment.

**Project 1: Multiple Robots Movement Simulation**


This Python application utilizes Pygame to create a visual simulation where multiple robots move towards the centroid of a user-defined rectangle on the screen.

Features

**Interactive Rectangle Definition**: Users define the corners of a rectangle by clicking, and the application calculates the centroid.
**Robot Placement and Animation**: Place multiple robots that animate towards the rectangle's centroid upon a right-click.
**Dynamic Text Display**: Coordinates of rectangle corners and the centroid are displayed.


Controls
Left Click: Define corners of the rectangle or place robots.
Right Click: Initiate robot movement towards the centroid.




**Project 2: A* Pathfinding Simulation**


This Python application uses Pygame to simulate a robot navigating through a 10x10 grid. The pathfinding is performed using the A* algorithm, considering randomly generated obstacles within the grid.

**Features**
**Grid and Obstacle Setup**: A 10x10 grid where obstacles are randomly placed.
**Interactive Start and End Points**: Users click to set the start and end points for the robot's journey.
**A* Pathfinding**: Implements A* algorithm to find the shortest path avoiding obstacles.
**Animation**: Animates the robot moving along the calculated path.


Controls
Mouse Click: Define the start point with the first click and the end point with the second click.



Dependencies
Python 3.x
Pygame
Images (e.g., robot.png should be in the project directory)


Additional Notes
Ensure robot.png is in the same directory as the scripts for the second project.
Obstacles are randomly generated each time the application is launched.
