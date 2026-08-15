import pygame
import pygame_gui
from State import state
import VoiceAssistant

width, height = 1280, 720

pygame.init()
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((32, 33, 35))

    # Render GUI

    pygame.display.flip()

    clock.tick(60) # Cap to 60 FPS

pygame.quit()
