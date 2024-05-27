import pygame
import sys
import random
import heapq

# Initialize Pygame
pygame.init()

# Set up display
CELL_SIZE = 50  # Size of each grid cell in pixels
GRID_WIDTH, GRID_HEIGHT = 10, 10  # Number of cells in the grid
WINDOW_SIZE = (GRID_WIDTH * CELL_SIZE, GRID_HEIGHT * CELL_SIZE)
window = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("10x10 Grid")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

robot_image = pygame.image.load("robot.png").convert_alpha()
robot_image = pygame.transform.scale(robot_image, (CELL_SIZE, CELL_SIZE))  # Resize the image to match cell size

# Function to draw the grid and randomly color 30 cells
def draw_grid(surface, filled_cells, start=None, end=None, path=None):
    for x in range(0, WINDOW_SIZE[0], CELL_SIZE):
        for y in range(0, WINDOW_SIZE[1], CELL_SIZE):
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            if (x // CELL_SIZE, y // CELL_SIZE) == start:
                pygame.draw.rect(surface, GREEN, rect)
            elif (x // CELL_SIZE, y // CELL_SIZE) == end:
                pygame.draw.rect(surface, RED, rect)
            elif (x // CELL_SIZE, y // CELL_SIZE) in filled_cells:
                pygame.draw.rect(surface, WHITE, rect)
            elif path and (x // CELL_SIZE, y // CELL_SIZE) in path:
                pygame.draw.rect(surface, BLUE, rect)
            else:
                pygame.draw.rect(surface, BLACK, rect)
            pygame.draw.rect(surface, WHITE, rect, 1)  # Draw grid lines

    # Draw the robot image at the start point
    if start:
        surface.blit(robot_image, (start[0] * CELL_SIZE, start[1] * CELL_SIZE))


# Function to animate the robot along the calculated path
def animate_robot(surface, path):
    for i in range(len(path) - 1):
        # Calculate the difference between the current and next cell
        dx = (path[i + 1][0] - path[i][0]) * CELL_SIZE
        dy = (path[i + 1][1] - path[i][1]) * CELL_SIZE
        # Animate the robot
        for j in range(CELL_SIZE):
            surface.fill(BLACK)  # Clear the screen
            draw_grid(surface, obstacles, start_point, end_point, path)  # Redraw the grid and path
            # Blit the robot at the current position with an offset based on the progress of animation
            surface.blit(robot_image, (path[i][0] * CELL_SIZE + j * dx // CELL_SIZE,
                                       path[i][1] * CELL_SIZE + j * dy // CELL_SIZE))
            pygame.display.flip()  # Update the display
            pygame.time.delay(10)  # Delay for smoother animation


# Get neighboring cells
def neighbors(cell):
    x, y = cell
    neighbors_list = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
    # Filter out neighbors that are outside the grid boundaries or occupied by obstacles
    neighbors_list = [(x, y) for x, y in neighbors_list if
                      0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT and (x, y) not in obstacles]
    return neighbors_list


# A* algorithm function
def astar(start, end, obstacles):
    if start in obstacles or end in obstacles:
        return None  # If start or end point is an obstacle, return None

    open_list = []
    closed_set = set()
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, end)}

    heapq.heappush(open_list, (f_score[start], start))

    while open_list:
        current = heapq.heappop(open_list)[1]

        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)  # Add the start point to the path
            path.reverse()  # Reverse the path to get it from start to end
            return path

        closed_set.add(current)

        for neighbor in neighbors(current):
            tentative_g_score = g_score[current] + 1

            if neighbor in closed_set:
                continue

            if neighbor not in [i[1] for i in open_list] or tentative_g_score < g_score.get(neighbor, 0):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, end)
                heapq.heappush(open_list, (f_score[neighbor], neighbor))

    return None


# Heuristic function (Manhattan distance)
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


# Generate a set of 30 random cells to be obstacle
obstacles = set()
while len(obstacles) < 30:
    cell = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
    obstacles.add(cell)

print('obstacles', obstacles)

start_point = None
end_point = None

# Main loop
running = True
path_found = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            grid_x = mouse_x // CELL_SIZE
            grid_y = mouse_y // CELL_SIZE
            if start_point is None:
                start_point = (grid_x, grid_y)
                print("Start Point:", start_point)
            elif end_point is None:
                if (grid_x, grid_y) != start_point:
                    end_point = (grid_x, grid_y)
                    print("End Point:", end_point)

    window.fill(BLACK)  # Fill the window with black
    draw_grid(window, obstacles, start_point, end_point)  # Draw the grid with start and end points

    if start_point and end_point:
        path = astar(start_point, end_point, obstacles)
        if path:
            draw_grid(window, obstacles, start_point, end_point, path)  # Draw the path if found
            path_found = True
        else:
            print("Path cannot be found due to obstacles around the starting point.")
            path_found = False

    pygame.display.flip()  # Update the display

# Print the shortest path coordinates if path was found
if path_found:
    print("Shortest path coordinates:", path)
    animate_robot(window, path)
else:
    print("No valid path found.")

# Quit pygame
pygame.quit()
sys.exit()
