import pygame
from pygame.locals import *
import random
import sys

pygame.font.init()
pygame.mixer.init()


frame_size_x = 900
frame_size_y = 500
window_screen = pygame.display.set_mode(
    (frame_size_x, frame_size_y))
pygame.display.set_caption("Space Shooter")

white = (255, 255, 255)  # RGB Code for White
black = (0, 0, 0)  # RGB Code for Black
green = (110, 194, 54)  # RGB Code for Green Bullet
blue = (23, 54, 235)  # RGB Code for Blue Bullet

border = pygame.Rect((frame_size_x // 2) - 5, 0, 10,
                     frame_size_y)  # Create Window Divide

# bullet_hit_sound = pygame.mixer.Sound(os.path.join('Assets', 'sfx_hit.ogg'))  # BULLET HIT PLAYER SOUND EFFECT
bullet_hit_sound = pygame.mixer.Sound('gallery/audio/sfx_hit.ogg')
# bullet_fire_sound = pygame.mixer.Sound(os.path.join('Assets', 'sfx_fire.ogg'))  # BULLET FIRED SOUND EFFECT
bullet_fire_sound = pygame.mixer.Sound('gallery/audio/sfx_fire.ogg')
game_end_sound = pygame.mixer.Sound('gallery/audio/sfx_game_over.ogg')

health_font = pygame.font.SysFont('Impact', 40)  # FONT FOR HEALTH DISPLAY
winner_font = pygame.font.SysFont('Impact', 100)  # FONT FOR WINNER DISPLAY
health_size = 30  # Size of Health Bar


FPS = 60  # Game FPS
velocity = 5  # Speed of Spaceship
bullet_velocity = 7  # Speed of Bullets
max_num_of_bullet = 5  # Max Number of Bullets available on screen at once
ship_width, ship_height = 55, 40  # Dimensions for Spaceship Sprites
bullet_width, bullet_height = 10, 5  # Dimensions for bullets

gree_hit = pygame.USEREVENT + 1
blue_hit = pygame.USEREVENT + 2

# green_ship_img = pygame.transform.rotate(pygame.image.load(os.path.join('Assets', 'shipGreen.png')),
green_ship_img = pygame.transform.rotate(
    pygame.image.load('gallery/sprites/shipGreen.png'), 270)
# IMPORT green SPACESHIP IMAGE
# blue_ship_img = pygame.transform.rotate(pygame.image.load('gallery/sprites/shipBlue.png'),90)
blue_ship_img = pygame.transform.rotate(
    pygame.image.load('gallery/sprites/shipBlue.png'), 90)
green_ship = pygame.transform.scale(green_ship_img, (ship_width, ship_height))
blue_ship = pygame.transform.scale(blue_ship_img, (ship_width, ship_height))

background = pygame.transform.scale(pygame.image.load(
    'gallery/sprites/background.png'), (frame_size_x, frame_size_y)).convert()
space_shooter_logo = pygame.image.load('gallery/sprites/space_shooter.png').convert_alpha()
############# Add code below to scale the logo to 300x150
space_shooter_logo = pygame.transform.scale(
    space_shooter_logo, (300, 150)).convert_alpha()


# DRAW GAME ASSETS IN window_screen
def draw_window(green_rect, blue_rect, green_bullets, blue_bullets, green_health, blue_health):
    window_screen.blit(background, (0, 0))  # DRAW background IMAGE
    pygame.draw.rect(window_screen, black, border)  # DRAW border

    green_health_text = health_font.render(
        "Health: " + str(green_health), 1, white)
    blue_health_text = health_font.render(
        "Health: " + str(blue_health), 1, white)
    window_screen.blit(green_health_text, (frame_size_x -
                       green_health_text.get_width() - 10, 10))  # DISPLAY green HEALTH
    window_screen.blit(blue_health_text, (10, 10))  # DISPLAY blue HEALTH

    # Used to show Green Spaceship on screen
    window_screen.blit(green_ship, (green_rect.x, green_rect.y))
    # Used to show Blue Spaceship on screen
    window_screen.blit(blue_ship, (blue_rect.x, blue_rect.y))

    for bullet in green_bullets:
        pygame.draw.rect(window_screen, green, bullet)  # DRAW green BULLETS
    for bullet in blue_bullets:
        # pygame.draw.rect(window_screen, green, bullet)  # DRAW green BULLETS
        pygame.draw.rect(window_screen, blue, bullet)  # DRAW blue BULLETS
    # create health medicine





    pygame.display.update()  # Update Screen


# HANDLE green SPACESHIP MOVEMENT FROM PLAYER INPUT
def green_movement_handler(keys_pressed, green):
    if keys_pressed[pygame.K_a] and green.x - velocity > -5:  # LEFT
        green.x -= velocity
    if keys_pressed[pygame.K_d] and green.x - velocity + green.width < border.x - 5:  # RIGHT
        green.x += velocity
    if keys_pressed[pygame.K_w] and green.y - velocity > 0:  # UP
        green.y -= velocity
    if keys_pressed[pygame.K_s] and green.y - velocity + green.height < frame_size_y - 5:  # DOWN
        green.y += velocity


# HANDLE green SPACESHIP MOVEMENT FROM PLAYER INPUT
def blue_movement_handler(keys_pressed, blue):
    if keys_pressed[pygame.K_LEFT] and blue.x - velocity > border.x + border.width - 5:  # LEFT
        blue.x -= velocity
    if keys_pressed[pygame.K_RIGHT] and blue.x - velocity + blue.width < frame_size_x - 5:  # RIGHT
        blue.x += velocity
    if keys_pressed[pygame.K_UP] and blue.y - velocity > 0:  # UP
        blue.y -= velocity
    if keys_pressed[pygame.K_DOWN] and blue.y - velocity + blue.height < frame_size_y - 5:  # DOWN
        blue.y += velocity


# HANDLE BULLETS FIRED
def handle_bullets(green_bullets, blue_bullets, green, blue):
    for bullet in green_bullets:
        bullet.x += bullet_velocity
        if blue.colliderect(bullet):
            pygame.event.post(pygame.event.Event(blue_hit))
            green_bullets.remove(bullet)
        elif bullet.x > frame_size_x:
            green_bullets.remove(bullet)

    for bullet in blue_bullets:
        bullet.x -= bullet_velocity
        if green.colliderect(bullet):
            pygame.event.post(pygame.event.Event(gree_hit))
            blue_bullets.remove(bullet)
        elif bullet.x < 0:
            blue_bullets.remove(bullet)


# DISPLAY WINNER TEXT
def draw_winner(text):
    winner_text = winner_font.render(text, 1, white)
    window_screen.blit(winner_text, (frame_size_x // 2 - winner_text.get_width() /
                       2, frame_size_y // 2 - winner_text.get_height() / 2))
    pygame.display.update()
    game_end_sound.play()
    pygame.time.delay(5000)


# spawn health
def spawn_health():
    health = pygame.Rect(random.randint(
        0, frame_size_x - health_size), random.randint(0, frame_size_y - health_size), health_size, health_size)
    return health

# Main Function
def main():
    green_rect = pygame.Rect(100, 100, ship_width, ship_height)
    blue_rect = pygame.Rect(700, 300, ship_width, ship_height)
    green_bullets = []
    blue_bullets = []
    green_health = 10
    blue_health = 10
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                run = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(green_bullets) < max_num_of_bullet:
                    bullet = pygame.Rect(
                        green_rect.x + green_rect.width, green_rect.y + green_rect.height // 2 - 2, 10, 5)
                    green_bullets.append(bullet)
                    bullet_fire_sound.play()
                if event.key == pygame.K_RCTRL and len(blue_bullets) < max_num_of_bullet:
                    bullet = pygame.Rect(
                        blue_rect.x, blue_rect.y + blue_rect.height // 2 - 2, 10, 5)
                    blue_bullets.append(bullet)
                    bullet_fire_sound.play()

            if event.type == gree_hit:
                blue_health -= 1
                bullet_hit_sound.play()

            if event.type == blue_hit:
                green_health -= 1
                bullet_hit_sound.play()

        winner_text = ""
        if green_health < 1:
            winner_text = "Green Wins"

        if blue_health < 1:
            winner_text = "Blue Wins"

        if winner_text != "":
            draw_winner(winner_text)
            break
        keys_pressed = pygame.key.get_pressed()


        green_movement_handler(keys_pressed, green_rect)
        blue_movement_handler(keys_pressed, blue_rect)
        handle_bullets(green_bullets, blue_bullets, green_rect, blue_rect)
        draw_window(green_rect, blue_rect, green_bullets,
                    blue_bullets, green_health, blue_health)

        # health = spawn_health()
        # # make health move
        # health.y += 1
        # # draw health
        # pygame.draw.rect(window_screen, green, health)
        # # check if health collides with green
        # if green_rect.colliderect(health):
        #     green_health += 1
        #     # health_sound.play()
        #     health = spawn_health()
        # # check if health collides with blue
        # if blue_rect.colliderect(health):
        #     blue_health += 1
        #     # health_sound.play()
        #     health = spawn_health()

        # pygame.draw.rect(window_screen, green, health)

    welcome_screen()


def welcome_screen():
    while True:
        window_screen.blit(background, (0, 0))
        window_screen.blit(space_shooter_logo, (frame_size_x//3, 40))
        welcome_font = pygame.font.SysFont("impact", 24)
        welcome_text = welcome_font.render(
            "Press Any Key To Begin...", 1, white)
        window_screen.blit(welcome_text, (frame_size_x // 2 - welcome_text.get_width() //
                           2, frame_size_y // 2 - welcome_text.get_height() // 2))
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                print("Start the game")
                main()
        pygame.display.update()


welcome_screen()