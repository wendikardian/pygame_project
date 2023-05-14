import os
import pygame

pygame.font.init()  # Initialise pygame fonts
pygame.mixer.init()  # Initialise pygame sound effects handler

WIDTH, HEIGHT = 900, 500  # WINDOW RESOLUTION
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))  # SET WINDOW RESOLUTION
pygame.display.set_caption("Space Shooter")  # SET WINDOW TITLE

WHITE = (255, 255, 255)  # RGB Code for White
BLACK = (0, 0, 0)  # RGB Code for Black
GREEN = (110, 194, 54)  # RGB Code for Green Bullet
BLUE = (53, 180, 235)  # RGB Code for Blue Bullet

BORDER = pygame.Rect((WIDTH // 2) - 5, 0, 10, HEIGHT)  # Create Window Divide

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'sfx_hit.ogg'))  # BULLET HIT PLAYER SOUND EFFECT
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'sfx_fire.ogg'))  # BULLET FIRED SOUND EFFECT
GAME_END_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'sfx_game_over.ogg'))  # GAME OVER SOUND EFFECT

HEALTH_FONT = pygame.font.SysFont('kenvector_future.ttf', 40)  # FONT FOR HEALTH DISPLAY
WINNER_FONT = pygame.font.SysFont('kenvector_future.ttf', 100)  # FONT FOR WINNER DISPLAY

FPS = 60  # Game FPS
VELOCITY = 5  # Speed of Spaceship
BULLET_VELOCITY = 7  # Speed of Bullets
MAX_NUM_OF_BULLETS = 5  # Max Number of Bullets available on screen at once
SHIP_WIDTH, SHIP_HEIGHT = 55, 40  # Dimensions for Spaceship Sprites
BULLET_WIDTH, BULLET_HEIGHT = 10, 5  # Dimensions for bullets

GREEN_HIT = pygame.USEREVENT + 1
BLUE_HIT = pygame.USEREVENT + 2

GREEN_SHIP_IMG = pygame.transform.rotate(pygame.image.load(os.path.join('Assets', 'shipGreen.png')),
                                         270)  # IMPORT GREEN SPACESHIP IMAGE
BLUE_SHIP_IMG = pygame.transform.rotate(pygame.image.load(os.path.join('Assets', 'shipBlue.png')),
                                        90)  # IMPORT BLUE SPACESHIP IMAGE

GREEN_SHIP = pygame.transform.scale(GREEN_SHIP_IMG, (SHIP_WIDTH, SHIP_HEIGHT))  # RESCALE GREEN SPACESHIP IMAGE
BLUE_SHIP = pygame.transform.scale(BLUE_SHIP_IMG, (SHIP_WIDTH, SHIP_HEIGHT))  # RESCALE BLUE SPACESHIP IMAGE

BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'background.png')),
                                    (WIDTH, HEIGHT))  # IMPORT BACKGROUND IMAGE


# DRAW GAME ASSETS IN WINDOW
def draw_window(green, blue, green_bullets, blue_bullets, green_health, blue_health):
    WINDOW.blit(BACKGROUND, (0, 0))  # DRAW BACKGROUND IMAGE
    pygame.draw.rect(WINDOW, BLACK, BORDER)  # DRAW BORDER

    green_health_text = HEALTH_FONT.render("Health: " + str(green_health), 1, WHITE)
    blue_health_text = HEALTH_FONT.render("Health: " + str(blue_health), 1, WHITE)
    WINDOW.blit(green_health_text, (WIDTH - green_health_text.get_width() - 10, 10))  # DISPLAY GREEN HEALTH
    WINDOW.blit(blue_health_text, (10, 10))  # DISPLAY BLUE HEALTH

    WINDOW.blit(GREEN_SHIP, (green.x, green.y))  # Used to show Green Spaceship on screen
    WINDOW.blit(BLUE_SHIP, (blue.x, blue.y))  # Used to show Blue Spaceship on screen

    for bullet in green_bullets:
        pygame.draw.rect(WINDOW, GREEN, bullet)  # DRAW GREEN BULLETS
    for bullet in blue_bullets:
        pygame.draw.rect(WINDOW, BLUE, bullet)  # DRAW BLUE BULLETS

    pygame.display.update()  # Update Screen


