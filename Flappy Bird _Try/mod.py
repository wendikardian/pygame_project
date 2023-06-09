import random # For generating random numbers
import sys # We will use sys.exit to exit the program
import pygame
from pygame.locals import * # Basic pygame imports
import time # To use sleep function
#
# Global Variables for the game
FPS = 32
frame_size_x = 289
frame_size_y = 511
hight_score = 0
window_screen = pygame.display.set_mode((frame_size_x, frame_size_y))
game_sprites = {}
game_sounds = {}
# player = 'gallery/sprites/bird.png'
player = 'gallery/sprites/astro.png'
background = 'gallery/sprites/bg.jpg'
pipe = 'gallery/sprites/pipe_2.png'
ground_by = frame_size_y * 0.8

def welcomeScreen():
    """
    Shows welcome images on the screen
    """

    player_x = int(frame_size_x/5)
    player_y = int((frame_size_y - game_sprites['player'].get_height())/2)
    base_x = 0
    while True:
        for event in pygame.event.get():
            # if user clicks on cross button, close the game
            if event.type == QUIT or (event.type==KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            # If the user presses space or up key, start the game for them
            elif event.type==KEYDOWN and (event.key==K_SPACE or event.key == K_UP):
                return
            else:
                window_screen.blit(game_sprites['background'], (0, 0))
                window_screen.blit(game_sprites['player'], (player_x, player_y))
                # add Text in Pygame in window_screen using Impact font with 32 size, the text said "Astro Man"
                welcome_text = pygame.font.SysFont('Impact', 32)
                welcome_surface = welcome_text.render("Astro Man", True, (255,255,255))
                score_rect = welcome_surface.get_rect()
                score_rect.midtop = (frame_size_x/2, 32)

                window_screen.blit(welcome_surface, score_rect)

                hight_score_font = pygame.font.SysFont('Impact', 20)
                hight_score_surface = hight_score_font.render("High Score : " + str(hight_score), True, (255,255,255))
                hight_score_rect = hight_score_surface.get_rect()
                hight_score_rect.midtop = (frame_size_x/2, 100)
                window_screen.blit(hight_score_surface, hight_score_rect)

                # window_screen.blit(game_sprites['message'], (messagex,messagey ))
                window_screen.blit(game_sprites['base'], (base_x, ground_by))
                pygame.display.update()
                fps_controller.tick(FPS)

def mainGame():
    score = 0
    player_x = int(frame_size_x/5)
    player_y = int(frame_size_x/2)
    base_x = 0
    player_flapped = False # It is true only when the bird is flapping
    # player_min_vel_y = -8
    player_flap_acc = -8 # velocity while flapping
    pipe_vel_x = -4
    player_vel_y = -9
    player_max_vel_y = 10
    player_acc_y = 1
    global hight_score
    # Add code
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    # my List of upper pipes
    upper_pipes = [
        {'x': frame_size_x+200, 'y':newPipe1[0]['y']},
        {'x': frame_size_x+200+(frame_size_x/2), 'y':newPipe2[0]['y']},
    ]
    # my List of lower pipes
    lower_pipes = [
        {'x': frame_size_x+200, 'y':newPipe1[1]['y']},
        {'x': frame_size_x+200+(frame_size_x/2), 'y':newPipe2[1]['y']},
    ]

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if player_y > 0:
                    player_vel_y = player_flap_acc
                    player_flapped = True
                    game_sounds['wing'].play()



        crashTest = isCollide(player_x, player_y, upper_pipes, lower_pipes) # This function will return true if the player is crashed
        if crashTest:
            if score > hight_score :
                hight_score = score
            time.sleep(1)
            # game_over(score)
            return

        #check for score
        playerMidPos = player_x + game_sprites['player'].get_width()/2
        for pipe in upper_pipes:
            pipeMidPos = pipe['x'] + game_sprites['pipe'][0].get_width()/2
            if pipeMidPos<= playerMidPos < pipeMidPos +4:
                score +=1
                print(f"Your score is {score}")
                game_sounds['point'].play()

        
        if player_vel_y <player_max_vel_y and not player_flapped:
            player_vel_y += player_acc_y

        if player_flapped:
            player_flapped = False
        playerHeight = game_sprites['player'].get_height()
        player_y = player_y + min(player_vel_y, ground_by - player_y - playerHeight)

        # move pipes to the left
        for upperPipe , lowerPipe in zip(upper_pipes, lower_pipes):
            upperPipe['x'] += pipe_vel_x
            lowerPipe['x'] += pipe_vel_x

        # Add a new pipe when the first is about to cross the leftmost part of the screen
        if 0<upper_pipes[0]['x']<5:
            newpipe = getRandomPipe()
            upper_pipes.append(newpipe[0])
            lower_pipes.append(newpipe[1])

        # if the pipe is out of the screen, remove it
        if upper_pipes[0]['x'] < -game_sprites['pipe'][0].get_width():
            upper_pipes.pop(0)
            lower_pipes.pop(0)

        # Lets blit our sprites now
        window_screen.blit(game_sprites['background'], (0, 0))
        for upperPipe, lowerPipe in zip(upper_pipes, lower_pipes):
            window_screen.blit(game_sprites['pipe'][0], (upperPipe['x'], upperPipe['y']))
            window_screen.blit(game_sprites['pipe'][1], (lowerPipe['x'], lowerPipe['y']))

        window_screen.blit(game_sprites['base'], (base_x, ground_by))
        window_screen.blit(game_sprites['player'], (player_x, player_y))
        # myDigits = [int(x) for x in list(str(score))]
        # width = 0
        # for digit in myDigits:
        #     width += game_sprites['numbers'][digit].get_width()
        # Xoffset = (frame_size_x - width)/2

        # for digit in myDigits:
        #     window_screen.blit(game_sprites['numbers'][digit], (Xoffset, frame_size_y*0.12))
        #     Xoffset += game_sprites['numbers'][digit].get_width()
        score_font = pygame.font.SysFont('Poppins', 32)
        score_surface = score_font.render(str(score), True, (255,255,255))
        score_rect = score_surface.get_rect()
        score_rect.midtop = (frame_size_x/2, 32)
        window_screen.blit(score_surface, score_rect)
        pygame.display.update()
        fps_controller.tick(FPS)



def isCollide(player_x, player_y, upper_pipes, lower_pipes):
    if player_y > frame_size_y * 0.7 or player_y<0:
        game_sounds['hit'].play()
        return True

    for pipe in upper_pipes:
        pipeHeight = game_sprites['pipe'][0].get_height()
        if(player_y < pipeHeight + pipe['y'] and abs(player_x - pipe['x']) < game_sprites['pipe'][0].get_width()):
            game_sounds['hit'].play()
            return True

    for pipe in lower_pipes:
        if (player_y + game_sprites['player'].get_height() > pipe['y']) and abs(player_x - pipe['x']) < game_sprites['pipe'][0].get_width():
            game_sounds['hit'].play()
            return True

    return False

def getRandomPipe():
    """
    Generate positions of two pipes(one bottom straight and one top rotated ) for blitting on the screen
    """
    pipeHeight = game_sprites['pipe'][0].get_height()
    offset = frame_size_y/3
    y2 = offset + random.randrange(0, int(frame_size_y - game_sprites['base'].get_height()  - 1.2 *offset))
    pipeX = frame_size_x + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x': pipeX, 'y': -y1}, #upper Pipe
        {'x': pipeX, 'y': y2} #lower Pipe
    ]
    return pipe







