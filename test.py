import pygame
import random
import time

pygame.init()

pygame.mixer.init()

pygame.mixer.music.load("music/background_music.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

SCREEN_WIDTH = 760
SCREEN_HEIGHT = 760
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("img/icon.png")
pygame.display.set_icon(icon)

background_img = pygame.image.load("img/space_background.png")
target_img = pygame.image.load("img/target_ufo.png")
crosshair_img = pygame.image.load("img/crosshair.png")
explosion_img = pygame.image.load("img/explosion.png")  # Загрузка изображения взрыва

target_width = target_img.get_width()
target_height = target_img.get_height()

target_x = random.randint(0, SCREEN_WIDTH - target_width)
target_y = random.randint(0, SCREEN_HEIGHT - target_height)

pygame.mouse.set_visible(False)

# Список для отслеживания активных взрывов
explosions = []
explosion_duration = 1.5  # Длительность отображения взрыва в секундах

# Переменные для счёта очков и таймера
score = 0
game_duration = 60  # Продолжительность игры в секундах
start_time = time.time()

font = pygame.font.Font(None, 36)  # Шрифт для отображения текста

running = True
while running:
    screen.blit(background_img, (0, 0))
    current_time = time.time()
    elapsed_time = current_time - start_time

    # Проверяем, истекло ли время игры
    if elapsed_time >= game_duration:
        running = False
        break

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if target_x < mouse_x < target_x + target_width and target_y < mouse_y < target_y + target_height:
                # Добавляем новый взрыв в список
                explosions.append((target_x, target_y, time.time()))
                target_x = random.randint(0, SCREEN_WIDTH - target_width)
                target_y = random.randint(0, SCREEN_HEIGHT - target_height)
                score += 25  # Добавляем очки за попадание

    # Обновляем и отображаем взрывы
    for explosion in explosions[:]:
        explosion_x, explosion_y, explosion_start_time = explosion
        if current_time - explosion_start_time < explosion_duration:
            screen.blit(explosion_img, (explosion_x, explosion_y))
        else:
            # Удаляем взрывы, которые больше не нужно отображать
            explosions.remove(explosion)

        # Отображаем цель
    screen.blit(target_img, (target_x, target_y))

    # Отображаем прицел
    mouse_x, mouse_y = pygame.mouse.get_pos()
    crosshair_offset_x = crosshair_img.get_width() // 2
    crosshair_offset_y = crosshair_img.get_height() // 2
    screen.blit(crosshair_img, (mouse_x - crosshair_offset_x, mouse_y - crosshair_offset_y))

    # Отображаем количество очков и оставшееся время
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    time_text = font.render(f"Time: {int(game_duration - elapsed_time)}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    screen.blit(time_text, (SCREEN_WIDTH - 150, 10))

    pygame.display.update()

# Отображаем сообщение о завершении игры
screen.fill((0, 0, 0))
end_text = font.render(f"Time's up. Your score: {score}", True, (255, 255, 255))
screen.blit(end_text, (SCREEN_WIDTH // 2 - end_text.get_width() // 2, SCREEN_HEIGHT // 2))
pygame.display.update()
time.sleep(3)  # Задержка для отображения сообщения перед выходом

pygame.quit()
