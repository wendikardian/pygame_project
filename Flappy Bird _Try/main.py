import random
import pygame
from pygame.locals import *


pygame.init()
FPS = 32
SCREENWIDTH = 289
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GROUNDY = SCREENHEIGHT * 0.8
GAME_SPRITES = {}
GAME_SOUNDS = {}
font = pygame.font.Font(None, 24)

def welcome_screen():
    playerx = int(SCREENWIDTH / 5)
    playery = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height()) / 2)
    baseX=0
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                quit()
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'], (0, 0))
                SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
                SCREEN.blit(GAME_SPRITES['base'], (baseX, GROUNDY))
                pygame.display.update()
                FPSCLOCK.tick(FPS)

def mainGame():
    print("Welcome to Main game")
    score = 0
    playerX = int(SCREENWIDTH / 5)
    playerY = int(SCREENWIDTH / 2)
    baseX = 0

    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    upperPipes = [
        {'x': SCREENWIDTH + 200, 'y': newPipe1[0]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': newPipe2[0]['y']},
    ]

    lowerPipes = [
        {'x': SCREENWIDTH + 200, 'y': newPipe1[1]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': newPipe2[1]['y']},
    ]

    pipeVelX = -4
    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1

    playerFlapAccv = -8
    playerFlapped  = False



    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pgame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playerY > 0:
                    print("You press space or up key")
                    playerVelY = playerFlapAccv
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()
        
        playerMidPos = playerX  + GAME_SPRITES['player'].get_width() / 2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width() / 2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                score += 1
                print(f"Your score is {score}")
                
                GAME_SOUNDS['point'].play()

        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY 

        
        if playerFlapped : 
            playerFlapped = False
        playerHeight = GAME_SPRITES['player'].get_height()
        playerY = playerY + min (playerVelY, GROUNDY - playerY - playerHeight)

        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

        
        if 0<upperPipes[0]['x'] < 5:
            newPipe = getRandomPipe()
            print(newPipe)
            upperPipes.append(newPipe[0])
            lowerPipes.append(newPipe[1])

        if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        crashTest = isCollide(playerX, playerY, upperPipes, lowerPipes)
        if crashTest:
            return


        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0], (upperPipe['x'], upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerPipe['x'], lowerPipe['y']))
        
        SCREEN.blit(GAME_SPRITES['base'], (baseX, GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'], (playerX, playerY))
        scoreText = font.render("Score : {}".format(score), True, (255,255,255))
        SCREEN.blit(scoreText, ( (SCREENWIDTH) / 3, SCREENHEIGHT*0.12))
        

        # for digit in myDigits:
        #     SCREEN.blit(GAME_SPRITES['numbers'][digit], (xOffset, SCREENHEIGHT*0.12))
            # xOffset += GAME_SPRITES['numbers'][digit].get_width()

        
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def isCollide(playerX, playerY, upperPipes, lowerPipes):
    if playerY > GROUNDY - 25 or playerY < 0:
        # add game over sound
        GAME_SOUNDS['hit'].play()
        return True

    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if(playerY < pipeHeight + pipe['y'] and abs(playerX - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True
    
    for pipe in lowerPipes:
        if (playerY + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(playerX - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True

def getRandomPipe():
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT / 3
    y2 = offset + random.randrange(0, int(SCREENHEIGHT - GAME_SPRITES['base'].get_height() - 1.2 * offset))
    pipeX = SCREENWIDTH + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        {
        'x' : pipeX, 'y' : -y1
        },
        {
        'x' : pipeX, 'y' : y2
        }
    ]
    return pipe

FPSCLOCK = pygame.time.Clock()
pygame.display.set_caption("Flappy Bird")
GAME_SPRITES['base'] = pygame.image.load('gallery/sprites/base.png').convert_alpha()
GAME_SPRITES['pipe'] =(pygame.transform.rotate(pygame.image.load('gallery/sprites/pipe.png').convert_alpha(), 180), 
    pygame.image.load('gallery/sprites/pipe.png').convert_alpha()
    )
GAME_SPRITES['background'] = pygame.image.load('gallery/sprites/background.png').convert()
GAME_SPRITES['player'] = pygame.image.load('gallery/sprites/bird.png').convert_alpha()
GAME_SPRITES['numbers'] = (
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
GAME_SOUNDS['die'] = pygame.mixer.Sound('gallery/audio/die.wav')
GAME_SOUNDS['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav')
GAME_SOUNDS['point'] = pygame.mixer.Sound('gallery/audio/point.wav')
GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('gallery/audio/swoosh.wav')
GAME_SOUNDS['wing'] = pygame.mixer.Sound('gallery/audio/wing.wav')


while True:
    welcome_screen()
    mainGame()