import pygame
from random import randint


pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Running Game")
clock = pygame.time.Clock()
font = pygame.font.Font("font/Pixeltype.ttf", 32)
game_active = False
start_time = 0
score = 0


skybox= pygame.image.load('graphics/sky.png').convert()
ground = pygame.image.load('graphics/Ground.png').convert()


# Video frames for enemy
enemy_frame1 = pygame.image.load("graphics/enemies/Enemy.png").convert_alpha()
enemy_frame2 = pygame.image.load("graphics/enemies/Enemy_2.png").convert_alpha()
enemy_frames = [enemy_frame1, enemy_frame2]
enemy_frame_index = 0
enemy = enemy_frames[enemy_frame_index]

# Video frames for ghost
enemy2_frame1 = pygame.image.load("graphics/enemies/Enemy2.png").convert_alpha()
enemy2_frame2 = pygame.image.load("graphics/enemies/Enemy2_2.png").convert_alpha()
enemy2_frames = [enemy2_frame1, enemy2_frame2]
enemy2_frame_index = 0
enemy2 = enemy2_frames[enemy2_frame_index]

obstacle_rect_list = []


player_walk_1 = pygame.image.load("graphics/player/Player.png").convert_alpha()
player_walk_2 = pygame.image.load("graphics/player/Player2.png").convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0
player_jump = pygame.image.load("graphics/player/Player3.png").convert_alpha()
player = player_walk[player_index]
player_rect = player.get_rect(midbottom = (80, 320))
player_gravity = 0




# Create introduction screen
player_stand = pygame.image.load("graphics/player/Player.png").convert_alpha()
player_stand =  pygame.transform.scale2x(player_stand)
player_stand_rect = player_stand.get_rect(center = (400, 200))


# Setting game setup (name etc)
game_name = font.render("Runner Game", False, "white")
game_name = pygame.transform.scale2x(game_name)
game_name_rect = game_name.get_rect(center = (400, 80))


game_message = font.render("Press Space to start", False, "white")
game_message_rect = game_message.get_rect(center = (400, 300))

# timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1000)

obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1000)


enemy_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(enemy_animation_timer, 200)

enemy2_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(enemy2_animation_timer, 500)


def display_score():
    current_time = int(pygame.time.get_ticks() / 600) - start_time
    score = font.render(f"{current_time}", False, "white")
    score_rect = score.get_rect(center = (400, 50))
    screen.blit(score, score_rect)
    return current_time

def player_animation():
    global player, player_index

    if player_rect.bottom < 320:
        player = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0
        player = player_walk[int(player_index)]

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5
            if obstacle_rect.bottom == 320:
                screen.blit(enemy, obstacle_rect)
            else:
                screen.blit(enemy2, obstacle_rect)
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
        return obstacle_list
    else: 
        return []

def collision(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit() 
        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos) and player_rect.bottom == 320:
                    player_gravity = -20
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom == 320:
                    player_gravity = -20
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 600)

        if game_active:
            if event.type == obstacle_timer:
                if randint(0, 2):
                    obstacle_rect_list.append(enemy.get_rect(bottomright = (randint(900, 1100), 320)))
                else:
                    obstacle_rect_list.append(enemy2.get_rect(bottomright = (randint(900, 1100), 210)))
            if event.type == enemy_animation_timer:
                if enemy_frame_index == 0:
                    enemy_frame_index = 1
                else:
                    enemy_frame_index = 0
                
                enemy = enemy_frames[enemy_frame_index]
            
            if event.type == enemy2_animation_timer:
                if enemy2_frame_index == 0:
                    enemy2_frame_index = 1
                else:
                    enemy2_frame_index = 0
                
                enemy2 = enemy2_frames[enemy2_frame_index]





    if game_active:
        screen.blit(skybox, (0,0))
        screen.blit(ground, (0, 320))
        score = display_score()
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 320:
            player_rect.bottom = 320
        
        player_animation()
        screen.blit(player, player_rect)

        obstacle_rect_list = obstacle_movement(obstacle_rect_list)
        game_active = collision(player_rect, obstacle_rect_list)
        



    else:
        screen.fill((64,64,64))
        screen.blit(player_stand, player_stand_rect)
        obstacle_rect_list.clear()
        player_rect.midbottom = (80, 320)
        player_gravity = 0

        score_message = font.render("Your score : {}". format(score), False, "white")
        score_message_rect = score_message.get_rect(center = (400, 320))


        screen.blit(game_name, game_name_rect)

        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_message, score_message_rect)
    
    

    pygame.display.update()
    clock.tick(60)

        
