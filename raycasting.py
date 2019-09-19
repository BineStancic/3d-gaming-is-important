########################
## 3D view

import pygame
import numpy as np
import math
import cmath
from scipy.interpolate import interp1d

pygame.init()

wn_x, wn_y = (1000, 500)
wn = pygame.display.set_mode((wn_x, wn_y))

class Wall():
    def __init__(self, x1, y1, x2, y2):
        self.a = np.array([x1,y1])
        self.b = np.array([x2,y2])

    def draw(self, wn):
        pygame.draw.line(wn, (255,255,255), (self.a), (self.b))


class Ray():
    def __init__(self, pos, dir):
        #self.pos = np.array([x,y])
        self.pos = pos
        #print("secondd" +str(self.pos))
        #self.dir = np.array([0,1])
        #
        #
        self.dir = dir   #np.angle(complex([0., 1.0j]), deg = True)

        #self.dir =
        #print("ANGEEEE" +str(self.dir))

        ###POSITION MUST BE IN ANGLE CHECK ARRAY ANGLE

    def point(self, x, y):
        self.dir[0] = x - self.pos[0]
        self.dir[1] = y - self.pos[1]


    #when calling the ray method in player class the position is an array inslide list
    #not valid form
    def draw(self, wn):
        pygame.draw.line(wn, (255,255,255), (self.pos), (self.pos + self.dir))

    def impact(self, wall):
        #wall positions
        x1 = wall.a[0]
        y1 = wall.a[1]
        x2 = wall.b[0]
        y2 = wall.b[1]

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
            #print('Intersect')
            px,py = (x1 + t*(x2 - x1), y1 + t*(y2-y1))
            return(px, py)
        else:
            return(False)



class Player():
    def __init__(self, x, y):
        self.pos = np.array([x,y])
        self.rays = []
        self.heading = 0
        self.fov = 90
        for i in range(-self.fov/2, self.fov/2, 1):
            radians = math.radians(i)
            dir_vec = [1000*math.cos(radians), 1000*math.sin(radians)]
            self.rays.append(Ray(self.pos, dir_vec))

    ###### CREATE A PLAYER ANGLES FUNCTION THAT YOU CAN CALL IN rotate.
    def update_fov(self, fov):
        self.fov = fov
        self.rays = []
        for i in range(-self.fov/2, self.fov/2, 1):
            radians = math.radians(i)
            dir_vec = [1000*math.cos(radians), 1000*math.sin(radians)]
            self.rays.append(Ray(self.pos, dir_vec + self.heading))


    def draw(self):
        pygame.draw.circle(wn, (255,0,0), (self.pos), 2)
        for rayzz in self.rays:
            #print(rayzz)
            rayzz.draw(wn)
#####MOVE METHOD FOR PLAYER BASED ON KEY DIRECTIONSSS SO FAR X<Y FROM MOUSE POSSS!!!!
    def move(self, x, y):
        self.pos[0] = x
        self.pos[1] = y

    '''
    def rotate(self, min_change, max_change):
        #print('change')
        self.max = self.max + max_change
        #print(self.max)
        self.min = self.min + min_change


    def rotate(self, atm):
        vel = [1000*math.cos(self.heading), 1000*math.sin(self.heading)]
        np.append(self.pos, vel)
        print('rot')
        print(vel)
    '''

    def rotate(self,angle):
        self.heading += angle
        index = 0
        for i in range(-self.fov/2, self.fov/2, 1):
            radians = math.radians(i)
            dir_vec = [1000*math.cos(radians), 1000*math.sin(radians)]
            self.rays[index].append(Ray(self.pos, dir_vec + self.heading))



    def look(self, walls):
        scene = []
        for i in range(len(self.rays)):
            rayzz = self.rays[i]
            closest = 0
            bool = False
            record = 10000
            for wall in walls:
                point = rayzz.impact(wall)
                if point != False:
                    dist = math.hypot(point[0] - self.pos[0], point[1] - self.pos[1])
                    ##print(dist)
                    if dist < record:
                        record = dist
                        closest = point
                        bool = True
            if bool == True:
                #print("closest ray")
                pygame.draw.line(wn, (255,255,255), (self.pos), (closest))
            scene.append(record)
        return scene
#walls = Wall(0, 0, wn_x, 0)


walls = []
walls.append(Wall(0, 0, 500, 0))
walls.append(Wall(0, 0, 0, 500))
walls.append(Wall(500, 0, 500, 500))
walls.append(Wall(0, 500, 500, 500))
walls.append(Wall(100, 100, 200, 200))
walls.append(Wall(100, 100, 100, 400))
walls.append(Wall(100, 100, 100, 400))
walls.append(Wall(0, 250, 500, 250))
walls.append(Wall(250, 0, 250, 500))

#ADD more walls to create a map



player1 = Player(200,200)
#ray1 = ray(200,200)


def drawGame():
    wn.fill((0,0,0))

    x,y = pygame.mouse.get_pos()
    player1.move(x,y)


    keys = pygame.key.get_pressed()



    if keys[pygame.K_a]:
        player1.rotate(-1)
    if keys[pygame.K_d]:
        player1.rotate(1)










    for wall in walls:
        wall.draw(wn)

    #3DDDDDDDDDD
    scene = player1.look(walls)
    #print(scene)
    elem_w = wn_x/len(scene)
    for i in range(len(scene)):
        map1 = interp1d([0,500],[255,0])
        adjusted = map1(scene[i])
        map2 = interp1d([0,500],[wn_y,0])
        height2 = map2(scene[i])
        pygame.draw.rect(wn, (adjusted, adjusted, adjusted), (i*elem_w + wn_x/2, 0 + height2/3, elem_w, height2))


    pygame.display.update()

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    drawGame()


pygame.quit()
