import pygame
import sys
from pygame.locals import *

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Multiple Robots Movement")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

font = pygame.font.SysFont(None, 24)

rectangle_points = []
robot_positions = []
drawing_line = False
robot_movement_started = []
paths = []


def draw_rectangle(points):
    if len(points) == 4:
        pygame.draw.lines(screen, BLACK, True, points, 1)


def calculate_centroid(points):
    x_coords = [p[0] for p in points]
    y_coords = [p[1] for p in points]
    centroid = (sum(x_coords) // len(points), sum(y_coords) // len(points))
    return centroid


def move_robot_stepwise(start_pos, end_pos):
    x1, y1 = start_pos
    x2, y2 = end_pos
    path = []
    while x1 != x2:
        if x1 < x2:
            x1 += 1
        else:
            x1 -= 1
        path.append((x1, y1))
    while y1 != y2:
        if y1 < y2:
            y1 += 1
        else:
            y1 -= 1
        path.append((x1, y1))
    return path


def animate_robot_movement(path, robot_index):
    for pos in path:
        pygame.draw.circle(screen, RED, pos, 5)
        pygame.display.update()
        pygame.time.delay(10)
    robot_positions[robot_index] = path[-1]


def render_text(text, position):
    img = font.render(text, True, BLUE)
    screen.blit(img, position)


# Main loop
running = True
while running:
    screen.fill(WHITE)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                if len(rectangle_points) < 4:
                    rectangle_points.append(event.pos)
                elif len(rectangle_points) == 4:
                    robot_positions.append(event.pos)
                    robot_movement_started.append(False)
                    paths.append([])
            elif event.button == 3:  # Right click
                if len(rectangle_points) == 4 and robot_positions:
                    drawing_line = True

    draw_rectangle(rectangle_points)
    for point in rectangle_points:
        pygame.draw.circle(screen, GREEN, point, 5)
    if len(rectangle_points) == 4:
        render_text(f"Pillar Corners: {rectangle_points}", (10, 10))
        centroid = calculate_centroid(rectangle_points)
        render_text(f"Center (Centroid): {centroid}", (10, 30))

    for pos in robot_positions:
        pygame.draw.circle(screen, RED, pos, 5)

    if drawing_line:
        for i in range(len(robot_positions)):
            if not robot_movement_started[i]:
                paths[i] = move_robot_stepwise(robot_positions[i], centroid)
                animate_robot_movement(paths[i], i)
                robot_movement_started[i] = True

    pygame.display.update()
