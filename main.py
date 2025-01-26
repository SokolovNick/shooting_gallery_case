import pygame
import random
import time

pygame.init()
pygame.mixer.init()

pygame.mixer.music.load("music/background_music.mp3")
pygame.mixer.music.set_volume(0.5)

SCREEN_WIDTH = 760
SCREEN_HEIGHT = 760
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("img/icon.png")
pygame.display.set_icon(icon)

background_img = pygame.image.load("img/space_background.png")
target_img = pygame.image.load("img/target_ufo.png")
crosshair_img = pygame.image.load("img/crosshair.png")
explosion_img = pygame.image.load("img/explosion.png")

font = pygame.font.Font(None, 48)
small_font = pygame.font.Font(None, 36)


def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))


def start_menu():
    menu_running = True
    options = ["New Game", "High Scores", "Quit"]
    selected_index = 0  # Tracks which menu item is currently selected

    while menu_running:
        screen.fill((0, 0, 0))
        draw_text("Space Invaders", font, (255, 255, 255), SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 150)

        # Get mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Draw menu options
        for i, option in enumerate(options):
            option_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50 + i * 50, 200, 40)

            # Highlight if hovered or selected
            if option_rect.collidepoint(mouse_x, mouse_y):
                selected_index = i
                color = (255, 255, 0)  # Highlighted color
            elif i == selected_index:
                color = (255, 255, 0)  # Keyboard-selected color
            else:
                color = (255, 255, 255)  # Default color

            draw_text(option, small_font, color, option_rect.x, option_rect.y)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:  # Navigate up
                    selected_index = (selected_index - 1) % len(options)
                elif event.key == pygame.K_DOWN:  # Navigate down
                    selected_index = (selected_index + 1) % len(options)
                elif event.key == pygame.K_RETURN:  # Select option
                    if options[selected_index] == "New Game":
                        menu_running = False
                    elif options[selected_index] == "High Scores":
                        show_high_scores()
                    elif options[selected_index] == "Quit":
                        pygame.quit()
                        quit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
                for i, option in enumerate(options):
                    option_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50 + i * 50, 200, 40)
                    if option_rect.collidepoint(mouse_x, mouse_y):
                        if option == "New Game":
                            menu_running = False
                        elif option == "High Scores":
                            show_high_scores()
                        elif option == "Quit":
                            pygame.quit()
                            quit()


def show_high_scores():
    scores_running = True
    while scores_running:
        screen.fill((0, 0, 0))
        draw_text("High Scores", font, (255, 255, 255), SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 100)
        draw_text("Press Enter to return to menu", small_font, (255, 255, 255), SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Back to menu
                    scores_running = False


def main_game():
    target_width = target_img.get_width()
    target_height = target_img.get_height()

    target_x = random.randint(0, SCREEN_WIDTH - target_width)
    target_y = random.randint(0, SCREEN_HEIGHT - target_height)

    pygame.mouse.set_visible(False)
    explosions = []
    explosion_duration = 1.5

    score = 0
    game_duration = 60
    start_time = time.time()

    running = True
    while running:
        screen.blit(background_img, (0, 0))
        current_time = time.time()
        elapsed_time = current_time - start_time

        if elapsed_time >= game_duration:
            running = False
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if target_x < mouse_x < target_x + target_width and target_y < mouse_y < target_y + target_height:
                    explosions.append((target_x, target_y, time.time()))
                    target_x = random.randint(0, SCREEN_WIDTH - target_width)
                    target_y = random.randint(0, SCREEN_HEIGHT - target_height)
                    score += 10

        for explosion in explosions[:]:
            explosion_x, explosion_y, explosion_start_time = explosion
            if current_time - explosion_start_time < explosion_duration:
                screen.blit(explosion_img, (explosion_x, explosion_y))
            else:
                explosions.remove(explosion)

        screen.blit(target_img, (target_x, target_y))
        mouse_x, mouse_y = pygame.mouse.get_pos()
        crosshair_offset_x = crosshair_img.get_width() // 2
        crosshair_offset_y = crosshair_img.get_height() // 2
        screen.blit(crosshair_img, (mouse_x - crosshair_offset_x, mouse_y - crosshair_offset_y))

        score_text = small_font.render(f"Score: {score}", True, (255, 255, 255))
        time_text = small_font.render(f"Time: {int(game_duration - elapsed_time)}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        screen.blit(time_text, (SCREEN_WIDTH - 150, 10))

        pygame.display.update()

    screen.fill((0, 0, 0))
    end_text = font.render(f"Time's up. Your score: {score}", True, (255, 255, 255))
    screen.blit(end_text, (SCREEN_WIDTH // 2 - end_text.get_width() // 2, SCREEN_HEIGHT // 2))
    pygame.display.update()
    time.sleep(3)


# Run the start menu
pygame.mixer.music.play(-1)
start_menu()
main_game()
pygame.quit()
