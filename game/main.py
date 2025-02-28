import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH, HEIGHT = 640, 480
BALL_RADIUS = 10
PADDLE_WIDTH, PADDLE_HEIGHT = 100, 20
BRICK_WIDTH, BRICK_HEIGHT = 60, 30
FPS = 60

# Set up some colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Set up the font
font = pygame.font.Font(None, 36)

# Set up the clock
clock = pygame.time.Clock()

# Set up the paddle
paddle_x, paddle_y = WIDTH // 2, HEIGHT - PADDLE_HEIGHT - 10
paddle_dx = 0

# Set up the ball
ball_x, ball_y = WIDTH // 2, HEIGHT // 2
ball_dx, ball_dy = 5, 5

# Set up the bricks
bricks = []
for i in range(5):
    for j in range(10):
        brick_x = 10 + j * (BRICK_WIDTH + 5)
        brick_y = 50 + i * (BRICK_HEIGHT + 5)
        # Generate a light random color for the brick
        r = random.randint(192, 255)
        g = random.randint(192, 255)
        b = random.randint(192, 255)
        brick_color = (r, g, b)
        bricks.append((brick_x, brick_y, brick_color))

# Set up the score and lives
score = 0
lives = 3

# Game loop
while lives > 0:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Move the paddle
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        paddle_dx = -10
    elif keys[pygame.K_RIGHT]:
        paddle_dx = 10
    else:
        paddle_dx = 0
    paddle_x += paddle_dx

    # Move the ball
    ball_x += ball_dx
    ball_y += ball_dy

    # Bounce the ball off the edges
    if ball_x < BALL_RADIUS or ball_x > WIDTH - BALL_RADIUS:
        ball_dx *= -1
    if ball_y < BALL_RADIUS:
        ball_dy *= -1

    # Bounce the ball off the paddle
    if ball_y > HEIGHT - PADDLE_HEIGHT - BALL_RADIUS and paddle_x < ball_x < paddle_x + PADDLE_WIDTH:
        ball_dy *= -1

    # Check for collision with bricks
    for brick in bricks:
        if ball_x > brick[0] and ball_x < brick[0] + BRICK_WIDTH and ball_y > brick[1] and ball_y < brick[1] + BRICK_HEIGHT:
            bricks.remove(brick)
            ball_dy *= -1
            score += 1

    # Check for game over
    if ball_y > HEIGHT - BALL_RADIUS:
        lives -= 1
        ball_x, ball_y = WIDTH // 2, HEIGHT // 2
        ball_dx, ball_dy = 5, 5

    # Draw everything
    screen.fill(BLACK)
    pygame.draw.circle(screen, WHITE, (ball_x, ball_y), BALL_RADIUS)
    pygame.draw.rect(screen, WHITE, (paddle_x, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT))
    for brick in bricks:
        pygame.draw.rect(screen, brick[2], (brick[0], brick[1], BRICK_WIDTH, BRICK_HEIGHT))
    text = font.render("Score: " + str(score) + " Lives: " + str(lives), True, WHITE)
    screen.blit(text, (10, 10))
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Game over, display score board
screen.fill(BLACK)
text = font.render("Final score: " + str(score), True, WHITE)
screen.blit(text, (WIDTH // 2 - 100, HEIGHT // 2 - 18))
pygame.display.flip()
pygame.time.wait(3000)  # Wait in seconds before quitting
print("Game Over! Final score:", score)
pygame.quit()
sys.exit()