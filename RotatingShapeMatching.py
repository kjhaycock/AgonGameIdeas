#Important Note: Random shapes used for demo purposes, final game would use an array of shapes which would be cycled through to ensure it is deterministic.

import pygame
import sys
import random
import numpy as np

pygame.init()

GRID_SIZE = 15
SQUARE_SIZE = 40
MARGIN = 2
WINDOW_SIZE = (GRID_SIZE * (SQUARE_SIZE + MARGIN) + MARGIN, 
               (GRID_SIZE + 1) * (SQUARE_SIZE + MARGIN) + MARGIN)

WHITE = (255, 255, 255)
LIGHT_GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)  
PINK = (255, 192, 203)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)

screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Rotating Shape Matching")

CENTER_ROW = GRID_SIZE // 2
CENTER_COL = GRID_SIZE // 2

def create_base_grid():
    grid = np.empty((GRID_SIZE + 1, GRID_SIZE), dtype=object)
    
    for i in range(GRID_SIZE + 1):
        for j in range(GRID_SIZE):
            grid[i, j] = WHITE
    
    for j in range(GRID_SIZE):
        grid[0, j] = LIGHT_GRAY
    grid[0, 0] = PINK
    
    for i in range(1, GRID_SIZE + 1):
        for j in range(GRID_SIZE):
            if (i - 1) == CENTER_ROW or j == CENTER_COL:
                grid[i, j] = LIGHT_GRAY
    
    mid_row = GRID_SIZE // 2
    mid_col = GRID_SIZE // 2
    
    for i in range(1, GRID_SIZE + 1):
        for j in range(GRID_SIZE):
            main_i = i - 1
            if (main_i < mid_row and j > mid_col) or (main_i > mid_row and j < mid_col):
                grid[i, j] = BLACK
    
    cursor_i = 1 + (mid_row // 2)
    cursor_j = mid_col + (GRID_SIZE - mid_col) // 2
    grid[cursor_i, cursor_j] = PINK
    
    return grid, (cursor_i, cursor_j)

def define_target_shape(grid, level):
    mid_row = GRID_SIZE // 2
    mid_col = GRID_SIZE // 2
    
    if level in [1, 2]:
        quadrant_start_i = 1 + mid_row + 1
        quadrant_end_i = GRID_SIZE
        quadrant_start_j = 0
        quadrant_end_j = mid_col - 1
        
        center_i = (quadrant_start_i + quadrant_end_i) // 2
        center_j = (quadrant_start_j + quadrant_end_j) // 2
        
        if level == 1:
            num_cells = 4
        else:
            num_cells = 12
            
        shape_cells = create_shape_in_quadrant(quadrant_start_i, quadrant_end_i, 
                                              quadrant_start_j, quadrant_end_j, 
                                              center_i, center_j, num_cells)
        
        for cell in shape_cells:
            i, j = cell
            if 1 <= i < GRID_SIZE + 1 and 0 <= j < GRID_SIZE:
                grid[i, j] = BLUE
                
        return grid, shape_cells
    
    elif level in [3, 4]:
        quadrant_start_i = 1 + mid_row + 1
        quadrant_end_i = GRID_SIZE
        quadrant_start_j = mid_col + 1
        quadrant_end_j = GRID_SIZE - 1
        
        center_i = (quadrant_start_i + quadrant_end_i) // 2
        center_j = (quadrant_start_j + quadrant_end_j) // 2
        
        if level == 3:
            num_cells = 4
        else:
            num_cells = 12
            
        shape_cells = create_shape_in_quadrant(quadrant_start_i, quadrant_end_i, 
                                              quadrant_start_j, quadrant_end_j, 
                                              center_i, center_j, num_cells)
        
        for cell in shape_cells:
            i, j = cell
            if 1 <= i < GRID_SIZE + 1 and 0 <= j < GRID_SIZE:
                grid[i, j] = GREEN
                
        return grid, shape_cells
    
    else:
        num_cells = 4 if level == 5 else 12
        
        quadrant1_start_i = 1 + mid_row + 1
        quadrant1_end_i = GRID_SIZE
        quadrant1_start_j = 0
        quadrant1_end_j = mid_col - 1
        
        center1_i = (quadrant1_start_i + quadrant1_end_i) // 2
        center1_j = (quadrant1_start_j + quadrant1_end_j) // 2
        
        shape1_cells = create_shape_in_quadrant(quadrant1_start_i, quadrant1_end_i, 
                                               quadrant1_start_j, quadrant1_end_j, 
                                               center1_i, center1_j, num_cells)
        
        for cell in shape1_cells:
            i, j = cell
            if 1 <= i < GRID_SIZE + 1 and 0 <= j < GRID_SIZE:
                grid[i, j] = BLUE
        
        quadrant2_start_i = 1 + mid_row + 1
        quadrant2_end_i = GRID_SIZE
        quadrant2_start_j = mid_col + 1
        quadrant2_end_j = GRID_SIZE - 1
        
        center2_i = (quadrant2_start_i + quadrant2_end_i) // 2
        center2_j = (quadrant2_start_j + quadrant2_end_j) // 2
        
        shape2_cells = create_shape_in_quadrant(quadrant2_start_i, quadrant2_end_i, 
                                               quadrant2_start_j, quadrant2_end_j, 
                                               center2_i, center2_j, num_cells)
        
        for cell in shape2_cells:
            i, j = cell
            if 1 <= i < GRID_SIZE + 1 and 0 <= j < GRID_SIZE:
                grid[i, j] = GREEN
                
        return grid, (shape1_cells, shape2_cells)

def create_shape_in_quadrant(start_i, end_i, start_j, end_j, center_i, center_j, num_cells):
    shape_cells = [(center_i, center_j)]
    current_i, current_j = center_i, center_j
    
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    while len(shape_cells) < num_cells:
        di, dj = random.choice(directions)
        new_i, new_j = current_i + di, current_j + dj
        
        if (start_i <= new_i <= end_i and 
            start_j <= new_j <= end_j and 
            (new_i, new_j) not in shape_cells):
            
            shape_cells.append((new_i, new_j))
            current_i, current_j = new_i, new_j
            
    return shape_cells

def move_cursor(grid, cursor_pos, direction, previous_positions, target_shape, level, active_cursor):
    cursor_i, cursor_j = cursor_pos
    new_i, new_j = cursor_i, cursor_j
    
    if direction == "up":
        new_i = max(1, cursor_i - 1)
        original_color = grid[new_i, new_j]
        previous_positions.append((cursor_pos, original_color))
        
        if level in [1, 2]:
            grid[cursor_i, cursor_j] = RED
            grid[new_i, new_j] = PINK
        elif level in [3, 4]:
            grid[cursor_i, cursor_j] = ORANGE
            grid[new_i, new_j] = YELLOW
        else:
            if active_cursor == "pink":
                grid[cursor_i, cursor_j] = RED
                grid[new_i, new_j] = PINK
            else:
                grid[cursor_i, cursor_j] = ORANGE
                grid[new_i, new_j] = YELLOW
            
        return grid, (new_i, new_j), previous_positions
    elif direction == "down":
        if previous_positions:
            prev_pos, original_color = previous_positions.pop()
            grid[cursor_i, cursor_j] = get_original_color(grid, cursor_pos, target_shape, level, active_cursor)
            
            if level in [1, 2]:
                grid[prev_pos[0], prev_pos[1]] = PINK
            elif level in [3, 4]:
                grid[prev_pos[0], prev_pos[1]] = YELLOW
            else:
                if active_cursor == "pink":
                    grid[prev_pos[0], prev_pos[1]] = PINK
                else:
                    grid[prev_pos[0], prev_pos[1]] = YELLOW
                
            return grid, prev_pos, previous_positions
        return grid, cursor_pos, previous_positions
    
    return grid, cursor_pos, previous_positions

def get_original_color(grid, pos, target_shape, level, active_cursor=None):
    i, j = pos
    
    if i == 0:
        if j == 0:
            return PINK if level in [1, 2] or (active_cursor == "pink" and level > 4) else YELLOW
        return LIGHT_GRAY
    
    main_i = i - 1
    mid_row = GRID_SIZE // 2
    mid_col = GRID_SIZE // 2
    
    if main_i == mid_row or j == mid_col:
        return LIGHT_GRAY
    
    if (main_i < mid_row and j > mid_col) or (main_i > mid_row and j < mid_col):
        return BLACK
    
    if level > 4:
        shape1, shape2 = target_shape
        for cell in shape1:
            if (i, j) == cell:
                return BLUE
        for cell in shape2:
            if (i, j) == cell:
                return GREEN
    else:
        for cell in target_shape:
            if (i, j) == cell:
                return BLUE if level in [1, 2] else GREEN
    
    return WHITE

def rotate_point_clockwise(point):
    i, j = point
    if i == 0:
        return (i, j)
    
    center = (GRID_SIZE - 1) / 2
    i_centered = (i - 1) - center
    j_centered = j - center
    new_i = j_centered + center + 1
    new_j = -i_centered + center
    new_i = int(round(new_i))
    new_j = int(round(new_j))
    new_i = max(1, min(GRID_SIZE, new_i))
    new_j = max(0, min(GRID_SIZE - 1, new_j))
    return (new_i, new_j)

def rotate_point_counter_clockwise(point):
    i, j = point
    if i == 0:
        return (i, j)
    
    center = (GRID_SIZE - 1) / 2
    i_centered = (i - 1) - center
    j_centered = j - center
    new_i = -j_centered + center + 1
    new_j = i_centered + center
    new_i = int(round(new_i))
    new_j = int(round(new_j))
    new_i = max(1, min(GRID_SIZE, new_i))
    new_j = max(0, min(GRID_SIZE - 1, new_j))
    return (new_i, new_j)

def rotate_grid_clockwise(grid, cursor_pos, previous_positions):
    main_grid = grid[1:GRID_SIZE + 1, :].copy()
    
    rotated_main_grid = np.rot90(main_grid, k=3)
    
    rotated_grid = np.vstack([grid[0:1, :], rotated_main_grid])
    
    rotated_cursor = rotate_point_clockwise(cursor_pos)
    
    previous_positions.clear()
    return rotated_grid, rotated_cursor, previous_positions

def rotate_grid_counter_clockwise(grid, cursor_pos, previous_positions):
    main_grid = grid[1:GRID_SIZE + 1, :].copy()
    
    rotated_main_grid = np.rot90(main_grid, k=1)
    
    rotated_grid = np.vstack([grid[0:1, :], rotated_main_grid])
    
    rotated_cursor = rotate_point_counter_clockwise(cursor_pos)
    
    previous_positions.clear()
    return rotated_grid, rotated_cursor, previous_positions

def check_win_condition_complex(grid, target_shape, level):
    drawn_cells = []
    cursor_cell = None
    
    for i in range(GRID_SIZE + 1):
        for j in range(GRID_SIZE):
            if level in [1, 2]:
                if grid[i, j] == RED:
                    drawn_cells.append((i, j))
                elif grid[i, j] == PINK:
                    cursor_cell = (i, j)
            else:
                if grid[i, j] == ORANGE:
                    drawn_cells.append((i, j))
                elif grid[i, j] == YELLOW:
                    cursor_cell = (i, j)
    
    if cursor_cell:
        drawn_cells.append(cursor_cell)
    
    if len(drawn_cells) != len(target_shape):
        return False
    
    drawn_set = set(drawn_cells)
    
    if drawn_set == set(target_shape):
        return True
    
    rotated_90 = [rotate_point_clockwise(point) for point in target_shape]
    if drawn_set == set(rotated_90):
        return True
    
    rotated_180 = [rotate_point_clockwise(rotate_point_clockwise(point)) for point in target_shape]
    if drawn_set == set(rotated_180):
        return True
    
    rotated_270 = [rotate_point_counter_clockwise(point) for point in target_shape]
    if drawn_set == set(rotated_270):
        return True
    
    return False

def check_win_condition_simple(grid, target_shape):
    blue_cells = []
    red_cells = []
    
    for i in range(1, GRID_SIZE + 1):
        for j in range(GRID_SIZE):
            if grid[i, j] == BLUE:
                blue_cells.append((i, j))
            elif grid[i, j] == RED or grid[i, j] == PINK:
                red_cells.append((i, j))
    
    if len(red_cells) != len(blue_cells):
        return False
    
    def to_quadrant_coords(cells):
        if not cells:
            return []
            
        quadrant_coords = []
        for i, j in cells:
            if i < 9 and j < 7:
                quadrant_i = i - 1
                quadrant_j = j
            elif i < 9 and j >= 8:
                quadrant_i = i - 1
                quadrant_j = j - 8
            elif i >= 9 and j < 7:
                quadrant_i = i - 9
                quadrant_j = j
            else:
                quadrant_i = i - 9
                quadrant_j = j - 8
            
            quadrant_coords.append((quadrant_i, quadrant_j))
        
        min_i = min(coord[0] for coord in quadrant_coords)
        min_j = min(coord[1] for coord in quadrant_coords)
        
        normalized_coords = [(coord[0] - min_i, coord[1] - min_j) for coord in quadrant_coords]
        
        return sorted(normalized_coords)
    
    blue_quadrant_coords = to_quadrant_coords(blue_cells)
    red_quadrant_coords = to_quadrant_coords(red_cells)
    
    return blue_quadrant_coords == red_quadrant_coords

def check_win_condition_dual(grid, target_shapes):
    shape1, shape2 = target_shapes
    
    blue_cells = []
    red_cells = []
    
    for i in range(1, GRID_SIZE + 1):
        for j in range(GRID_SIZE):
            if grid[i, j] == BLUE:
                blue_cells.append((i, j))
            elif grid[i, j] == RED or grid[i, j] == PINK:
                red_cells.append((i, j))
    
    if len(red_cells) != len(blue_cells):
        return False
    
    drawn_cells = []
    cursor_cell = None
    
    for i in range(1, GRID_SIZE + 1):
        for j in range(GRID_SIZE):
            if grid[i, j] == ORANGE:
                drawn_cells.append((i, j))
            elif grid[i, j] == YELLOW:
                cursor_cell = (i, j)
    
    if cursor_cell:
        drawn_cells.append(cursor_cell)
    
    if len(drawn_cells) != len(shape2):
        return False
    
    drawn_set = set(drawn_cells)
    
    if (drawn_set == set(shape2) or
        drawn_set == set([rotate_point_clockwise(point) for point in shape2]) or
        drawn_set == set([rotate_point_clockwise(rotate_point_clockwise(point)) for point in shape2]) or
        drawn_set == set([rotate_point_counter_clockwise(point) for point in shape2])):
        
        return check_win_condition_simple(grid, shape1)
    
    return False

def end_game(grid):
    for i in range(GRID_SIZE + 1):
        for j in range(GRID_SIZE):
            grid[i, j] = RED
    return grid

def reset_level(level):
    grid, cursor_pos = create_base_grid()
    
    if level > 4:
        grid, target_shapes = define_target_shape(grid, level)
        
        mid_row = GRID_SIZE // 2
        mid_col = GRID_SIZE // 2
        
        pink_cursor_i = 1 + (mid_row // 2)
        pink_cursor_j = mid_col + (GRID_SIZE - mid_col) // 2
        grid[pink_cursor_i, pink_cursor_j] = PINK
        
        yellow_cursor_i = 1 + (mid_row // 2)
        yellow_cursor_j = mid_col // 2
        grid[yellow_cursor_i, yellow_cursor_j] = YELLOW
        
        cursor_pos = (pink_cursor_i, pink_cursor_j)
        
        for j in range(GRID_SIZE):
            if j < level:
                grid[0, j] = RED
            elif j == level:
                grid[0, j] = PINK
            else:
                grid[0, j] = LIGHT_GRAY
                
        return grid, target_shapes, cursor_pos, [], "pink"
    else:
        grid, target_shape = define_target_shape(grid, level)
        
        for j in range(GRID_SIZE):
            if j < level:
                grid[0, j] = RED
            elif j == level:
                if level in [1, 2]:
                    grid[0, j] = PINK
                else:
                    grid[0, j] = YELLOW
            else:
                grid[0, j] = LIGHT_GRAY
        
        if level in [3, 4]:
            mid_row = GRID_SIZE // 2
            mid_col = GRID_SIZE // 2
            
            cursor_i = 1 + (mid_row // 2)
            cursor_j = mid_col // 2
            
            if grid[cursor_pos[0], cursor_pos[1]] == PINK:
                grid[cursor_pos[0], cursor_pos[1]] = get_original_color(grid, cursor_pos, target_shape, level, "pink")
            
            grid[cursor_i, cursor_j] = YELLOW
            cursor_pos = (cursor_i, cursor_j)
        
        return grid, target_shape, cursor_pos, [], "pink" if level in [1, 2] else "yellow"

def draw_grid(grid):
    screen.fill(BLACK)
    for row in range(GRID_SIZE + 1):
        for column in range(GRID_SIZE):
            color = grid[row, column]
            pygame.draw.rect(
                screen,
                color,
                [
                    MARGIN + (MARGIN + SQUARE_SIZE) * column,
                    MARGIN + (MARGIN + SQUARE_SIZE) * row,
                    SQUARE_SIZE,
                    SQUARE_SIZE
                ]
            )
    pygame.display.flip()

def flash_screen():
    for _ in range(3):
        screen.fill(GREEN)
        pygame.display.flip()
        pygame.time.delay(100)
        draw_grid(grid)
        pygame.display.flip()
        pygame.time.delay(100)
        
        for j in range(GRID_SIZE):
            if j < current_level:
                grid[0, j] = RED
            elif j == current_level:
                if current_level in [1, 2]:
                    grid[0, j] = PINK
                else:
                    grid[0, j] = YELLOW
            else:
                grid[0, j] = LIGHT_GRAY

current_level = 1
grid, target_shape, cursor_pos, previous_positions, active_cursor = reset_level(current_level)

clock = pygame.time.Clock()
running = True
game_won = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if current_level > 4:
                    if active_cursor == "pink":
                        grid[cursor_pos[0], cursor_pos[1]] = RED
                        for i in range(1, GRID_SIZE + 1):
                            for j in range(GRID_SIZE):
                                if grid[i, j] == YELLOW:
                                    cursor_pos = (i, j)
                                    active_cursor = "yellow"
                                    grid[0, current_level] = YELLOW
                                    break
                    else:
                        grid, cursor_pos, previous_positions = rotate_grid_counter_clockwise(grid, cursor_pos, previous_positions)
                else:
                    grid, cursor_pos, previous_positions = rotate_grid_counter_clockwise(grid, cursor_pos, previous_positions)
                draw_grid(grid)
            elif event.key == pygame.K_RIGHT:
                if current_level > 4:
                    if active_cursor == "yellow":
                        grid[cursor_pos[0], cursor_pos[1]] = ORANGE
                        for i in range(1, GRID_SIZE + 1):
                            for j in range(GRID_SIZE):
                                if grid[i, j] == PINK:
                                    cursor_pos = (i, j)
                                    active_cursor = "pink"
                                    grid[0, current_level] = PINK
                                    break
                    else:
                        grid, cursor_pos, previous_positions = rotate_grid_clockwise(grid, cursor_pos, previous_positions)
                else:
                    grid, cursor_pos, previous_positions = rotate_grid_clockwise(grid, cursor_pos, previous_positions)
                draw_grid(grid)
            elif event.key == pygame.K_UP:
                grid, cursor_pos, previous_positions = move_cursor(grid, cursor_pos, "up", previous_positions, target_shape, current_level, active_cursor)
                draw_grid(grid)
            elif event.key == pygame.K_DOWN:
                grid, cursor_pos, previous_positions = move_cursor(grid, cursor_pos, "down", previous_positions, target_shape, current_level, active_cursor)
                draw_grid(grid)
            elif event.key == pygame.K_SPACE:
                if current_level > 4:
                    grid, target_shape, cursor_pos, previous_positions, active_cursor = reset_level(current_level)
                else:
                    grid, target_shape, cursor_pos, previous_positions, _ = reset_level(current_level)
                game_won = False
                draw_grid(grid)
            elif event.key == pygame.K_s:
                if current_level < 6:
                    current_level += 1
                    if current_level > 4:
                        grid, target_shape, cursor_pos, previous_positions, active_cursor = reset_level(current_level)
                    else:
                        grid, target_shape, cursor_pos, previous_positions, _ = reset_level(current_level)
                    game_won = False
                    draw_grid(grid)
                else:
                    grid = end_game(grid)
                    game_won = True
                    draw_grid(grid)
    
    if not game_won:
        if current_level in [1, 2]:
            if check_win_condition_simple(grid, target_shape):
                flash_screen()
                
                if current_level < 6:
                    current_level += 1
                    if current_level > 4:
                        grid, target_shape, cursor_pos, previous_positions, active_cursor = reset_level(current_level)
                    else:
                        grid, target_shape, cursor_pos, previous_positions, _ = reset_level(current_level)
                else:
                    grid = end_game(grid)
                    game_won = True
        elif current_level in [3, 4]:
            if check_win_condition_complex(grid, target_shape, current_level):
                flash_screen()
                
                if current_level < 6:
                    current_level += 1
                    if current_level > 4:
                        grid, target_shape, cursor_pos, previous_positions, active_cursor = reset_level(current_level)
                    else:
                        grid, target_shape, cursor_pos, previous_positions, _ = reset_level(current_level)
                else:
                    grid = end_game(grid)
                    game_won = True
        else:
            if check_win_condition_dual(grid, target_shape):
                flash_screen()
                
                if current_level < 6:
                    current_level += 1
                    grid, target_shape, cursor_pos, previous_positions, active_cursor = reset_level(current_level)
                else:
                    grid = end_game(grid)
                    game_won = True
    
    draw_grid(grid)
    clock.tick(30)

pygame.quit()
sys.exit()