pygame.init() # Initialize all pygame's modules
fps_controller = pygame.time.Clock()
pygame.display.set_caption('Astro Man')
game_sprites['numbers'] = (
    pygame.image.load('gallery/sprites/0.png').convert_alpha(),
    pygame.image.load('gallery/sprites/1.png').convert_alpha(),
    pygame.image.load('gallery/sprites/2.png').convert_alpha(),
    pygame.image.load('gallery/sprites/3.png').convert_alpha(),
    pygame.image.load('gallery/sprites/4.png').convert_alpha(),
    pygame.image.load('gallery/sprites/5.png').convert_alpha(),
    pygame.image.load('gallery/sprites/6.png').convert_alpha(),
    pygame.image.load('gallery/sprites/7.png').convert_alpha(),
    pygame.image.load('gallery/sprites/8.png').convert_alpha(),
    pygame.image.load('gallery/sprites/9.png').convert_alpha(),
)

# game_sprites['message'] =pygame.image.load('gallery/sprites/message.png').convert_alpha()
game_sprites['pipe'] =(pygame.transform.rotate(pygame.image.load( pipe).convert_alpha(), 180),
pygame.image.load(pipe).convert_alpha()
)

# Game sounds
# game_sounds['swoosh'] = pygame.mixer.Sound('gallery/audio/swoosh.wav')
# game_sounds['die'] = pygame.mixer.Sound('gallery/audio/die.wav')
game_sounds['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav')
game_sounds['point'] = pygame.mixer.Sound('gallery/audio/point.wav')
game_sounds['wing'] = pygame.mixer.Sound('gallery/audio/jump.wav')

game_sprites['base'] =pygame.image.load('gallery/sprites/base_1.jpg').convert_alpha()
game_sprites['background'] = pygame.image.load(background).convert()
game_sprites['player'] = pygame.image.load(player).convert_alpha()
while True:
    welcomeScreen() # Shows welcome screen to the user until he presses a button
    mainGame() # This is the main game function
    # game_over() # Shows the game over screen