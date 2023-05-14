from email import message
import pygame
from sys import exit
from random import randint



#-------------SETTINGS:

def display_score():
    current_time = int(pygame.time.get_ticks() / 600) - start_time
    score = font.render(f"{current_time}", False, (0,0,0))
    score_rect = score.get_rect(center = (400, 50))
    screen.blit(score, score_rect)
    return current_time

def obstacle_movement(obstacle_list):  #spawning enemies
    if obstacle_list: #checks if list is empty
        for obstacle_rect in obstacle_list: #for every enemie in list
            obstacle_rect.x -= 5 #will give the speed of the enemies

            if obstacle_rect.bottom == 320: #if the enemie is on gro ud level, it will spawn the Enemy.png (skull)
                screen.blit(enemy, obstacle_rect)
            else:
                screen.blit(enemy2, obstacle_rect) #if its higher than ground level, it will spawn the Enemy2.png (ghost)
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100] #will only add the enemies to the list that are visable on the screem rest of them will be
                                                                                      #automatically removed (removed from list)
        return obstacle_list
    else: return []


def collisions(player, obstacles): #check for player collision function
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect): return False
    return True


def player_animation(): #player animations, walkign and jumping
    global player, player_index 

    if player_rect.bottom < 320: #plays the jumping animation if player is above the ground level
        player = player_jump #changes the image to jump
    else:
        player_index += 0.1 #if the player is not above the gound level, walking animation will start. We can set how fast will images swap
        if player_index >= len(player_walk):player_index = 0 #if the list of availble images will be exceeded, loop will start from the beginning
        player = player_walk[int(player_index)] #switch imagas of the player to list of images (walking animation frames)

pygame.init() # Necessary command to start any game.        

screen = pygame.display.set_mode((800,400)) #game's window resolution
pygame.display.set_caption("Running - The Game") #game's window name(Game's name)
clock = pygame.time.Clock() #fps count variable
font = pygame.font.Font("font/Pixeltype.ttf", 50) # loads font from the folder,  .Font(font type, font size)
game_active = False #game state
start_time = 0
score = 0


#-------------ASSETS:

#loading images from the folder
skybox = pygame.image.load('graphics/Sky.png').convert() #.convert() transforms .png file into a pygame file, which is easier to process for pygame

ground = pygame.image.load('graphics/Ground.png').convert()


#-------------SPRITES:

#font
# score_text = font.render(" My game ", False, (64,64,64)) #renders font,    .render(text, AntyAliasing, color(can be RGB or HEX values))
# score_rect = score_text.get_rect(center = (400,50))

#enemies
#skull
enemy_frame1 = pygame.image.load("graphics/enemies/Enemy.png").convert_alpha() #adds alpha(remove "whitebox" from images)
enemy_frame2 = pygame.image.load("graphics/enemies/Enemy_2.png").convert_alpha()
enemy_frames = [enemy_frame1, enemy_frame2]  #list of available animation frames
enemy_frame_index = 0 #take first image from the availabe frames/images list
enemy = enemy_frames[enemy_frame_index] #set is as the defaul image to render in the game

#ghost
enemy2_frame1 = pygame.image.load("graphics/enemies/Enemy2.png").convert_alpha()
enemy2_frame2 = pygame.image.load("graphics/enemies/Enemy2_2.png").convert_alpha()
enemy2_frames = [enemy2_frame1, enemy2_frame2]
enemy2_frame_index = 0
enemy2 = enemy2_frames[enemy2_frame_index]

# enemy_rect = enemy.get_rect(bottomright = (600,320)) #enemy starting position

obstacle_rect_list = [] #empty list for storing spawned enemies images




#player
player_walk_1 = pygame.image.load("graphics/player/Player.png").convert_alpha()
player_walk_2 = pygame.image.load("graphics/player/Player2.png").convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0 #variable to choose which walking frame to use from list above
player_jump = pygame.image.load("graphics/player/Player3.png").convert_alpha()

player=player_walk[player_index]
player_rect = player.get_rect(midbottom = (80,320)) #creats rectangle (kinda like hitbox) for a player .get_rect(from what point we are "grabbing" image, coordinance)
player_gravity = 0

#intro screen
player_stand = pygame.image.load("graphics/player/Player.png").convert_alpha()
player_stand = pygame.transform.scale2x(player_stand) #scaleing image 2x
player_stand_rect = player_stand.get_rect(center = (400, 200))

#game name
game_name = font.render("Running - The Game", False, "White")
game_name = pygame.transform.scale2x(game_name)
game_name_rect = game_name.get_rect(center = (400,80))

game_message = font.render("Press SPACE to run", False, "WHITE")
game_message_rect = game_message.get_rect(center = (400,320))

#timer
obstacle_timer =pygame.USEREVENT + 1 #we add +1 because pygame has serveral others USEREVENTs that might interfere with our code
pygame.time.set_timer(obstacle_timer, 1100) #timer for event   .set_timer(what even, time in miliseconds)

