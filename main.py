import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Soccer Game")

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
SKY_BLUE = (135, 206, 235)
GREEN = (34, 139, 34)
SAND = (194, 178, 128)
BLACK = (0, 0, 0)

# Fonts
font = pygame.font.Font(None, 36)
large_font = pygame.font.Font(None, 72)

# Load assets
player_img = pygame.Surface((40, 60))
player_img.fill(BLUE)
ball_img = pygame.Surface((20, 20))
pygame.draw.circle(ball_img, WHITE, (10, 10), 10)

# Game variables
player_pos = [WIDTH // 2 - 20, HEIGHT - 100]
ball_pos = [player_pos[0] + 10, player_pos[1] - 30]
ball_velocity = [0, 0]
charging = False
charge_start = 0
kick_power = 0
kicked = False
game_over = False
gravity = 0.2  # Slower gravity for a smoother drop
air_resistance = 0.99
distance = 0
camera_offset = 0

# Clock
clock = pygame.time.Clock()
FPS = 60

# Functions
def draw_background():
    screen.fill(SKY_BLUE)
    pygame.draw.rect(screen, SAND, (0, HEIGHT // 2, WIDTH, HEIGHT // 2))

def reset_game():
    global player_pos, ball_pos, ball_velocity, charging, charge_start, kick_power, kicked, game_over, distance, camera_offset
    player_pos = [WIDTH // 2 - 20, HEIGHT - 100]
    ball_pos = [player_pos[0] + 10, player_pos[1] - 30]
    ball_velocity = [0, 0]
    charging = False
    charge_start = 0
    kick_power = 0
    kicked = False
    game_over = False
    distance = 0
    camera_offset = 0

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e and not kicked and not game_over:
                charging = True
                charge_start = pygame.time.get_ticks()
            if event.key == pygame.K_r:
                reset_game()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_e and charging:
                charging = False
                kicked = True
                charge_end = pygame.time.get_ticks()
                hold_time = (charge_end - charge_start) / 1000
                kick_power = min(hold_time * 2, 20)  # Kick power increases by 2 per second, up to a max of 20
                ball_velocity = [kick_power * 20, -kick_power * 15]  # Adjusted initial velocity

    # Update ball movement
    if kicked:
        # Apply gravity
        ball_velocity[1] += gravity

        # Update ball position
        ball_pos[0] += ball_velocity[0]
        ball_pos[1] += ball_velocity[1]

        # Apply air resistance
        ball_velocity[0] *= air_resistance
        ball_velocity[1] *= air_resistance

        # Check for ground collision
        if ball_pos[1] >= HEIGHT - 20:  # 20 is the ball's radius
            ball_pos[1] = HEIGHT - 20
            ball_velocity[1] = -ball_velocity[1] * 0.7  # Bounce back with reduced speed

            # Stop ball if velocity is very low
            if abs(ball_velocity[1]) < 1 and abs(ball_velocity[0]) < 1:
                ball_velocity = [0, 0]
                kicked = False
                game_over = True  # Mark game as over

        # Calculate distance traveled
        distance += abs(ball_velocity[0]) / 10

        # Lock camera on ball
        camera_offset = ball_pos[0] - WIDTH // 2

    # Draw everything
    draw_background()
    screen.blit(player_img, (player_pos[0] - camera_offset, player_pos[1]))
    screen.blit(ball_img, (ball_pos[0] - camera_offset, ball_pos[1]))

    # Display stats
    stats = [
        f"Kick Power: {kick_power:.2f}",
        f"Distance: {distance:.2f} meters",
        f"Speed: {math.sqrt(ball_velocity[0]**2 + ball_velocity[1]**2):.2f}"
    ]
    for i, stat in enumerate(stats):
        text = font.render(stat, True, BLACK)
        screen.blit(text, (10, 10 + i * 30))

    # Display "Start Again" message if the game is over
    if game_over:
        msg = large_font.render("Start Again (Press R)", True, RED)
        screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2 - msg.get_height() // 2))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()