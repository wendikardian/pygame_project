import pygame
import os
import random


pygame.init()
WIDTH = 750
HEIGHT = 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")


# load assets 
red_space = pygame.image.load("assets/pixel_laser_red.png")
green_space = pygame.image.load("assets/pixel_laser_green.png")
blue_space = pygame.image.load("assets/pixel_laser_blue.png")
yellow_space = pygame.image.load("assets/pixel_laser_yellow.png")


red_laser = pygame.image.load("assets/pixel_laser_red.png")
green_laser = pygame.image .load("assets/pixel_laser_green.png")
blue_laser = pygame.image.load("assets/pixel_laser_blue.png")
yellow_laser = pygame.image.load("assets/pixel_laser_yellow.png")


background = pygame.transform.scale(pygame.image.load("assets/background-black.png"), (750, 750))



title_font = pygame.font.SysFont("Poppins", 70)

class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))
    
    def move(self, vel):
        self.y += vel
    
    def off_screen(self, height):
        return not(self.y <= height and self.y >= 0)

    def collision(self, obj):
        return collide(self, obj)


class Ship:
    COOLDOWN = 30

    def __init__(self, x, y, health = 100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0
    

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1
    
    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()
    
    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1
    
class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x,y, health)
        self.ship_img = yellow_space
        self.laser_img = yellow_laser
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)
    
    def draw(self, window):
        super().draw(window)
        self.healthbar(window)
    
    def healthbar(self, window):
        pygame.draw.rect(window, (255,0,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0,255,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health/self.max_health), 10))
    


            

def main_game():
    run = True
    FPS = 60
    level = 0
    lives = 5
    main_font = pygame.font.SysFont("Poppins", 50)
    lost_font = pygame.font.SysFont("Poppins", 60)
    clock = pygame.time.Clock()


    enemies = []
    wave_length = 5
    enemy_val = 1

    lost = False
    lost_count = 0


    player = Player(300, 630)
    player_vel = 5 
    laser_vel = 5

    def redraw_window():
        screen.blit(background, (0,0))
        lives_label = main_font.render(f"lives : {lives}", 1, (255,255,255))
        level_label = main_font.render(f"level : {level}", 1, (255,255,255))


        screen.blit(lives_label, (10,10))
        screen.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))
        player.draw(screen)

        pygame.display.update()
    

    while run:
        clock.tick(FPS)
        redraw_window()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - player_vel > 0:
            player.x -= player_vel
        if keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH:
            player.x += player_vel
        if keys[pygame.K_w] and player.y - player_vel > 0:
            player.y -= player_vel
        if keys[pygame.K_s] and player.y + player_vel + player.get_height() + 15 < HEIGHT:
            player.y += player_vel
        if keys[pygame.K_SPACE]:
            player.shoot()
        
        player.move_lasers(-laser_vel, enemies)
 

running = True
while running:
    screen.blit(background, (0,0))
    title_label = title_font.render("Press the mouse", 1, (255,255,255))
    screen.blit(title_label, (WIDTH/2 - title_label.get_width()/2, 350))
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            # running = False
            main_game()

pygame.quit()