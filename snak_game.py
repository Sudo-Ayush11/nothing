import pygame
import time
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 400

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)

# Snake block size
BLOCK_SIZE = 10

# Frames per second controller
clock = pygame.time.Clock()
FPS = 15

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Fonts
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

def score_display(score):
    value = score_font.render("Your Score: " + str(score), True, GREEN)
    screen.blit(value, [10, 10])

def message(msg, color):
    msg_surface = font_style.render(msg, True, color)
    screen.blit(msg_surface, [WIDTH / 6, HEIGHT / 3])

def game_loop():
    game_over = False
    game_close = False

    x, y = WIDTH / 2, HEIGHT / 2
    x_change, y_change = 0, 0

    snake = []
    length = 1

    food_x = round(random.randrange(0, WIDTH - BLOCK_SIZE) / 10.0) * 10.0
    food_y = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / 10.0) * 10.0

    while not game_over:
        while game_close:
            screen.fill(BLUE)
            message("You lost! Press Q-Quit or C-Play Again", RED)
            score_display(length - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x_change == 0:
                    x_change, y_change = -BLOCK_SIZE, 0
                elif event.key == pygame.K_RIGHT and x_change == 0:
                    x_change, y_change = BLOCK_SIZE, 0
                elif event.key == pygame.K_UP and y_change == 0:
                    x_change, y_change = 0, -BLOCK_SIZE
                elif event.key == pygame.K_DOWN and y_change == 0:
                    x_change, y_change = 0, BLOCK_SIZE

        if x >= WIDTH or x < 0 or y >= HEIGHT or y < 0:
            game_close = True

        x += x_change
        y += y_change
        screen.fill(BLACK)
        pygame.draw.rect(screen, GREEN, [food_x, food_y, BLOCK_SIZE, BLOCK_SIZE])

        snake_head = [x, y]
        snake.append(snake_head)
        if len(snake) > length:
            del snake[0]

        for block in snake[:-1]:
            if block == snake_head:
                game_close = True

        for block in snake:
            pygame.draw.rect(screen, WHITE, [block[0], block[1], BLOCK_SIZE, BLOCK_SIZE])

        score_display(length - 1)
        pygame.display.update()

        if x == food_x and y == food_y:
            food_x = round(random.randrange(0, WIDTH - BLOCK_SIZE) / 10.0) * 10.0
            food_y = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / 10.0) * 10.0
            length += 1

        clock.tick(FPS)

    pygame.quit()
    quit()

game_loop()