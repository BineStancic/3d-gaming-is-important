import pygame
import numpy as np
import math

pygame.init()

wn_x, wn_y = (500, 500)
wn = pygame.display.set_mode((wn_x, wn_y))

class wall():
    def __init__(self, x1, y1, x2, y2):
        self.a = np.array([x1,y1])
        self.b = np.array([x2,y2])

    def draw(self, wn):
        pygame.draw.line(wn, (255,255,255), (self.a), (self.b))


class ray():
    def __init__(self, x, y):
        self.pos = np.array([x,y])
        #self.dir = np.array([0,1])
        self.dir = np.angle([0., 1.0j])

        ###POSITION MUST BE IN ANGLE CHECK ARRAY ANGLE

    def point(self, x, y):
        self.dir[0] = x - self.pos[0]
        self.dir[1] = y - self.pos[1]

    def draw(self, wn):
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
            px,py = (x1 + t*(x2 - x1), y1 + t*(y2-y1))
            return(px,py)
        else:
            print('miss')



class player():
    def __init__(self, x, y):
        self.pos = np.array([x,y])
        self.rays = []
        for i in range(359):
            self.rays.append(ray(self.pos, math.radians(i)))

    def draw(self):
        pygame.draw.circle(wn, (255,0,0), (self.pos), 2)
        for rayzz in self.rays:
            rayzz.draw(wn)



wall1 = wall(300, 100, 300, 400)
player1 = player(100,100)
#ray1 = ray(200,200)


def drawGame():
    wn.fill((0,0,0))
    wall1.draw(wn)


    x,y = pygame.mouse.get_pos()
    #ray1.point(x,y)
    #print(x,y)
    #ray1.impact()
    #ray1.draw(wn)
    player1.draw()
    pygame.display.update()

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    drawGame()


pygame.quit()
