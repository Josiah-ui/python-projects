import dis
from turtle import distance

import pygame
import random
import math

pygame.init()
W, H = 900, 700

screen = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()
particles = []

for _ in range(300):
    particles.append([
        random.randint(0, W),
        random.randint(0, W),
        random.uniform(0.5, 2)
    ])
    
running = True
while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((3, 3, 15))
        mx ,my = pygame.mouse.get_pos()
        for p in particles:
            dx = mx - p[0]
            dy = my - p[1]
            distance = math.sqrt(dx * dx + dy * dy)
            if distance < 250 and distance > 1:
                p[0] += dx / distance * 2
                p[1] += dy / distance * 2
            else:
                p[0] += math.sin(p[1] * 0.01)
                p[1] += math.cos(p[0] * 0.01)
            pygame.draw.circle(
                screen,
                (80, 180, 255),
                (int(p[0]), int(p[1])),
                int(p[2])
            )
        pygame.draw.circle(
            screen,
            (255, 255, 220),
            (mx, my),
            5
        )
        pygame.display.flip()
        clock.tick(60)

pygame.quit()