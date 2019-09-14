import pygame
import numpy as np

pygame.init()

wn_x, wn_y = (500, 500)
wn = pygame.display.set_mode((wn_x, wn_y))

class wall():
    def __init__(self, x1, y1, x2, y2):
        self.a = np.array([x1,y1])
        self.b = np.array([x2,y2])

    def show(self, wn):
        pygame.draw.line(wn, (255,255,255), (self.a), (self.b))

        #print(self.a)
        #DRAW circle at point the ray hits in drwar def

class ray():
    def __init__(self, x, y):
        self.pos = np.array([x,y])
        self.dir = np.array([0,1])

    def point(self, x, y):
        self.dir[0] = x - self.pos[0]
        self.dir[1] = y - self.pos[1]

    def show(self, wn):
        pygame.draw.line(wn, (255,255,255), (self.pos), (self.pos + self.dir))

    def impact(self):
        #wall positions
        x1 = wall1.a[0]
        y1 = wall1.a[1]
        x2 = wall1.b[0]
        y2 = wall1.b[1]

        #ray positions
        x3 = self.pos[0]
        y3 = self.pos[1]
        x4 = self.pos[0] + self.dir[0]
        y4 = self.pos[1] + self.dir[1]

        #check for intersectio float needed because otherwise int (not accurate)
        den = float((x1 - x2)*(y3 - y4) - (y1 - y2)*(x3 - x4))
        t = float(((x1 - x3)*(y3 - y4) - (y1 - y3)*(x3 - x4))/den)
        u = -float(((x1 - x2)*(y1 - y3) - (y1 - y2)*(x1 - x3))/den)

        if(t >= 0. and t <= 1. and u >= 0. and u <= 1.):
            print('Intersect')
        else:
            print('miss')




wall1 = wall(300, 100, 300, 400)
ray1 = ray(200,200)


def drawGame():
    wn.fill((0,0,0))
    wall1.show(wn)


    x,y = pygame.mouse.get_pos()
    ray1.point(x,y)
    #print(x,y)
    ray1.impact()
    ray1.show(wn)
    pygame.display.update()

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    drawGame()


pygame.quit()
