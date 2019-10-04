# 3D Raycasting


Using pygame library to make a 3d game.

Using the raycasting method to rended the 3D view from a top down view:

1. Player class that has a certain field of whiew
2. In that field of view the player emmits rays.
3. Rays check if they intersect with any walls(lines) and output the points of intersection https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection
4. Render rectangles that decrease in brightness and size the further the intersection is from the player
5. Order the rectangles in a new window from left to right so they show what the player sees.
