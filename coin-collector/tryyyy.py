import pygame
import random

# Initialize Pygame
pygame.init()

# Set the window size
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500

# Create the game window
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Set the game window title
pygame.display.set_caption("Fruit Collector")

# Set the game background color
BACKGROUND_COLOR = (255, 255, 255)

# Load the character image
character_img = pygame.image.load("images/fox.png")

# Load the fruit image
fruit_img = pygame.image.load("images/coin.png")

# Load the obstacle image
obstacle_img = pygame.image.load("images/spike.png")
obstacle_img = pygame.transform.scale(obstacle_img, (50, 50))
# Set the initial position of the character
character_x = 50
character_y = WINDOW_HEIGHT // 2

# Set the initial position of the fruit and obstacle
fruit_x = WINDOW_WIDTH + 100
fruit_y = random.randint(50, WINDOW_HEIGHT - 50)
obstacle_x = WINDOW_WIDTH + 100
obstacle_y = random.randint(50, WINDOW_HEIGHT - 50)

# Set the speed of the fruit and obstacle
fruit_speed = 5
obstacle_speed = 2

# Set the score
score = 0

# Set the font for the score text
font = pygame.font.Font(None, 30)

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # Move the character
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        character_y -= 5
    if keys[pygame.K_DOWN]:
        character_y += 5

    # Move the fruit and obstacle
    fruit_x -= fruit_speed
    obstacle_x -= obstacle_speed

    # Check if the fruit and obstacle have gone off the screen
    if fruit_x < -50:
        fruit_x = WINDOW_WIDTH + 100
        fruit_y = random.randint(50, WINDOW_HEIGHT - 50)
    if obstacle_x < -50:
        obstacle_x = WINDOW_WIDTH + 100
        obstacle_y = random.randint(50, WINDOW_HEIGHT - 50)

    # Check if the character has collected the fruit
    if (character_x + 50 > fruit_x and character_x < fruit_x + 50
            and character_y + 50 > fruit_y and character_y < fruit_y + 50):
        score += 1
        fruit_x = WINDOW_WIDTH + 100
        fruit_y = random.randint(50, WINDOW_HEIGHT - 50)

    # Check if the character has hit the obstacle
    if (character_x + 50 > obstacle_x and character_x < obstacle_x + 50
            and character_y + 50 > obstacle_y and character_y < obstacle_y + 50):
        running = False

    # Clear the screen
    window.fill(BACKGROUND_COLOR)

    # Draw the character, fruit, and obstacle
    window.blit(character_img, (character_x, character_y))
    window.blit(fruit_img, (fruit_x, fruit_y))
    window.blit(obstacle_img, (obstacle_x, obstacle_y))

    # Draw the score text
    score_text = font.render("Score: {}".format(score), True, (0, 0, 0))
    window.blit(score_text, (10, 10))

    # Update the display
    pygame.display.update()

# Quit Pygame
pygame.quit()
