import pygame
import math
import random

pygame.init()

# Window setup
FPS = 60
clock = pygame.time.Clock()

WIDTH = 1280
HEIGHT = 720
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Circle collision!")

# Colors
WHITE = 255, 255, 255,
BLACK = 0, 0, 0,
RED = 255, 0, 0,

# Classes
class Circle:
    def __init__(self, color, radius, pos=[0, 0], vertices=32):
        self.color = color
        self.radius = radius
        self.pos = pos
        self.vertices = vertices
        self.lines = []
        self.calculate_shape()
    
    def calculate_shape(self):
        if self.vertices >= 3:
            self.lines.clear()

            angle = 0
            while angle <= math.pi * 2:
                x = math.sin(angle) * self.radius
                y = math.cos(angle) * self.radius

                self.lines.append([x, y])
                angle += (math.pi * 2) / self.vertices
        else:
            print("[Error] Circle vertices cannot be less than 3!")
            quit()
    
    def draw(self, window):
        for i in range(len(self.lines)):
            if i > 0:
                x1 = round(self.lines[i - 1][0] + self.pos[0])
                y1 = round(self.lines[i - 1][1] + self.pos[1])
                x2 = round(self.lines[i][0] + self.pos[0])
                y2 = round(self.lines[i][1] + self.pos[1])

                pygame.draw.line(window, self.color, (x1, y1), (x2, y2))
        
        # Draw last line
        x1 = round(self.lines[-1][0] + self.pos[0])
        y1 = round(self.lines[-1][1] + self.pos[1])
        x2 = round(self.lines[0][0] + self.pos[0])
        y2 = round(self.lines[0][1] + self.pos[1])
        
        pygame.draw.line(window, self.color, (x1, y1), (x2, y2))


# Functions
def is_circle_overlapping(circle1, circle2):
    dx = circle1.pos[0] - circle2.pos[0]
    dy = circle1.pos[1] - circle2.pos[1]
    r = circle1.radius + circle2.radius

    return dx ** 2 + dy ** 2 < r ** 2


def is_point_in_circle(circle, px, py):
    dx = circle.pos[0] - px
    dy = circle.pos[1] - py
    r = circle.radius
    
    return dx ** 2 + dy ** 2 < r ** 2


# Main variables
size = 50
circles = []

for i in range(size):
    circles.append(Circle(BLACK, random.randint(5, 50), [random.randint(0, WIDTH), random.randint(0, HEIGHT)], 64))

selected_circle_index = -1

# Main loop
run = True
while run:
    ts = clock.tick(FPS) / 1000

    # Input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    mouse_button = pygame.mouse.get_pressed()
    mouse_pos = pygame.mouse.get_pos()
    key = pygame.key.get_pressed()

    if mouse_button[0]:
        if selected_circle_index == -1:
            for i in range(len(circles)):
                if is_point_in_circle(circles[i], mouse_pos[0], mouse_pos[1]):
                    selected_circle_index = i
                    break
    else:
        selected_circle_index = -1
    
    if selected_circle_index >= 0 and selected_circle_index < len(circles):
        circles[selected_circle_index].pos = [mouse_pos[0], mouse_pos[1]]

        if key[pygame.K_UP]:
            circles[selected_circle_index].radius += 1
            circles[selected_circle_index].calculate_shape()
        if key[pygame.K_DOWN]:
            circles[selected_circle_index].radius -= 1
            circles[selected_circle_index].calculate_shape()
    
    # Solve overlapping
    for i in range(len(circles)):
        for j in range(len(circles)):
            if i != j:
                if is_circle_overlapping(circles[i], circles[j]):
                    dx = circles[i].pos[0] - circles[j].pos[0]
                    dy = circles[i].pos[1] - circles[j].pos[1]
                    length = math.sqrt(dx ** 2 + dy ** 2) or 1

                    min_length = circles[i].radius + circles[j].radius
                    overlapping_distance = min_length - length or 1

                    x = dx / (length / overlapping_distance)
                    y = dy / (length / overlapping_distance)

                    circles[i].pos[0] += x / 2; circles[i].pos[1] += y / 2
                    circles[j].pos[0] -= x / 2; circles[j].pos[1] -= y / 2

    # Draw
    window.fill(WHITE)
    
    for circle in circles:
        circle.draw(window)

    pygame.display.update()

pygame.quit()
