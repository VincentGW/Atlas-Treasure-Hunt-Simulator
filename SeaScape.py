#THIS CODE IS A WIP
#NEXT: EFFECTIVELY USE OOP TO LEVERAGE THE MAPGEN() FUNC
#F6 RUNS THIS PROGRAM IN NPP
import random
import pygame as pg

#Variables
black = (0, 0, 0)
blue = (55, 95, 210)
green = (20, 180, 70)
white = (255, 255, 255)
red = (255, 0, 0)
x_resolution = 800
y_resolution = 600
tile = x_resolution/16
x = 5
y = 5
base_map = []
for i in range(0, 17):
    base_map.append(range(0,13))
pg.font.init()
coords_font = pg.font.Font('freesansbold.ttf', 10)

#User Defined Functions    
def Draw(color, origin_list, border):
    pg.draw.rect(gameDisplay, color, origin_list, border)

def rr(a, b):
    return random.randrange(a, b, 1)

#Main running functionality
gameDisplay = pg.display.set_mode((x_resolution, y_resolution))
running = True
while running:
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
    gameDisplay.fill(black)
    sea = (rr(50,60), rr(90,100), rr(205,215))
    coords = [x+1, y+1]
    n = -1
    for e in base_map:
            n = n+1
            for i in e:
                Draw(sea, [n*tile, i*tile, 49, 49], 0)
    Draw(red, [x*tile, y*tile, 49, 49], 2)
    coords_text = coords_font.render('coords: '+str(coords), True, white)
    coords_textRect = coords_text.get_rect()
    coords_textRect.center = (x_resolution - 755, y_resolution - 7)
    gameDisplay.blit(coords_text, coords_textRect)
    pg.display.update()
