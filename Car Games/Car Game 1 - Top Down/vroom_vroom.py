import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Retro Grand Prix")

# Colors
WHITE = (255, 255, 255)

# Load assets
car_image = pygame.image.load("assets/car.png").convert_alpha()  # Car image
road_image = pygame.image.load("assets/road.png").convert()      # Road background
road_y = 0  # Initial vertical position of the road

# Game variables
car_x, car_y = WIDTH // 2 - 50, HEIGHT - 200
car_speed = 5
obstacles = []
obstacle_speed = 7
clock = pygame.time.Clock()

# Generate an obstacle
def create_obstacle():
    x_pos = random.randint(233, WIDTH - 259)
    rect = pygame.Rect(x_pos, -100, 50, 100)
    obstacles.append(rect)

# Game loop
running = True
while running:
    screen.fill(WHITE)
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Move the car left and right
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and car_x > 233:
        car_x -= car_speed
    if keys[pygame.K_RIGHT] and car_x < WIDTH - 259:
        car_x += car_speed
    
    # Move and loop the road background
    road_y += obstacle_speed
    if road_y >= HEIGHT:
        road_y = 0
    screen.blit(road_image, (0, road_y - HEIGHT))
    screen.blit(road_image, (0, road_y))
    
    # Create obstacles
    if random.randint(1, 50) == 1:  # Probability of creating a new obstacle
        create_obstacle()
    
    # Move and draw obstacles
    for obs in obstacles:
        obs.y += obstacle_speed
        pygame.draw.rect(screen, (200, 0, 0), obs)
        if obs.y > HEIGHT:
            obstacles.remove(obs)
    
    # Check collision with obstacles
    car_rect = car_image.get_rect(topleft=(car_x, car_y))
    if any(car_rect.colliderect(obs) for obs in obstacles):
        print("Game Over")
        running = False
    
    # Draw the car
    screen.blit(car_image, (car_x, car_y))
    
    # Update the display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()