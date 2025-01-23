import pygame
import random
pygame.init()

SCREEN_WIDTH = 760
SCREEN_HEIGHT = 760
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Shooting Gallery")
icon = pygame.image.load("img/icon.png")
pygame.display.set_icon(icon)

background_img = pygame.image.load("img/space_background.png")
target_img = pygame.image.load("img/target_ufo.png")

target_width = 118
target_height = 80

target_x = random.randint(0, SCREEN_WIDTH - target_width)
target_y = random.randint(0, SCREEN_HEIGHT - target_height)

running = True
while running:
    screen.blit(background_img, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if target_x < mouse_x < target_x + target_width and target_y < mouse_y < target_y + target_height:
                target_x = random.randint(0, SCREEN_WIDTH - target_width)
                target_y = random.randint(0, SCREEN_HEIGHT - target_height)
    screen.blit(target_img, (target_x, target_y))
    pygame.display.update()

pygame.quit()
