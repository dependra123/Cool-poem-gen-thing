import pygame
import random

#make a window
WIDTH, HEIGHT = 800, 600
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Thing")



#make a surface for the road

        
class Road ():
    def __init__(self, maxspeed,blocksize = 15):

        self.maxspeed = maxspeed
        self.roads = []
        self.blocksize = blocksize
    

    
    def draw_roads(self):
        #Set the size of the grid block
        for x in range(0, WIDTH, self.blocksize):
            for y in range(0, HEIGHT, self.blocksize):
                rect = pygame.Rect(x, y, self.blocksize, self.blocksize)
                pygame.draw.rect(screen, (255,255,255), rect, 1)
                self.roads.append(rect)


class Intersection(Road):
    #make a dicatnary of the colours red yellow and green
    
    def __init__(self, colour, x, y):
        colours = {'red': (255,0,0), 'yellow': (255,255,0), 'green': (0,255,0)}
        self.colour = colours[colour]
        self.x = x
        self.y = y
    def place_intersection(self):
        #draw a small square 
        rect = pygame.Rect(self.x, self.y, 5, 5)
        pygame.draw.rect(screen, self.colour, rect, 0)
    
        

class Road_Object(Road):
    def init(self, sprite = pygame.sprite.Sprite):
        self.speed = 0
        
        self.Sprite = sprite
    def sed_speed(self):
        self.speed = random.randint(30, Road.Maxspeed)


class Car():
    def __init__(self, image, road, intersection):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.speed = 0
        self.road = road
        self.intersection = intersection
        self.destination = 0
    def update(self):
        self.speed = self.road.speed()

        
        print (self.speed)
    def destination(self):
        #choose a destionation
        self.destinationx = random.randint(0, WIDTH/self.road.blocksize)
        self.destinationy = random.randint(0, HEIGHT/self.road.blocksize)
       
    def starting_position(self):
        #choose a starting position
        #make sure that the destionation is not the same as the starting position
        self.starting_positionx = random.randint(0, WIDTH/self.road.blocksize)
        self.starting_positiony = random.randint(0, HEIGHT/self.road.blocksize)
        print (WIDTH/self.road.blocksize)
        print (HEIGHT/self.road.blocksize)

        print (self.starting_positionx, self.starting_positiony)
        return self.starting_positionx, self.starting_positiony
    def choose_path(self):
            #choose a path
            #first go straight to the x axis of the destination
            if self.starting_position < self.destination:
                self.pathx = self.starting_position + self.destination
            else:
                self.pathx = self.starting_position - self.destination
            #then go straight to the y axis of the destination
            if self.starting_position < self.destination:
                self.pathy = self.starting_position + self.destination
            else:
                self.pathy = self.starting_position - self.destination

            return self.pathx, self.pathy
    def move(self, pathx, pathy):
        #move the car towards the path x or path y randomly
        if random.randint(0,1) == 0:
            if self.rect.x < pathx:
                self.rect.x += self.speed
            else:
                self.rect.x -= self.speed
        else:
            if self.rect.y < pathy:
                self.rect.y += self.speed
            else:
                self.rect.y -= self.speed
    def draw(self, starting):
        #draw the car on the starting position on the edge of the screen and on the road 
        self.rect.x = starting[0] * self.road.blocksize
        self.rect.y = starting[1] * self.road.blocksize
        screen.blit(self.image, self.rect, (0,0, 250, 25))

        
# draw the road        
def main():
    roadlist = []
    intersectionlist = []
    roads = Road(100, 40)
    car = Car(pygame.image.load('car.png'), roads, intersectionlist)
    for x in range (len(roads.roads)):
        road = Road_Object(sprite = roads.roads[x])
        roadlist.append(road)
    starting = car.starting_position()

    car.draw(starting)

    for road in roadlist:
        road.sed_speed()
    
   
    roads.draw_roads()

    #find to the corrner of each block

    for x in range(0, WIDTH, roads.blocksize):
        for y in range(0, HEIGHT, roads.blocksize):
            intersection = Intersection('yellow', x, y)
            intersection.place_intersection()
            intersectionlist.append(intersection)



    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        
        pygame.display.update()
        pygame.time.delay(10)


main()