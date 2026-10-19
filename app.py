import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH = 400
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Colors
SKY = (135, 206, 235)
GREEN = (34, 177, 76)
YELLOW = (255, 220, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Game settings
bird_x = 80
bird_y = 300
bird_radius = 15
bird_velocity = 0
gravity = 0.5
jump_strength = -8

pipe_width = 60
pipe_gap = 170
pipe_speed = 3

pipes = []
score = 0
font = pygame.font.SysFont(None, 36)
clock = pygame.time.Clock()

def create_pipe():
    gap_y = random.randint(150, 400)
    return {
        "x": WIDTH,
        "gap_y": gap_y,
        "scored": False
    }

pipes.append(create_pipe())
game_over = False

# Main game loop
while True:

    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                bird_velocity = jump_strength

            if event.key == pygame.K_r and game_over:
                bird_y = 300
                bird_velocity = 0
                pipes = [create_pipe()]
                score = 0
                game_over = False

    if not game_over:

        # Bird physics
        bird_velocity += gravity
        bird_y += bird_velocity

        # Create new pipes
        if pipes[-1]["x"] < WIDTH - 220:
            pipes.append(create_pipe())

        # Move pipes
        for pipe in pipes:
            pipe["x"] -= pipe_speed

        # Remove pipes outside the screen
        pipes = [pipe for pipe in pipes if pipe["x"] + pipe_width > 0]

        # Bird collision rectangle
        bird_rect = pygame.Rect(
            bird_x - bird_radius,
            int(bird_y) - bird_radius,
            bird_radius * 2,
            bird_radius * 2
        )

        # Collision detection and scoring
        for pipe in pipes:

            top_height = pipe["gap_y"] - pipe_gap // 2
            bottom_y = pipe["gap_y"] + pipe_gap // 2

            top_rect = pygame.Rect(
                pipe["x"], 0,
                pipe_width, top_height
            )

            bottom_rect = pygame.Rect(
                pipe["x"], bottom_y,
                pipe_width, HEIGHT - bottom_y
            )

            if bird_rect.colliderect(top_rect) or bird_rect.colliderect(bottom_rect):
                game_over = True

            if not pipe["scored"] and pipe["x"] + pipe_width < bird_x:
                score += 1
                pipe["scored"] = True

        # Screen boundary collision
        if bird_y - bird_radius < 0 or bird_y + bird_radius > HEIGHT:
            game_over = True

    # Draw background
    screen.fill(SKY)

    # Draw pipes
    for pipe in pipes:
        top_height = pipe["gap_y"] - pipe_gap // 2
        bottom_y = pipe["gap_y"] + pipe_gap // 2

        pygame.draw.rect(
            screen, GREEN,
            (pipe["x"], 0, pipe_width, top_height)
        )

        pygame.draw.rect(
            screen, GREEN,
            (pipe["x"], bottom_y, pipe_width, HEIGHT - bottom_y)
        )

    # Draw bird
    pygame.draw.circle(
        screen, YELLOW,
        (bird_x, int(bird_y)), bird_radius
    )

    # Draw eye
    pygame.draw.circle(
        screen, WHITE,
        (bird_x + 5, int(bird_y) - 5), 5
    )

    pygame.draw.circle(
        screen, BLACK,
        (bird_x + 7, int(bird_y) - 5), 2
    )

    # Display score
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    # Game over screen
    if game_over:
        over_text = font.render("GAME OVER!", True, BLACK)
        restart_text = font.render("Press R to Restart", True, BLACK)

        screen.blit(
            over_text,
            (WIDTH // 2 - over_text.get_width() // 2, 250)
        )

        screen.blit(
            restart_text,
            (WIDTH // 2 - restart_text.get_width() // 2, 300)
        )

    pygame.display.update()