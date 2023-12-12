import pygame as pg 
import numpy as np
import sys

#
# Первоначальная конфигурация 
#
SCREEN_HEIGHT = 400 # fixme: Поменять на 720
SCREEN_WIDTH = 1280
MOVESPACE = np.pi*SCREEN_HEIGHT
FPS = 120
GRID_SPEED = 2
PLAYER_SPEED = 10
VOID_RADIUS = 100

# Цвета 
BLACK = (0,0,0)
WHITE = (255,255,255)
PURPLE = (181,100,227)

def ctx(x):
    return x-SCREEN_WIDTH/2
def ctx_back(x):
    return x+SCREEN_WIDTH/2
def cty(y):
    return SCREEN_HEIGHT-y
def cty_back(y):
    return SCREEN_HEIGHT-y
def out(xc,yc): # Характеристики для вывода картинки
    r=(VOID_RADIUS+SCREEN_HEIGHT-yc)/2
    phi=xc*2*np.pi/MOVESPACE
    x=SCREEN_WIDTH/2+r*np.sin(phi)
    y=SCREEN_HEIGHT/2+r*np.cos(phi)
    return(x,y,r,phi)

class Player:
    def __init__(self,x=ctx_back(0),y=cty_back(0)):
        self.move_direction=0
        self.r = 30
        self.x = x 
        self.y = y 
        self.color = PURPLE 
    def draw(self):
        #pg.draw.circle(screen,self.color,[self.x,self.y],self.r)
        outc = out(ctx(self.x),cty(self.y))
        pg.draw.circle(screen,self.color,[outc[0],outc[1]],self.r)
    def move_left(self):
        self.x-=PLAYER_SPEED
        self.x = ctx(self.x)
        if self.x<-MOVESPACE/2: 
            self.x = MOVESPACE + self.x
        self.x=ctx_back(self.x)
    def move_right(self):
        self.x+=PLAYER_SPEED
        self.x = ctx(self.x)
        if self.x>MOVESPACE/2: 
            self.x = -MOVESPACE + self.x
        self.x=ctx_back(self.x)

class Test:
    def __init__(self):
        self.rows_number = 0
        self.circles_number = 7
        self.rows_crds = [i*SCREEN_HEIGHT/self.rows_number for i in range(0,self.rows_number)]
        self.circles_rds = [i*SCREEN_HEIGHT*2/self.circles_number for i in range(1,self.circles_number)]

    def colorfunc(self, min, current):
        return(255*current/min/7)
    
    def circles_draw(self):
        rds = self.circles_rds

        for i in range(0,len(rds)):
            c = self.colorfunc(SCREEN_HEIGHT*2/self.circles_number, rds[i])
            pg.draw.circle(screen,(c,c,c),[ctx_back(0),cty_back(0)-SCREEN_HEIGHT/2],self.circles_rds[i], int(0.01*self.circles_rds[i]))
        
    def circles_move(self):
        rds = self.circles_rds
        for i in range(0,len(rds)):
            self.circles_rds[i]+=GRID_SPEED
            if self.circles_rds[i]>SCREEN_HEIGHT*2: self.circles_rds[i]=SCREEN_HEIGHT*2/self.circles_number

    def boundaries(self):

        def makeLines(coe,count):
            out1 = out(-MOVESPACE*coe/count, 0)
            out2 = out(-MOVESPACE*coe/count, 3*SCREEN_HEIGHT)
            pg.draw.line(screen,WHITE,[out1[0],out1[1]],[out2[0],out2[1]], 2)
            out1 = out(MOVESPACE*coe/count, 0)
            out2 = out(MOVESPACE*coe/count, 3*SCREEN_HEIGHT)
            pg.draw.line(screen,WHITE,[out1[0],out1[1]],[out2[0],out2[1]], 2)

        [makeLines(i,10) for i in range(0,12)] 

    def rows_move(self):
        crds = self.rows_crds
        for i in range(0,len(crds)):
            self.rows_crds[i]+=GRID_SPEED
            if self.rows_crds[i] >= SCREEN_HEIGHT: 
                self.rows_crds[i]=self.rows_crds[i]-SCREEN_HEIGHT
    
    def rows_draw(self):
        for el in self.rows_crds:
            pg.draw.line(screen,WHITE,[0,el],[SCREEN_WIDTH,el])

pg.init()
screen = pg.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
clock = pg.time.Clock()


test = Test()
player = Player()

pg.display.update()

left_pressed, right_pressed = False, False 

while True:
    screen.fill(BLACK)

    test.boundaries()
    test.rows_move()
    test.rows_draw()
    test.circles_move()
    test.circles_draw()

    player.draw()

    for event in pg.event.get():
        if event.type == pg.KEYDOWN and event.key == pg.K_a:
            left_pressed = True
            right_pressed = False
        if event.type == pg.KEYDOWN and event.key == pg.K_d:
            right_pressed = True
            left_pressed = False
        if event.type == pg.KEYUP and event.key == pg.K_a:
            left_pressed = False 
        if event.type == pg.KEYUP and event.key == pg.K_d:
            right_pressed = False 
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

    if left_pressed:
        player.move_left()
    if right_pressed:
        player.move_right()

    pg.display.flip()
    clock.tick(FPS)
    
