import pygame
import random

pygame.init()

SCREEN_WIDTH = 760
SCREEN_HEIGHT = 760
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("img/icon.png")
pygame.display.set_icon(icon)

background_img = pygame.image.load("img/space_background.png")
target_img = pygame.image.load("img/target_ufo.png")
crosshair_img = pygame.image.load("img/crosshair.png")  # Загрузите изображение прицела

# Получите размеры изображений
target_width = target_img.get_width()
target_height = target_img.get_height()

# Инициализируйте позицию цели
target_x = random.randint(0, SCREEN_WIDTH - target_width)
target_y = random.randint(0, SCREEN_HEIGHT - target_height)

# Скрыть системный курсор мыши
pygame.mouse.set_visible(False)

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

    # Получите текущую позицию курсора мыши
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Отобразите цель
    screen.blit(target_img, (target_x, target_y))

    # Отобразите прицел в центре курсора
    crosshair_offset_x = crosshair_img.get_width() // 2
    crosshair_offset_y = crosshair_img.get_height() // 2
    screen.blit(crosshair_img, (mouse_x - crosshair_offset_x, mouse_y - crosshair_offset_y))

    pygame.display.update()

pygame.quit()
