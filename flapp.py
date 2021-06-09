# import moduls for game 
import random
import sys
import pygame
from pygame.locals import *

# Global variables
FPS=35
ScreenWidth=289
ScreenHeight=511
SCREEN=pygame.display.set_mode((ScreenWidth,ScreenHeight))
GroundY=ScreenHeight*0.8
Game_Sprites={}
Game_Sounds={}
Player='bird.png'
Background='background.png'
Pipe='pipe.png'

# this is the welcome screen
def welcomeScreen():
    # shows welcome Screen
    playerx=int(ScreenWidth/5)
    playery=int((ScreenHeight - Game_Sprites['player'].get_height())/2)
    messagex=int((ScreenWidth - Game_Sprites['message'].get_width())/2)
    messagey=int(ScreenHeight*0.13)
    basex=0
    while True:
        for event in pygame.event.get():
            # if user press the cross button then close the game
            if event.type == QUIT or (event.type==KEYDOWN and event.key ==K_ESCAPE):
                pygame.quit()
                sys.exit()
            # if user press on space return from here
            elif event.type==KEYDOWN and(event.key==K_SPACE or event.key == K_UP):
                return 
            # bliting image on welcome screen
            else:
                SCREEN.blit(Game_Sprites['background'],(0,0))
                SCREEN.blit(Game_Sprites['player'],(playerx,playery))
                SCREEN.blit(Game_Sprites['message'],(messagex,messagey))
                SCREEN.blit(Game_Sprites['base'],(basex,GroundY))
                pygame.display.update()
                FPSCLOCK.tick(FPS)