enemy_animation_timer = pygame.USEREVENT + 2 #creates timer for enemy frames
pygame.time.set_timer(enemy_animation_timer, 200)

enemy2_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(enemy2_animation_timer, 500)


#-------------GAME:
while True:
    for event in pygame.event.get():    
        if event.type == pygame.QUIT:
            pygame.quit()
            exit() #forces exit the game, stops all code
        #------
        # if event.type == pygame.MOUSEMOTION: #checks if coursor/mouse is hovering over player's rectangle
        #     if player_rect.collidepoint(event.pos):
        #         print("This is player")
        #------
        # if event.type == pygame.MOUSEMOTION: #checks coursor/mouse X,Y position
        #     print(event.pos)
          # if event.type == pygame.MOUSEBUTTONUP: #checks if any Mouse Botton is released
        #      print("Release!")
        #------
        # if event.type == pygame.KEYDOWN: #checks if any key is pressed
        #     print("key down")
        # if event.type == pygame.KEYUP: #checks if eny key is released
        #     print("key up")
          #------
        # keys = pygame.key.get_pressed() #lists all the keys
        # if keys[pygame.K_SPACE]: #checks for specific key
        #     print("jump")

        #--CONTROLS:
        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN: #checks if any Mouse Botton is pressed
                    if player_rect.collidepoint(event.pos) and player_rect.bottom == 320: #cehck if mouse is on player and if player is on the ground level
                        player_gravity = -20
                
            if event.type == pygame.KEYDOWN: #checks if any key is pressed/jump function
                    if event.key == pygame.K_SPACE and player_rect.bottom == 320: #checks if it is Space key and if player is on the ground level
                        player_gravity = -20
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                # enemy_rect.left = 800   #enemy starting position
                start_time = int(pygame.time.get_ticks() / 600)
        

        if game_active:
            if event.type == obstacle_timer:
                if randint(0, 2):
                    obstacle_rect_list.append(enemy.get_rect(bottomright = (randint(900,1100),320)))
                else:
                    obstacle_rect_list.append(enemy2.get_rect(bottomright = (randint(900,1100),210)))
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
                    

    if game_active: #starts the game
        #---base surfaces--
        screen.blit(skybox,(0,0)) #.blit = place surfaces (on what, (what cooridinance X,Y)),
                                #pygame will place surfaces in the order as they appear in the code (like layers).
                                #first surface in the code will be rendered as the most furthest
        screen.blit(ground,(0,320))

        # pygame.draw.rect(screen, "#e4f2ff", score_rect, border_radius=4) #pygame draws the specified shape   
        #                                                                 #.rect(dispaly surface, color(can be RGB or HEX values) , shape, + more)

        # screen.blit(score_text,score_rect)
        
        #------
        # pygame.draw.line(screen, "white", (0,0), pygame.mouse.get_pos(), 20) #draws a line     .line(display surface, color, starting point(X,Y), ending point(X,Y), width)
        # pygame.draw.ellipse(screen, "pink", pygame.Rect(50, 200, 100, 100)) #  pygame.Rect creates a shape in a shape .Rect(X position, Y position, width, height)
        #------

        #-----------------------------------

        #score
        score = display_score()

        #enemy 
        # screen.blit(enemy,enemy_rect)
        # enemy_rect.x -= 5 #enemy "speed", changing the coordinance of the rectangle

        # if enemy_rect.right <= 0: #checks if enemy has left the screen to put it back (loop the movement)
        #     enemy_rect.left = 800

        #player 
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 320: 
            player_rect.bottom = 320

        player_animation()
        screen.blit(player, player_rect)
        

        #enemies movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)
        
        game_active = collisions(player_rect, obstacle_rect_list)
        #------
        #if player_rect.colliderect(enemy_rect): #collision detection, checks if rectagle1 collide rectangle2 (in every frame)     rectagle1.colliderect(rectagle2)
        #mouse_pos = pygame.mouse.get_pos() #mouse position, renders it as a rectangle
        #------
        # if player_rect.collidepoint((mouse_pos)): #checks if coursor (mouse), collides with player's rectangle
        #     print(pygame.mouse.get_pressed())
        #------

        #End of the game
        # if enemy_rect.colliderect(player_rect):
            # game_active = False #end game and stops updating the code in the 'game_active' loop

    else:
        screen.fill((64, 64, 64))
        screen.blit(player_stand, player_stand_rect)
        obstacle_rect_list.clear()
        player_rect.midbottom = (80, 320)
        player_gravity = 0

        score_message = font.render(f'Your Score: {score}', False, "White") # score summary
        score_message_rect = score_message.get_rect(center = (400, 320))


        screen.blit(game_name, game_name_rect) 


        if score == 0: #if ther is no score
            screen.blit(game_message, game_message_rect) #instruction to press SPACE will show
        else: #if there is any score, higher value than 0
            screen.blit(score_message, score_message_rect) #score will be displayed instead




    #updates game by every frame
    pygame.display.update() #update the screen with every frame
    clock.tick(60) #fps count



