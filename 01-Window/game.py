import pygame
from sys import exit # closes all code

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Dark Souls")
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    # draw all our elements
    # update everything
    pygame.display.update()
    clock.tick(60)

