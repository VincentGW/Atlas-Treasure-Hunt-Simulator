#THIS CODE IS A WIP

import random
import pygame as pg

#Colors
black = (0, 0, 0)
blue = (55, 95, 210)
green = (20, 180, 70)
white = (255, 255, 255)
red = (255, 0, 0)
#Variables
pg.font.init()
coords_font = pg.font.Font('freesansbold.ttf', 10)
x_resolution = 800
y_resolution = 600
scale = int(x_resolution/16)

#User Defined Functions    
def Draw(color, origin_list, border):
    pg.draw.rect(Display, color, origin_list, border)

def rr(a, b):
    return random.randrange(a, b, 1)

#Objects
class Tile:
    def __init__(self, coors):
        self.name = 'Tile ' + str(coors)
        self.sea = (rr(50,55), rr(85,100), rr(195,215))
        self.color = str(self.name) + ' is blue'
        self.locate = coors

    def draw(self, a, b):
        Draw(self.sea, [a*scale, b*scale, 49, 49], 0)

class Map:
    def __init__(self, name):
        self.name = 'Map ' + str(name)
        self.innertest = 'This attribute is unique to ' + name + ' because this variable was define in __init__. Here is the proof: ' + str(rr(1,99))
    
    outertest = 'This attribute is shared by all Maps:' + str(rr(1,99))
    
    def create():
        built_map = []
        for x in range(0, 16):
            vertical = []
            for y in range(0,12):
                coor = (x,y)
                vertical.append(Tile(coor))
            built_map.append(vertical)
        return built_map

    map = create()

#Test Prints for debugging:
    #print(Map('A').map[5][5].locate)
    #print(Map('A').innertest)
    #print(Map('A').outertest)
    #print(Map('B').innertest)
    #print(Map('B').outertest)

#Main running functionality
Display = pg.display.set_mode((x_resolution, y_resolution))
running = True
map = Map('Map1').map
x = 5
y = 5

while running:
    Display.fill(black)
    xdraw = 0
    ydraw = 0
    for column in map:
        ydraw = 0
        for tile in column:
            tile.draw(xdraw,ydraw)
            ydraw = ydraw + 1
        xdraw = xdraw + 1
        
    Draw(red, [x*scale, y*scale, 49, 49], 2)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                x = x-1
            if event.key == pg.K_RIGHT:
                x = x+1
            if event.key == pg.K_UP:
                y = y-1
            if event.key == pg.K_DOWN:
                y = y+1
    coords = [x+1, y+1]
    coords_text = coords_font.render('coords: '+str(coords), True, white)
    coords_textRect = coords_text.get_rect()
    coords_textRect.center = (x_resolution - 755, y_resolution - 7)
    Display.blit(coords_text, coords_textRect)
    pg.display.update()
