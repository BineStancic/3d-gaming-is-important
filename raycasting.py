########################
## MAKING 3D balls

import pygame
import numpy as np
import math
import cmath
from scipy.interpolate import interp1d

pygame.init()

wn_x, wn_y = (500, 500)
wn = pygame.display.set_mode((1000, 500))
font = pygame.font.SysFont('comicsans', 20, True)


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
        self.vel = 5
        self.max = 60
        self.min = 0
        #self.fov = 90
        for i in range(self.min, self.max, 1):
            radians = math.radians(i)
            dir_vec = [1000*math.cos(radians), 1000*math.sin(radians)]
            self.rays.append(Ray(self.pos, dir_vec))

    ###### CREATE A PLAYER ANGLES FUNCTION THAT YOU CAN CALL IN rotate.

    def update_fov(self):
        self.rays = []
        for i in range(self.min, self.max, 1):
            radians = math.radians(i)
            dir_vec = [1000*math.cos(radians), 1000*math.sin(radians)]
            self.rays.append(Ray(self.pos, dir_vec))
            #if i == (self.max - self.min)*0.5:
            #    self.heading = dir_vec



    def draw(self):
        player1.movement()

        pygame.draw.circle(wn, (255,0,0), (self.pos), 2)
        for rayzz in self.rays:
            rayzz.draw(wn)

    #####MOVE METHOD FOR PLAYER BASED ON KEY DIRECTIONSSS SO FAR X<Y FROM MOUSE POSSS!!!!
    '''
    def move(self,x,y):
        self.pos[0] = x
        self.pos[1] = y
    '''
    def movement(self):
        if keys[pygame.K_a] and self.pos[0] > 5:
            self.pos[0] -= self.vel
        if keys[pygame.K_d] and self.pos[0] < wn_x - 5:
            self.pos[0] += self.vel
        if keys[pygame.K_w] and self.pos[1] > 5:
            self.pos[1] -= self.vel
        if keys[pygame.K_s] and self.pos[1] < wn_y - 5:
            self.pos[1] += self.vel




    def rotate(self, min_change, max_change):
        self.max = self.max + max_change
        self.min = self.min + min_change
        self.update_fov()

    '''
    def rotate(self, atm):
        vel = [1000*math.cos(self.heading), 1000*math.sin(self.heading)]
        np.append(self.pos, vel)
        print('rot')
        print(vel)


    def rotate(self,angle):
        self.heading += angle
        index = 0
        for i in range(-self.fov/2, self.fov/2, 1):
            radians = math.radians(i)
            dir_vec = [1000*math.cos(radians), 1000*math.sin(radians)]
            self.rays[index].append(Ray(self.pos, dir_vec + self.heading))
    '''


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

    def look_balls(self, walls):
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

    '''
    def look_ball(self, walls, balls):
        scene = []
        for i in range(len(self.rays)):
            rayzz = self.rays[i]
            closest_w = 0
            closest_b = 0
            bool = False
            record = 10000
            for wall in walls:
                for ball in balls:
                    point_w = rayzz.impact(wall)
                    point_b = rayzz.impact(ball)
                    if point_w != False:
                        dist_w = math.hypot(point_w[0] - self.pos[0], point_w[1] - self.pos[1])
                        #print(dist_w)
                        if point_b != False:
                            dist_b = math.hypot(point_b[0] - self.pos[0], point_b[1] - self.pos[1])
                            if dist_w < record:
                                record = dist_w
                                closest = point_w
                                bool = True
            if bool == True:
                #print("closest ray")
                pygame.draw.line(wn, (255,255,255), (self.pos), (closest))
            scene.append(record)
        return scene
    '''

class Object():
    def __init__(self, x1, y1, x2, y2):
        self.a = np.array([x1,y1])
        self.b = np.array([x2,y2])

    def topdown_draw(self, wn):
        pygame.draw.line(wn, (255,0,0), (self.a), (self.b))

    def fps_draw(self):
        return


walls = []
walls.append(Wall(0, 0, 500, 0))
walls.append(Wall(0, 0, 0, 500))
walls.append(Wall(500, 0, 500, 500))
walls.append(Wall(0, 500, 500, 500))

walls.append(Wall(50, 50, 50, 150))
walls.append(Wall(100, 0, 100, 100))
walls.append(Wall(50, 100, 100, 100))
walls.append(Wall(0, 250, 100, 250))
walls.append(Wall(100, 250, 100, 300))
walls.append(Wall(200, 50, 200, 300))
walls.append(Wall(200, 300, 300, 300))
walls.append(Wall(100, 250, 100, 300))


#ADD more walls to create a map
keys = pygame.key.get_pressed()



player1 = Player(200,200)
balls = []
balls.append(Object(10, 20, 20, 20))
balls.append(Object(350,350,370,350))
#ray1 = ray(200,200)

def drawGame():
    score = 0
    wn.fill((0,0,0))
    #x,y = pygame.mouse.get_pos()
    #player1.move(x,y)

    #if keys[pygame.K_a]:
    #    player1.rotate(-1, -1)
    #if keys[pygame.K_d]:
    #    player1.rotate(1,1)






    for wall in walls:
        wall.draw(wn)



    #3DDDDDDDDDD
    scene = player1.look(walls)

    #print(scene)
    #2 times because of the 500 pixels of top down!!
    elem_w = wn_x/len(scene)
    for i in range(len(scene)):
        map1 = interp1d([0,708],[255,0]) ###708 is the longest diagonal
        adjusted = map1(scene[i])
        map2 = interp1d([0,708],[wn_y,0])
        height2 = map2(scene[i])
        #Centre of rectangle
        x_cen = (i*elem_w + elem_w/2)
        y_cen = wn_y/2
        #Converted to corner axis based on width, height
        pygame.draw.rect(wn, (adjusted, adjusted, adjusted), (wn_x + (x_cen - elem_w/2), y_cen -height2 /2, elem_w, height2))



    #######################DRAWING BALLS

    for ball in balls:
        ball.topdown_draw(wn)

    ball_view = player1.look_balls(balls)
    #elem_w2 = wn_x/(len(ball_view)+1)
    #print(ball_view)
    ball_exist = []
    for i in range(len(ball_view)):
        if ball_view[i] != 10000:
                ball_exist.append(ball_view[i])

    #print(ball_exist)
    if len(ball_exist) != 0:
        ball_dist = sum(ball_exist)/ len(ball_exist)
        text = font.render('Distance to ball: ' +str(ball_dist), 1, (255,0,0))
        wn.blit(text, (10, 10))
        if ball_dist == 0:
            print("yeet")
            balls.pop()


    pygame.display.update()


run = True
while run:
    keys = pygame.key.get_pressed()

    pygame.event.set_grab(True)
    pygame.mouse.set_pos = (250, 250)
    mouse_move = (0,0)
    for event in pygame.event.get():
        if keys[pygame.K_ESCAPE]:
            run = False

        if event.type == pygame.MOUSEMOTION:
            mouse_move = event.rel
        if mouse_move != (0,0):
            x_rotation = np.sign(mouse_move[0])
            player1.rotate(x_rotation, x_rotation)

    pygame.mouse.set_visible(False)


    keys = pygame.key.get_pressed()
    player1.movement()
    drawGame()


pygame.quit()