# HANDLE GREEN SPACESHIP MOVEMENT FROM PLAYER INPUT
def green_movement_handler(keys_pressed, green):
    if keys_pressed[pygame.K_a] and green.x - VELOCITY > -5:  # LEFT
        green.x -= VELOCITY
    if keys_pressed[pygame.K_d] and green.x - VELOCITY + green.width < BORDER.x - 5:  # RIGHT
        green.x += VELOCITY
    if keys_pressed[pygame.K_w] and green.y - VELOCITY > 0:  # UP
        green.y -= VELOCITY
    if keys_pressed[pygame.K_s] and green.y - VELOCITY + green.height < HEIGHT - 5:  # DOWN
        green.y += VELOCITY


# HANDLE GREEN SPACESHIP MOVEMENT FROM PLAYER INPUT
def blue_movement_handler(keys_pressed, blue):
    if keys_pressed[pygame.K_LEFT] and blue.x - VELOCITY > BORDER.x + BORDER.width - 5:  # LEFT
        blue.x -= VELOCITY
    if keys_pressed[pygame.K_RIGHT] and blue.x - VELOCITY + blue.width < WIDTH - 5:  # RIGHT
        blue.x += VELOCITY
    if keys_pressed[pygame.K_UP] and blue.y - VELOCITY > 0:  # UP
        blue.y -= VELOCITY
    if keys_pressed[pygame.K_DOWN] and blue.y - VELOCITY + blue.height < HEIGHT - 5:  # DOWN
        blue.y += VELOCITY


# HANDLE BULLETS FIRED
def handle_bullets(green_bullets, blue_bullets, green, blue):
    for bullet in green_bullets:
        bullet.x += BULLET_VELOCITY
        if blue.colliderect(bullet):
            pygame.event.post(pygame.event.Event(BLUE_HIT))
            green_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            green_bullets.remove(bullet)

    for bullet in blue_bullets:
        bullet.x -= BULLET_VELOCITY
        if green.colliderect(bullet):
            pygame.event.post(pygame.event.Event(GREEN_HIT))
            blue_bullets.remove(bullet)
        elif bullet.x < 0:
            blue_bullets.remove(bullet)


# DISPLAY WINNER TEXT
def draw_winner(text):
    winner_text = WINNER_FONT.render(text, 1, WHITE)
    WINDOW.blit(winner_text, (WIDTH // 2 - winner_text.get_width() / 2, HEIGHT // 2 - winner_text.get_height() / 2))
    pygame.display.update()
    GAME_END_SOUND.play()
    pygame.time.delay(5000)


# Main Function
def main():
    green = pygame.Rect(100, 100, SHIP_WIDTH, SHIP_HEIGHT)
    blue = pygame.Rect(700, 300, SHIP_WIDTH, SHIP_HEIGHT)

    green_bullets = []
    blue_bullets = []

    green_health = 10
    blue_health = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        # Ensure Game Runs at 60FPS
        clock.tick(FPS)
        # Check for pygame events
        for event in pygame.event.get():

            # Check if game is quit
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(green_bullets) < MAX_NUM_OF_BULLETS:
                    bullet = pygame.Rect(green.x + green.width, green.y + green.height // 2 - 2, 10, 5)
                    green_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                if event.key == pygame.K_RCTRL and len(blue_bullets) < MAX_NUM_OF_BULLETS:
                    bullet = pygame.Rect(blue.x, blue.y + blue.height // 2 - 2, 10, 5)
                    blue_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == GREEN_HIT:
                blue_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == BLUE_HIT:
                green_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ""
        if green_health < 0:
            winner_text = "Green Wins"

        if blue_health < 0:
            winner_text = "Blue Wins"

        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        green_movement_handler(keys_pressed, green)
        blue_movement_handler(keys_pressed, blue)

        handle_bullets(green_bullets, blue_bullets, green, blue)

        draw_window(green, blue, green_bullets, blue_bullets, green_health, blue_health)

    main()


if __name__ == "__main__":
    main()
