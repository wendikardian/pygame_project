import pygame
from pygame.locals import *

pygame.font.init()
pygame.mixer.init()
################# Add code below ###############
frame_size_x = 900
frame_size_y = 500
window_screen = pygame.display.set_mode(
    (frame_size_x, frame_size_y))
pygame.display.set_caption("Space Shooter")
white = (255, 255, 255)  # RGB Code for White
black = (0, 0, 0)  # RGB Code for Black
green = (110, 194, 54)  # RGB Code for Green Bullet
blue = (23, 54, 235)  # RGB Code for Blue Bullet
background = pygame.transform.scale(pygame.image.load(
    'gallery/sprites/background.png'), (frame_size_x, frame_size_y))
space_shooter_logo = pygame.image.load('gallery/sprites/space_shooter.png').convert_alpha()