# this is the main game
def mainGame():
    # variables for main game
    score=0
    playerx=int(ScreenWidth/5)
    playery=int(ScreenWidth/2)
    basex=0

    # cretes two pipes for blitting on the Screen
    newPipe1=getRandomPipe()
    newPipe2=getRandomPipe()
    #my list for upper pipe
    upperPipes=[
        {'x':ScreenWidth+200 ,'y':newPipe1[0]['y']},
        {'x':ScreenWidth+200+(ScreenWidth/2),'y':newPipe2[0]['y']}
    ]
    #my list for lower pipe
    lowerPipes=[
        {'x':ScreenWidth+200 ,'y':newPipe1[1]['y']},
        {'x':ScreenWidth+200+(ScreenWidth/2),'y':newPipe2[1]['y']}
    ]
    # variables for giving velocity
    pipeVelX=-4
    playerVelY=-9
    playerMaxVelY=10
    playerMinVelY=-8
    playerAccY=1
    playerFlpAccv=-8 #velocity while flapping
    playerFlapped=False #it is true only when the bird ids flapping


    while True:
        for event in pygame.event.get():
            # if press on quit button the game will be quit
            if event.type==QUIT or (event.type == KEYDOWN and event.key==K_ESCAPE):
                pygame.quit()
                sys.exit()
            # if press space then pay the game
            if event.type==KEYDOWN and(event.key==K_SPACE or event.key==K_UP):
                # if player position is more than 0 then add the velocity
                if playery>0:
                    playerVelY = playerFlpAccv
                    playerFlapped=True
                    Game_Sounds['wing'].play()

        # if the bird is collide with the pipes then collide function should be call and gameOver
        crashTest=isCollide(playerx,playery,upperPipes,lowerPipes)#this function is return true if it is crased 
        if crashTest:
            return
        
        #check for score
        playerMidPos=playerx+Game_Sprites['player'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos=pipe['x']+Game_Sprites['pipe'][0].get_width()/2
            if pipeMidPos <= playerMidPos < pipeMidPos+4:
                score +=1
                Game_Sounds['point'].play()


        # addd the velocity for the player 
        if playerVelY <playerMaxVelY  and not playerFlapped:
            playerVelY += playerAccY

        if playerFlapped:
            playerFlapped=False

        playerHeight=Game_Sprites['player'].get_height()
        playery=playery+ min(playerVelY ,GroundY -playery-playerHeight)
        
        # move pipes to the left
        for upperpipe  ,lowerpipe in zip(upperPipes,lowerPipes):
            # add velocityX to the pipes
            upperpipe['x'] += pipeVelX
            lowerpipe['x'] += pipeVelX

        #add a new pipe
        
        if 0<upperPipes[0]['x']<5:
            newpipe=getRandomPipe()
            # append a new pipe
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])

        # if the pipe is out of out of the screen remove it
        if upperPipes[0]['x'] < -Game_Sprites['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        # lets blit our sprites now.
        SCREEN.blit(Game_Sprites['background'],(0,0))
        for upperPipe ,lowerPipe in zip(upperPipes,lowerPipes):
            SCREEN.blit(Game_Sprites['pipe'][0],(upperPipe['x'],upperPipe['y']))
            SCREEN.blit(Game_Sprites['pipe'][1],(lowerPipe['x'],lowerPipe['y']))
            
        SCREEN.blit(Game_Sprites['base'],(basex,GroundY))
        SCREEN.blit(Game_Sprites['player'],(playerx,playery))
        myDigits=[int(x) for x in list(str(score))]
        width=0
        for digit in myDigits:
            width += Game_Sprites['numbers'][digit].get_width()
        Xoffset=(ScreenWidth- width)/2

        for digit in myDigits:
            SCREEN.blit(Game_Sprites['numbers'][digit],(Xoffset,ScreenWidth*0.12))
            Xoffset += Game_Sprites['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)

# when collide this function will execute
def isCollide(playerx,playery,upperPipes,lowerPipes):
    # if the player is out of screen or touches to the ground the the player ias out
    if playery>GroundY-25 or playery<0:
        Game_Sounds['hit'].play()
        return True

    for pipe in upperPipes:
        # if player touches to the upper pipe then the player is out
        pipeHeight=Game_Sprites['pipe'][0].get_height()
        if (playery < pipeHeight +pipe['y'] and abs(playerx - pipe['x'])< Game_Sprites['pipe'][0].get_width()):
            Game_Sounds['hit'].play()
            return True

        
    for pipe in lowerPipes:
        # if player touches to the lower pipe then the player is out
        if playery +Game_Sprites['player'].get_height() > pipe['y'] and abs(playerx - pipe['x'])< Game_Sprites['pipe'][0].get_width():
            Game_Sounds['hit'].play()
            return True
    return False

# generate rando pipes
def getRandomPipe():
    pipeHeight=Game_Sprites['pipe'][0].get_height()
    offset=ScreenHeight/3
    y2=offset+random.randrange(0,int(ScreenHeight -Game_Sprites['base'].get_height() - 1.2*offset))
    pipeX=ScreenWidth+10
    y1=pipeHeight -  y2+offset
    pipe=[
        {'x':pipeX , 'y':-y1}, #upper pipe
        {'x':pipeX , 'y':y2} #lower pipe
    ]
    return pipe

if __name__ == "__main__":
    # this will the main point where game stats
    pygame.init()#initiallize pygame moduls
    FPSCLOCK=pygame.time.Clock()
    pygame.display.set_caption("Flappy bird")
    Game_Sprites['numbers']=(

        pygame.image.load('0.png').convert_alpha(),
        pygame.image.load('1.png').convert_alpha(),
        pygame.image.load('2.png').convert_alpha(),
        pygame.image.load('3.png').convert_alpha(),
        pygame.image.load('4.png').convert_alpha(),
        pygame.image.load('5.png').convert_alpha(),
        pygame.image.load('6.png').convert_alpha(),
        pygame.image.load('7.png').convert_alpha(),
        pygame.image.load('8.png').convert_alpha(),
        pygame.image.load('9.png').convert_alpha()
    )
    Game_Sprites['message']=pygame.image.load('message.png').convert_alpha()
    Game_Sprites['base']=pygame.image.load('base.png').convert_alpha()
    Game_Sprites['pipe']=(
        pygame.transform.rotate(pygame.image.load(Pipe).convert_alpha(),180),
        pygame.image.load(Pipe).convert_alpha(),

    )

    #game sounds
    Game_Sounds['die']=pygame.mixer.Sound('die.wav')
    Game_Sounds['hit']=pygame.mixer.Sound('hit.wav')
    Game_Sounds['point']=pygame.mixer.Sound('point.wav')
    Game_Sounds['swoosh']=pygame.mixer.Sound('swoosh.wav')
    Game_Sounds['wing']=pygame.mixer.Sound('wing.wav')
   
    Game_Sprites['background']=pygame.image.load(Background).convert()
    Game_Sprites['player']=pygame.image.load(Player).convert_alpha()

    while True:
        welcomeScreen()
        mainGame()
        









