import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
CELL_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Neon Snake :)")
clock = pygame.time.Clock()
snake_speed = 12

NEON_GREEN = (0, 255, 128)
NEON_RED = (255, 51, 102)
NEON_BLUE = (0, 255, 255)
BLACK = (10, 10, 10)

score = 0
snake = []
snake_direction = (CELL_SIZE, 0)
food = (0, 0)

def draw_gradient():
    """Cyberpunk gradient background"""
    for y in range(HEIGHT):
        ratio = y / HEIGHT
        r = int(30 * (1 - ratio) + 10 * ratio)
        g = int(10 * (1 - ratio) + 30 * ratio)
        b = int(30 * (1 - ratio) + 60 * ratio)
        pygame.draw.line(screen, (r, g, b), (0, y), (WIDTH, y))

def draw_glowing_rect(x, y, color, size):
    """Draw glowing neon rectangles"""
    glow_levels = [8, 6, 4, 2]
    for i, g in enumerate(glow_levels):
        s = size + g
        alpha = max(20, 80 - i * 20)
        glow_surface = pygame.Surface((s, s), pygame.SRCALPHA)
        pygame.draw.rect(glow_surface, (*color, alpha), (0, 0, s, s), border_radius=8)
        screen.blit(glow_surface, (x - g // 2, y - g // 2))
    pygame.draw.rect(screen, color, (x, y, size, size), border_radius=4)

def draw_snake():
    for segment in snake:
        draw_glowing_rect(segment[0], segment[1], NEON_GREEN, CELL_SIZE)

def draw_food():
    draw_glowing_rect(food[0], food[1], NEON_RED, CELL_SIZE)

def show_score():
    font = pygame.font.SysFont("Consolas", 28, bold=True)
    text = font.render(f"Score: {score}", True, NEON_BLUE)
    screen.blit(text, (10, 10))

def button(text, x, y, w, h, color, hover_color, action=None):
    """Draws a button with hover effect"""
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, hover_color, (x, y, w, h), border_radius=12)
        if click[0] == 1 and action:
            action()
    else:
        pygame.draw.rect(screen, color, (x, y, w, h), border_radius=12)

    font = pygame.font.SysFont("Consolas", 35, bold=True)
    text_surf = font.render(text, True, BLACK)
    screen.blit(text_surf, (x + (w - text_surf.get_width()) // 2,
                            y + (h - text_surf.get_height()) // 2))

def reset_game():
    global snake, snake_direction, food, score
    snake = [(100, 100)]
    snake_direction = (CELL_SIZE, 0)
    food = (random.randrange(0, WIDTH, CELL_SIZE),
            random.randrange(0, HEIGHT, CELL_SIZE))
    score = 0

def game_loop():
    global snake, snake_direction, food, score

    reset_game()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake_direction != (0, CELL_SIZE):
                    snake_direction = (0, -CELL_SIZE)
                elif event.key == pygame.K_DOWN and snake_direction != (0, -CELL_SIZE):
                    snake_direction = (0, CELL_SIZE)
                elif event.key == pygame.K_LEFT and snake_direction != (CELL_SIZE, 0):
                    snake_direction = (-CELL_SIZE, 0)
                elif event.key == pygame.K_RIGHT and snake_direction != (-CELL_SIZE, 0):
                    snake_direction = (CELL_SIZE, 0)

        
        head = (snake[0][0] + snake_direction[0], snake[0][1] + snake_direction[1])
        snake.insert(0, head)

        if head == food:
            score += 1
            food = (random.randrange(0, WIDTH, CELL_SIZE),
                    random.randrange(0, HEIGHT, CELL_SIZE))
        else:
            snake.pop()

        # Collision check
        if (head[0] < 0 or head[0] >= WIDTH or
            head[1] < 0 or head[1] >= HEIGHT or
            head in snake[1:]):
            game_over_screen()

        # Draw
        draw_gradient()
        draw_snake()
        draw_food()
        show_score()
        pygame.display.flip()
        clock.tick(snake_speed)
def home_screen():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        draw_gradient()
        font = pygame.font.SysFont("Consolas", 60, bold=True)
        title = font.render("NEON SNAKE 🐍", True, NEON_GREEN)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 150))

        button("START", WIDTH//2 - 100, 300, 200, 60, NEON_GREEN, NEON_BLUE, game_loop)
        button("QUIT", WIDTH//2 - 100, 400, 200, 60, NEON_RED, NEON_BLUE, pygame.quit)

        pygame.display.flip()
        clock.tick(15)

def game_over_screen():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        draw_gradient()
        font = pygame.font.SysFont("Consolas", 50, bold=True)
        text = font.render("GAME OVER!", True, NEON_RED)
        score_text = font.render(f"Final Score: {score}", True, NEON_BLUE)
        screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - 100))
        screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2 - 40))

        button("RESTART", WIDTH//2 - 120, 350, 250, 60, NEON_GREEN, NEON_BLUE, game_loop)
        button("HOME", WIDTH//2 - 120, 430, 250, 60, NEON_RED, NEON_BLUE, home_screen)

        pygame.display.flip()
        clock.tick(15)

home_screen()




