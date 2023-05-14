import pygame
import random

# Initialize Pygame
pygame.init()

# Define the game screen size
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Load images
BIRD_IMAGE = pygame.image.load("Assets/bird.png")
PIPE_IMAGE = pygame.image.load("Assets/pipe-red.png")

# Define the bird and pipe sizes
BIRD_SIZE = BIRD_IMAGE.get_size()
PIPE_SIZE = PIPE_IMAGE.get_size()

# Set the bird position
bird_x = 50
bird_y = SCREEN_HEIGHT // 2 - BIRD_SIZE[1] // 2

# Set the pipe position
pipe_x = SCREEN_WIDTH - PIPE_SIZE[0]
pipe_y = SCREEN_HEIGHT - PIPE_SIZE[1]

# Set the gravity and jump values
gravity = 0.25
jump = -5
velocity = 0

# Set the game score
score = 0

# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                velocity = jump

    # Update the bird position
    bird_y += velocity
    velocity += gravity

    # Update the pipe position
    pipe_x -= 2

    # Check for collision with the pipe
    if bird_x + BIRD_SIZE[0] > pipe_x and bird_x < pipe_x + PIPE_SIZE[0] and bird_y + BIRD_SIZE[1] > pipe_y:
        running = False

    # Check if the pipe has passed the bird
    if pipe_x + PIPE_SIZE[0] < 0:
        pipe_x = SCREEN_WIDTH - PIPE_SIZE[0]
        pipe_y = random.randint(SCREEN_HEIGHT // 2, SCREEN_HEIGHT - PIPE_SIZE[1])
        score += 1

    # Draw the game elements
    screen.fill((255, 255, 255))
    screen.blit(BIRD_IMAGE, (bird_x, bird_y))
    screen.blit(PIPE_IMAGE, (pipe_x, pipe_y))
    # screen.draw.text(screen, "Score: " + str(score), (10, 10))
    pygame.draw.line(screen, (0, 0, 0), (0, SCREEN_HEIGHT // 2), (SCREEN_WIDTH, SCREEN_HEIGHT // 2))

    # Update the screen
    pygame.display.update()

# Clean up
pygame.quit()
