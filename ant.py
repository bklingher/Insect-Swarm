import random
#import random as r
import game
from game import *
import pygame
from pygame.locals import *

glb_x = 200
glb_y = 140
x_frame = 1000
y_frame = 700



class Board(object):

    def __init__(self, x, y, count,energy):
        self.x = x
        self.y = y
        self.count = count
        grid = []
        for i in xrange(x):
            grid.append([])
            for j in xrange(y): 
                grid[i].append(None)
        self.map = grid
        a = []
        for i in xrange(x):
            a.append([])
            for j in xrange(y): 
                a[i].append(None)
        self.a = a
        self.energy = energy
        

    ## def randomize(self):
    ##     for i in xrange(self.x):
    ##         for j in xrange(self.y):
    ##             if random.random()>0.9 and self.count>0:
    ##                 self.count -= 1
    ##                 if random.random()>.1:
    ##                     self.map[i][j] = Agent(i,j,i,j,True,0,self.energy)
    ##                 else:
    ##                     self.map[i][j] = Agent(i,j,i,j,False,0,self.energy)

    def randomize(self):
        c = 0
        for i in xrange(self.x):
            for j in xrange(self.y):
                if random.random()>0.9999:
                    for k in xrange(-2,3):
                        for l in xrange(-2,3):
                            if random.random()>.1:
                                if i+k>=0 and i+k<glb_x and j+l>=0 and j+l<glb_y and self.map[k+i][l+j] is None:
                                    self.map[k+i][l+j] = Food(k+i,l+j,random.randint(1,5))
                                    c += 1
        print c
                    

    def setup(self):
        #build hive NUMBER OF ANTS
        self.map[glb_x/2][glb_y/2] = Hive(glb_x/2,glb_y/2,1)

        

        
    def update(self):
        #use first loop to add new food to the board at low probability
        for i in xrange(self.x):
            for j in xrange(self.y):
                if self.map[i][j] is not None:
                    self.map[i][j].setu(self)
        for i in xrange(self.x):
            for j in xrange(self.y):
                if self.map[i][j] is not None:
                    self.map[i][j].tick(self,self.a)
        for i in xrange(self.x):
            for j in xrange(self.y):
                if self.a[i][j] is not None:
                    self.a[i][j].tick(self.a)

    def place(self,obj):
        pass

    def find(self):
        for i in xrange(self.x):
            for j in xrange(self.y):
                if self.map[i][j] is not None:
                    print("x "+str(self.map[i][j].x)+", y "+str(self.map[i][j].y))
        

    def draw(self,screen):

        for i in xrange(self.x):
            for j in xrange(self.y):
                if self.a[i][j] is not None:
                    if self.a[i][j].isBeacon():
                        pygame.draw.circle(screen,pygame.Color(255,0,0),(i*(x_frame/glb_x),j*(y_frame/glb_y)),2,0)
        
        hive1 = None
        for i in xrange(self.x):
            for j in xrange(self.y):
                if self.map[i][j] is not None:
                    if self.map[i][j].isFood():
                        pygame.draw.circle(screen,pygame.Color(0,255,0),(i*(x_frame/glb_x),j*(y_frame/glb_y)),2,0)
                    elif self.map[i][j].isHive():
                        hive1 = self.map[i][j]
                        pygame.draw.circle(screen,pygame.Color(0,0,0),(i*(x_frame/glb_x),j*(y_frame/glb_y)),4,0)
                    else:
                        #test drawing
                        pygame.draw.rect(screen, pygame.Color(0,0,0), ((i-5)*(x_frame/glb_x),(j-5)*(y_frame/glb_y),10*(x_frame/glb_x),10*(x_frame/glb_x)), 1)
                        #
                        pygame.draw.circle(screen,pygame.Color(0,0,0),(i*(x_frame/glb_x),j*(y_frame/glb_y)),2,0)




        fontObj = pygame.font.SysFont("Arial",32)
        msgSurf = fontObj.render("Food: "+str(hive1.food),False,pygame.Color(255,0,0))
        msgRect = msgSurf.get_rect()
        msgRect.topleft = (50, 650)
        screen.blit(msgSurf, msgRect)
    


def main():
    pygame.init()
    screen = pygame.display.set_mode((x_frame,y_frame))
    pygame.display.set_caption("Ants")
    clock = pygame.time.Clock()

    b = Board(glb_x,glb_y,20,100)
    b.randomize()
    b.setup()


    while True:

        
        for event in pygame.event.get():
            if event.type == QUIT:
                raise SystemExit

        screen.fill(pygame.Color(255,255,255))
        b.update()
        b.draw(screen)

        
        pygame.display.update()
        clock.tick(40)

        

if __name__=="__main__":
    main()
    


