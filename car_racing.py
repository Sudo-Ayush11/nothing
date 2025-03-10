import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car Racing Game")

# Clock and fonts
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 55)

# Car dimensions
CAR_WIDTH = 50
CAR_HEIGHT = 100

# Functions
def display_message(text, color, x, y):
    screen_text = font.render(text, True, color)
    screen.blit(screen_text, [x, y])

def car(x, y):
    pygame.draw.rect(screen, BLUE, [x, y, CAR_WIDTH, CAR_HEIGHT])

def enemy_car(x, y):
    pygame.draw.rect(screen, RED, [x, y, CAR_WIDTH, CAR_HEIGHT])

def game_loop():
    # Car position
    car_x = WIDTH // 2
    car_y = HEIGHT - CAR_HEIGHT - 20
    car_speed = 0

    # Enemy car
    enemy_x = random.randint(0, WIDTH - CAR_WIDTH)
    enemy_y = -CAR_HEIGHT
    enemy_speed = 7

    score = 0
    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    car_speed = -7
                if event.key == pygame.K_RIGHT:
                    car_speed = 7
            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                    car_speed = 0

        # Update car position
        car_x += car_speed

        # Prevent car from going off-screen
        if car_x < 0:
            car_x = 0
        elif car_x > WIDTH - CAR_WIDTH:
            car_x = WIDTH - CAR_WIDTH

        # Update enemy car position
        enemy_y += enemy_speed

        # Reset enemy car after it goes off-screen
        if enemy_y > HEIGHT:
            enemy_y = -CAR_HEIGHT
            enemy_x = random.randint(0, WIDTH - CAR_WIDTH)
            score += 1
            enemy_speed += 0.5  # Increase difficulty

        # Check for collision
        if (
            car_y < enemy_y + CAR_HEIGHT
            and car_y + CAR_HEIGHT > enemy_y
            and car_x < enemy_x + CAR_WIDTH
            and car_x + CAR_WIDTH > enemy_x
        ):
            display_message("GAME OVER", RED, WIDTH // 3, HEIGHT // 3)
            pygame.display.update()
            pygame.time.wait(2000)
            game_over = True

        # Draw everything
        screen.fill(WHITE)
        car(car_x, car_y)
        enemy_car(enemy_x, enemy_y)
        display_message(f"Score: {score}", BLACK, 10, 10)

        # Update display
        pygame.display.update()
        clock.tick(60)

    pygame.quit()

game_loop()