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

def get_user_name():
    name = ""
    input_running = True
    while input_running:
        screen.fill((0, 0, 0))
        draw_text("Enter Your Name:", font, (255, 255, 255), SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 100)
        draw_text(name, small_font, (255, 255, 255), SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and name.strip():  # Confirm input if not empty
                    input_running = False
                elif event.key == pygame.K_BACKSPACE:  # Handle backspace
                    name = name[:-1]
                else:
                    name += event.unicode  # Add typed character
    return name.strip()


def save_high_score(name, score):
    with open("high_scores.txt", "a") as file:
        file.write(f"{name},{score}\n")


def start_menu():
    menu_running = True
    options = ["New Game", "High Scores", "Quit"]
    selected_index = 0  # Tracks which menu item is currently selected
    user_name = None  # Initialize user_name

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
                        user_name = get_user_name()  # Ask for the user's name
                        menu_running = False  # Exit the menu to start the game
                    elif options[selected_index] == "High Scores":
                        show_high_scores()
                    elif options[selected_index] == "Quit":
                        pygame.quit()
                        quit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
                for i, option in enumerate(options):
                    option_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50 + i * 50, 200, 40)
                    if option_rect.collidepoint(mouse_x, mouse_y):
                        if options[selected_index] == "New Game":
                            user_name = get_user_name()  # Ask for the user's name
                            menu_running = False  # Exit the menu to start the game
                        elif option == "High Scores":
                            show_high_scores()
                        elif option == "Quit":
                            pygame.quit()
                            quit()

    return user_name


def show_high_scores():
    try:
        with open("high_scores.txt", "r") as file:
            scores = [line.strip().split(",") for line in file.readlines()]
            scores = sorted(scores, key=lambda x: int(x[1]), reverse=True)  # Sort by score descending
    except FileNotFoundError:
        scores = []

    scores_display_running = True
    while scores_display_running:
        screen.fill((0, 0, 0))
        draw_text("High Scores", font, (255, 255, 255), SCREEN_WIDTH // 2 - 150, 50)
        y_offset = 150

        for i, (name, score) in enumerate(scores[:10]):  # Show top 10 scores
            draw_text(f"{i + 1}. {name} - {score}", small_font, (255, 255, 255), 100, y_offset)
            y_offset += 40

        draw_text("Press ESC to return", small_font, (255, 255, 255), SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT - 100)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                scores_display_running = False


def countdown():
    countdown_time = 3  # Start from 3
    while countdown_time > 0:
        screen.fill((0, 0, 0))  # Clear the screen
        countdown_text = font.render(str(countdown_time), True, (255, 255, 255))
        screen.blit(countdown_text, (SCREEN_WIDTH // 2 - countdown_text.get_width() // 2, SCREEN_HEIGHT // 2))
        pygame.display.update()
        time.sleep(1)  # Wait for 1 second
        countdown_time -= 1

    # Display "GO!" message before starting
    screen.fill((0, 0, 0))
    go_text = font.render("GO!", True, (255, 255, 255))
    screen.blit(go_text, (SCREEN_WIDTH // 2 - go_text.get_width() // 2, SCREEN_HEIGHT // 2))
    pygame.display.update()
    time.sleep(1)


def main_game(user_name):
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

    # End screen logic
    screen.fill((0, 0, 0))
    end_text = font.render(f"Time's up. Your score: {score}", True, (255, 255, 255))
    save_high_score(user_name, score)
    screen.blit(end_text, (SCREEN_WIDTH // 2 - end_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
    draw_text("Press ESC to return to the main menu.", small_font, (255, 255, 255), SCREEN_WIDTH // 2 - 220,
              SCREEN_HEIGHT // 2 + 50)
    pygame.display.update()

    wait_for_menu = True
    while wait_for_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                wait_for_menu = False

    pygame.mouse.set_visible(True)  # Re-enable the mouse cursor
    start_menu()  # Return to the main menu


# Run the start menu
pygame.mixer.music.play(-1)
user_name = start_menu()  # Get the user's name from the start menu
countdown()               # Run the countdown before starting the game
main_game(user_name)      # Pass it to the main_game function
pygame.quit()
