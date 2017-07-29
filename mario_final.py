#Import Modules

import pygame,random,sys
from pygame.locals import *
pygame.init()

#Initializing variables

window_width = 1200
window_height = 600

blue = (0,0,255)
black = (0,0,0)
white = (255,255,255)

fps = 20
level = 0
addnewflamerate = 20

#defining the required function
class dragon:
    global firerect, imagerect, Canvas
    up = False
    down = True
    velocity = 15

    #Dragons initial position
    def __init__(self):
        self.image = load_image('dragon.png')
        self.imagerect = self.image.get_rect()
        self.imagerect.right = window_width
        self.imagerect.top = window_height/2
    def update(self):
        #If dragon hits cactus
        if (self.imagerect.top < cactusrect.bottom):
            self.up = False
            self.down = True
        #If dragon hits fire
        if (self.imagerect.bottom > firerect.top):
            self.up = True
            self.down = False
        #When dragon has to move down!
        if (self.down):
            self.imagerect.bottom += self.velocity
        #When dragon has to move up!
        if (self.up):
            self.imagerect.top -= self.velocity

        Canvas.blit(self.image, self.imagerect)
    #Function to get dragon's height-for fireball
    def return_height(self):
        h = self.imagerect.top
        return h
    
class flames:
    flamespeed = 20

    #Fireball initial position
    def __init__(self):
        self.image = load_image('fireball.png')
        self.imagerect = self.image.get_rect()
        self.height = Dragon.return_height() + 20
        self.surface = pygame.transform.scale(self.image, (20,20))
        self.imagerect = pygame.Rect(window_width-106, self.height, 20, 20)

    #To move fireball
    def update(self):
        self.imagerect.left -= self.flamespeed

    #To detect collision
    def collision(self):
        if (self.imagerect.left == 0):
            return True
        else:
            return False

class mario:
    global moveup, movedown, gravity, cactusrect, firerect
    speed = 10
    downspeed = 20
    
    #Mario initial position
    def __init__(self):
        self.image = load_image('maryo.png')
        self.imagerect = self.image.get_rect()
        self.imagerect.topleft = (50, window_height/2)
        self.score = 0

    def update(self):
        #If mario is moving up without colliding cactus
        if (moveup and (self.imagerect.top > cactusrect.bottom)):
            self.imagerect.top -= self.speed
            self.score += 1
        
        #If mario is moving down without colliding fire
        if (movedown and (self.imagerect.bottom < firerect.top)):
            self.imagerect.bottom += self.downspeed
            self.score +=1

        #If in air
        if (gravity and (self.imagerect.bottom < firerect.top)):
            self.imagerect.bottom +=self.speed

def terminate(): #To end the program
    pygame.quit()
    sys.exit()

def waitforkey():
    while True:       #To wait for user to start
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                terminate()
            if (event.type == pygame.KEYDOWN):
                if (event.key == pygame.K_ESCAPE):
                    terminate()
                return

def flamehitsmario(playerrect, flames):      #to check if flame has hit mario or not    
    for f in flame_list:
        if (playerrect.colliderect(f.imagerect)):
            return True
        return False

def drawtext(text, font, surface, x, y):     #To display text on screen
    textobj = font.render(text, 1, white)
    textrect = textobj.get_rect()
    textrect.topleft = (x,y)
    surface.blit(textobj, textrect)

def check_level(score):
    global window_height, level, cactusrect, firerect
    if (score in range(0, 250)):
        firerect.top = window_height - 50
        cactusrect.bottom = 50
        level = 1

    elif (score in range(250, 500)):
        firerect.top = window_height - 100
        cactusrect.bottom = 100
        level = 2
        
    elif (score in range(500, 750)):
        firerect.top = window_height - 100
        cactusrect.bottom = 150
        level = 3

    elif (score in range(750, 1000)):
        firerect.top = window_height - 100
        cactusrect.bottom = 200
        level = 4

def load_image(imagename):
    return pygame.image.load(imagename)


#------------------------End of function-Main code starts-----------------------

mainClock = pygame.time.Clock()
Canvas = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Mario')

#Setting up fonts, sounds and images

font = pygame.font.SysFont(None, 48)
scorefont = pygame.font.SysFont(None, 30)

fireimage = load_image('fire_bricks.png')
firerect = fireimage.get_rect()

cactusimage = load_image('cactus_bricks.png')
cactusrect = cactusimage.get_rect()

startimage = load_image('start.png')
startimagerect = startimage.get_rect()
startimagerect.centerx = window_width/2
startimagerect.centery = window_height/2

endimage = load_image('end.png')
endimagerect = endimage.get_rect()
endimagerect.centerx = window_width/2
endimagerect.centery = window_height/2

pygame.mixer.music.load('mario_theme.wav')
gameover = pygame.mixer.Sound('mario_dies.wav')

#-----------------------Getting to start screen--------------------------------
Canvas.blit(startimage, startimagerect)

pygame.display.update()
waitforkey()

#--------------------------Start the main code---------------------------------
topscore = 0
Dragon = dragon()

while True:

    flame_list = []
    player = mario()
    moveup = movedown = gravity = False
    flameaddcounter = 0

    gameover.stop()
    pygame.mixer.music.play(-1,0.0)
    
    while True:               #the main game loop

        for event in pygame.event.get():
            if (event.type == QUIT):
                terminate()

            if (event.type == KEYDOWN):

                if (event.key == K_UP):
                    movedown = False
                    moveup = True
                    gravity = False

                if (event.key == K_DOWN):
                    movedown = True
                    moveup = False
                    gravity = False

            if (event.type == KEYUP):
                if (event.key == K_UP):
                    moveup = False
                    gravity = True
                if (event.key == K_DOWN):
                    movedown = False
                    gravity = True

                if (event.key == K_ESCAPE):
                    terminate()
                    
        flameaddcounter += 1
        check_level(player.score)

        if (flameaddcounter == addnewflamerate):

            flameaddcounter = 0
            newflame = flames()
            flame_list.append(newflame)


        for f in flame_list:
            flames.update(f)

        for f in flame_list:
            if f.imagerect.left <= 0:
                flame_list.remove(f)

        player.update()
        Dragon.update()

        Canvas.fill(black)
        Canvas.blit(fireimage, firerect)
        Canvas.blit(cactusimage, cactusrect)
        Canvas.blit(player.image, player.imagerect)
        Canvas.blit(Dragon.image, Dragon.imagerect)

        drawtext('Score : %s | Top score : %s | Level : %s' %(player.score, topscore, level), scorefont, Canvas, 350, cactusrect.bottom + 10)

        for f in flame_list:
            Canvas.blit(f.surface, f.imagerect)


        if (flamehitsmario(player.imagerect, flame_list)):
            if (player.score > topscore):
                topscore = player.score
            break

        if ((player.imagerect.top <= cactusrect.bottom) or (player.imagerect.bottom >= firerect.top)):
            if player.score > topscore:
                topscore = player.score
            break
        
        pygame.display.update()

        mainClock.tick(fps)
        #-------------------Inner while loop closed--------------------------
    #Following code is executed when game stops(gameover) by any means
    pygame.mixer.music.stop()
    gameover.play()
    Canvas.blit(endimage, endimagerect)
    pygame.display.update()
    waitforkey()
