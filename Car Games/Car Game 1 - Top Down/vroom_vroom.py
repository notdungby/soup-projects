import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Vroom Vroom")

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Load assets
car_image = pygame.image.load("assets/car.png").convert_alpha()  # Car image
road_image = pygame.image.load("assets/road.png").convert()      # Road background

# Game variables
car_speed = 5
obstacles = []
obstacle_speed = 7
clock = pygame.time.Clock()

# Define button class
class Button:
    def __init__(self, text, x, y, width, height, color, action=None):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.action = action

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        font = pygame.font.Font(None, 36)
        text_surface = font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# Create buttons for the main menu
def main_menu():
    play_button = Button("Play", WIDTH // 2 - 100, HEIGHT // 2 - 100, 200, 50, GREEN, start_game)
    customization_button = Button("Customization", WIDTH // 2 - 100, HEIGHT // 2 - 40, 200, 50, BLUE)
    settings_button = Button("Settings", WIDTH // 2 - 100, HEIGHT // 2 + 20, 200, 50, BLUE)
    exit_button = Button("Exit", WIDTH // 2 - 100, HEIGHT // 2 + 80, 200, 50, RED, exit_game)

    buttons = [play_button, customization_button, settings_button, exit_button]

    running = True
    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.is_clicked(event.pos):
                        if button.action:
                            button.action()

        for button in buttons:
            button.draw(screen)

        pygame.display.flip()
        clock.tick(60)

# Function to start the game
def start_game():
    game_loop()

# Function to exit the game
def exit_game():
    pygame.quit()
    exit()

# Game loop
def game_loop():
    global obstacles
    obstacles.clear()  # Clear obstacles from previous runs

    car_x, car_y = WIDTH // 2 - 50, HEIGHT - 200
    road_y = 0
    running = True
    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and car_x > 233:
            car_x -= car_speed
        if keys[pygame.K_RIGHT] and car_x < WIDTH - 259:
            car_x += car_speed

        road_y += obstacle_speed
        if road_y >= HEIGHT:
            road_y = 0
        screen.blit(road_image, (0, road_y - HEIGHT))
        screen.blit(road_image, (0, road_y))

        if random.randint(1, 50) == 1:
            create_obstacle()

        for obs in obstacles:
            obs.y += obstacle_speed
            pygame.draw.rect(screen, (200, 0, 0), obs)
            if obs.y > HEIGHT:
                obstacles.remove(obs)

        car_rect = car_image.get_rect(topleft=(car_x, car_y))
        if any(car_rect.colliderect(obs) for obs in obstacles):
            game_over()
            return  # Exit the game loop

        screen.blit(car_image, (car_x, car_y))
        pygame.display.flip()
        clock.tick(60)

def create_obstacle():
    x_pos = random.randint(233, WIDTH - 259)
    rect = pygame.Rect(x_pos, -100, 50, 100)
    obstacles.append(rect)

# Game Over Screen
def game_over():
    running = True
    while running:
        screen.fill(WHITE)
        font = pygame.font.Font(None, 74)
        text_surface = font.render("You Crashed!", True, RED)
        text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        screen.blit(text_surface, text_rect)

        try_again_button = Button("Try Again", WIDTH // 2 - 100, HEIGHT // 2 + 20, 200, 50, GREEN, start_game)
        menu_button = Button("Menu", WIDTH // 2 - 100, HEIGHT // 2 + 80, 200, 50, BLUE, main_menu)

        for button in [try_again_button, menu_button]:
            button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if try_again_button.is_clicked(event.pos):
                    start_game()
                elif menu_button.is_clicked(event.pos):
                    main_menu()

        pygame.display.flip()
        clock.tick(60)

# Start the main menu
main_menu()

# Quit Pygame
pygame.quit()
