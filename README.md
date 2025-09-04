# Rotating Shape Matching
Game idea 1:
Controls:
* Space: Reset level.
* Left: Rotate grid 90 degrees left and switch cursor (if multiple).
* Right: Rotate grid 90 degrees right and switch cursor (if multiple).
* Up: Move cursor up, drawing one cell.
  
Debug Controls:
* S: Skip Level
* Down: Undo cursor move
  
Mechanic 1: Grid Rotation
* Concept: Pressing left rotates a 15x15 grid clockwise by 90 degrees.
* Visual: The grid, including the target shape and drawn shape, rotate 90 degrees around the center.

Mechanic 2: Shape Creation
* Concept: Pressing up moves the player's cursor, which starts in the center of the top left quadrant, up one cell, leaving the cell it left red.
* Visual: The cursor is pink, the drawn shape is red.
* Learning: The player must learn that they can draw two dimensional shapes by combining grid rotation and cursor movement.

Mechanic 3: Matching Target Shape
* Concept: A target shape is created using a random walk function in the bottom left quadrant.  The player must create a shape that corresponds to this target shape.
* Simple: The shapes correspond exactly as they appear.
* Complex: The shapes must correspond in accordance to their rotation, so the target shape must be rotated 180 degrees. 
* Visual: The target shape is blue and drawn in the bottom left on a black background (same as player's) when simple matching is required.  The target shape is blue and drawn in the bottom right on a white background (opposite player's) when complex matching is required.  When the shapes match the screen flashes red and a new level is displayed.
* Learning: The player must learn how their drawn shape should correspond to the target shape.

Mechanic 4: Cursor Switching
* Concept: Pressing right rotates the grid counter clockwise by 90 degrees and moves the cursor from one quadrant to another. 
* Visual: Two target shapes, in blue and green, are drawn in the bottom left and right quadrants.  Two cursors, pink and yellow, are used to draw two shapes, red and orange, in the top left and top right quadrants.
* Learning: The player must learn to switch between cursors, positioning them correctly prior to switching, and draw two shapes, one which corresponds simply and the other which corresponds complexly, to two target shapes.



Level 1: Simple 4-cell target shape, simple correspondence.
Level 2: Complex 12 cell target shape, simple correspondence.
Level 3: Simple 4 cell target shape, complex correspondence. 
Level 4: Complex 12 cell target shape, complex correspondence. 
Level 5: Two simple 4 cell target shapes, simple and complex correspondence.
Level 6: Two complex 12 cell target shapes, simple and complex correspondence.
