import pygame as pg
import random

#Colors
black = (0, 0, 0)
blue = (55, 95, 210)
green = (20, 180, 70)
white = (255, 255, 255)
red = (255, 0, 0)
gold3 = (201, 101, 31)
gold2 = (231, 181, 61)
gold1 = (233, 135, 45)
bazar2 = (160, 110, 50)
bazar3 = (180, 80, 65)
#Variables
pg.font.init()
coords_font = pg.font.Font('freesansbold.ttf', 10)
inv_font = pg.font.Font('freesansbold.ttf', 20)
x_resolution = 800
y_resolution = 600
scale = int(x_resolution/16)
x = 8
y = 6
meta_x = 0
meta_y = 0
inventory = {'Gold':0}
showinventory = None
showbazar = None

#User Defined Functions    
def Draw(color, origin_list, border):
    pg.draw.rect(Display, color, origin_list, border)
    
def DrawCoin(tile):
    pg.draw.circle(Display, gold3, (tile.x*scale + (scale/2+1), tile.y*scale + (scale/2+1)), 7)
    pg.draw.circle(Display, gold2, (tile.x*scale + (scale/2), tile.y*scale + (scale/2)), 7)
    pg.draw.line(Display, gold1, (tile.x*scale + scale/2 + 4, tile.y*scale + scale/2 - 4), (tile.x*scale + scale/2 - 2, tile.y*scale + scale/2 - 2))
    pg.draw.line(Display, gold1, (tile.x*scale + scale/2 + 2, tile.y*scale + scale/2 + 1.5), (tile.x*scale + scale/2 - 4, tile.y*scale + scale/2 + 4))

def DrawBazar(tile):
    pg.draw.circle(Display, bazar2, (tile.x*scale + (scale/2), tile.y*scale + (scale/2)), 11)
    pg.draw.circle(Display, bazar3, (tile.x*scale + (scale/2), tile.y*scale + (scale/2)), 10)
    pg.draw.circle(Display, gold3, (tile.x*scale + (scale/2), tile.y*scale + (scale/2)), 9)
    
def rr(a, b):
    return random.randrange(a, b, 1)

#Objects
class Tile:
    def __init__(self, coors, direct_seed, touch_seed):
        self.name = 'Tile ' + str(coors)
        self.sea = (rr(50,55), rr(85,100), rr(195,215))
        self.land = (rr(125,150), rr(140,180), rr(70,75))
        self.shore = (rr(200,220), rr(160,175), rr(120,130))
        self.gold = (rr(230,231), rr(180,181), rr(59,60))
        self.token = None
        self.bazar = None
        self.locate = coors
        self.x = coors[0]
        self.y = coors[1]
        self.ttype = str()
        self.direct_seed = direct_seed
        self.touch_seed = touch_seed
        self.randint = rr(1, 10000)
        if self.direct_seed == 1:
            self.randint = 0
        if 1 in self.touch_seed:
            self.randint = rr(0,1000)
        if self.randint < 750:
            self.ttype = 'Land'
        elif self.randint < 900:
            self.ttype = 'Shore'
        else:
            self.ttype = 'Water'
            
        if self.randint > 9970:
            self.token = True
        
        if self.ttype == 'Shore' and self.randint > 897:
            self.bazar = True
        
    def draw(self, a, b):
        if self.ttype == 'Water':
            Draw(self.sea, [a*scale, b*scale, 49, 49], 0)
        elif self.ttype == 'Shore':
            Draw(self.shore, [a*scale, b*scale, 49, 49], 0)
        else:
            Draw(self.land, [a*scale, b*scale, 49, 49], 0)
            
class Map:
    def __init__(self, metcoords):
        self.locate = 'Metacoords: ' + str(metcoords)
        self.innertest = 'Num unique to ' + str(metcoords) + ' : ' + str(rr(1,99))
        self.grid = []
        self.seeder = []
        for xf in range(0, 16):
            s_vertical = []
            for yf in range(0,12):
                island_seed = rr(1,1000)
                if island_seed < 50:
                    island_seed = 1
                else:
                    island_seed = 0
                s_vertical.append(island_seed)
            self.seeder.append(s_vertical)
        
        for x in range(0, 16):
            vertical = []
            for y in range(0,12):
                coor = (x,y)
                ds = self.seeder[x][y]
                try:
                    ts = (self.seeder[x-1][y-1],self.seeder[x-1][y],self.seeder[x-1][y+1],self.seeder[x][y-1],self.seeder[x][y+1],self.seeder[x+1][y-1],self.seeder[x+1][y],self.seeder[x+1][y+1])
                except:
                    ts = (0,0,0,0,0,0,0,0)
                vertical.append(Tile(coor,ds,ts))
            self.grid.append(vertical)

class Metamap:
    def __init__(self):
        self.name = 'The only Metamap'
    
    def metachart():
        built_metamap = []
        for x in range(0, 16):
            vertical = []
            for y in range(0,12):
                coor = (x,y)
                vertical.append(Map(coor))
            built_metamap.append(vertical)
        return built_metamap

    metagrid = metachart()

#Functions
def mapdraw(current_map_grid):
    xdraw = 0
    ydraw = 0
    for column in current_map_grid:
        ydraw = 0
        for tile in column:
            tile.draw(xdraw,ydraw)
            ydraw = ydraw + 1
        xdraw = xdraw + 1
        
def itemdraw(current_map_grid):
    xdraw = 0
    ydraw = 0
    for column in current_map_grid:
        ydraw = 0
        for tile in column:
            if tile.token == True:
                DrawCoin(tile)
            if tile.bazar == True:
                DrawBazar(tile)
            ydraw = ydraw + 1
        xdraw = xdraw + 1
                
def display_inventory():
    Layer_2 = pg.Surface((x_resolution, y_resolution))
    Layer_2.set_alpha(130)
    Layer_2.fill((0,0,0))
    inv_text1 = inv_font.render('~Inventory~', True, white)
    inv_text2 = inv_font.render( "Gold - " + str(inventory["Gold"]), True, white)
    inv_textRect1 = inv_text1.get_rect()
    inv_textRect2 = inv_text2.get_rect()
    inv_textRect1.center = (x_resolution/2, y_resolution/2 - 40)
    inv_textRect2.center = (x_resolution/2, y_resolution/2 + 40)
    Layer_2.blit(inv_text1, inv_textRect1)
    Layer_2.blit(inv_text2, inv_textRect2)
    Display.blit(inv_text1, inv_textRect1)
    Display.blit(inv_text2, inv_textRect2)
    Display.blit(Layer_2, (0,0))
    pg.display.update()
    
def bazar():
    Layer_2 = pg.Surface((x_resolution, y_resolution))
    Layer_2.set_alpha(130)
    Layer_2.fill((0,0,0))
    bazar_text1 = inv_font.render('~Sandy Bazar~', True, white)
    bazar_text2 = inv_font.render( "For 100 gold, you can have this tool that I found.", True, white)
    bazar_textRect1 = bazar_text1.get_rect()
    bazar_textRect2 = bazar_text2.get_rect()
    bazar_textRect1.center = (x_resolution/2, y_resolution/2 - 40)
    bazar_textRect2.center = (x_resolution/2, y_resolution/2 + 40)
    Layer_2.blit(bazar_text1, bazar_textRect1)
    Layer_2.blit(bazar_text2, bazar_textRect2)
    Display.blit(bazar_text1, bazar_textRect1)
    Display.blit(bazar_text2, bazar_textRect2)
    Display.blit(Layer_2, (0,0))
    pg.display.update()

#Main running functionality
running = True
menumode = False
menu_cursor = None
Display = pg.display.set_mode((x_resolution, y_resolution))
metamap = Metamap().metagrid
current_map = metamap[meta_x][meta_y]
current_map_grid = current_map.grid
selected_tile = current_map_grid[x][y]
pg.key.set_repeat(440,220)

while running:
    xbeforemove = x
    ybeforemove = y
    metaxbeforemove = meta_x
    metaybeforemove = meta_y
    if menumode == True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
                if event.key == pg.K_LEFT:
                    menu_cursor = None
                if event.key == pg.K_RIGHT:
                    menu_cursor = None
                if event.key == pg.K_UP:
                    menu_cursor = None
                if event.key == pg.K_DOWN:
                    menu_cursor = None
            if event.type == pg.KEYUP:
                if event.key == pg.K_RETURN:
                    showbazar = False
                    menumode = False
    else:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
                if event.key == pg.K_RETURN:
                    showinventory = True
                    showbazar = False
                if event.key == pg.K_LEFT:
                    x = x-1
                if event.key == pg.K_RIGHT:
                    x = x+1
                if event.key == pg.K_UP:
                    y = y-1
                if event.key == pg.K_DOWN:
                    y = y+1
            if event.type == pg.KEYUP:
                if event.key == pg.K_RETURN:
                    showinventory = False
        try:
            if x == 16:
                meta_x = meta_x + 1
                x = 0
                tilechecker = metamap[meta_x][meta_y].grid
                if not tilechecker[x][y].ttype == 'Water':
                    meta_x = metaxbeforemove
                    x = xbeforemove
            if x == -1:
                meta_x = meta_x - 1
                x = 15
                tilechecker = metamap[meta_x][meta_y].grid
                if not tilechecker[x][y].ttype == 'Water':
                    meta_x = metaxbeforemove
                    x = xbeforemove
            if y == 12:
                meta_y = meta_y + 1
                y = 0
                tilechecker = metamap[meta_x][meta_y].grid
                if not tilechecker[x][y].ttype == 'Water':
                    meta_y = metaybeforemove
                    y = ybeforemove
            if y == -1:
                meta_y = meta_y - 1
                y = 11
                tilechecker = metamap[meta_x][meta_y].grid
                if not tilechecker[x][y].ttype == 'Water':
                    meta_y = metaybeforemove
                    y = ybeforemove
        except:
            x = xbeforemove
            y = ybeforemove
            meta_y = metaybeforemove
            meta_x = metaxbeforemove

        current_map = metamap[meta_x][meta_y]
        current_map_grid = current_map.grid
        selected_tile = current_map_grid[x][y]
        if selected_tile.bazar == True:
            showbazar = True
            x = xbeforemove
            y = ybeforemove
        elif not selected_tile.ttype == 'Water':
            x = xbeforemove
            y = ybeforemove

        if selected_tile.token == True:
            selected_tile.token = False
            inventory["Gold"] = inventory["Gold"] + 10
        
        Display.fill(black)
        mapdraw(current_map_grid)
        itemdraw(current_map_grid)
        coords = [x,y]
        metacoords = [meta_x, meta_y]
        Draw(red, [coords[0]*scale, coords[1]*scale, 49, 49], 2)
        coords_text = coords_font.render('coords: ' + str(coords), True, white)
        coords_textRect = coords_text.get_rect()
        coords_textRect.center = (x_resolution - 755, y_resolution - 7)
        Display.blit(coords_text, coords_textRect)
        if showinventory == True:
            display_inventory()
        if showbazar == True:
            menumode = True
            bazar()
        pg.display.update()
        
#Test Prints for debugging:
#print(Map('A').map[5][5].locate)
#print(Map('A').innertest)
#print(Map('A').outertest)
#print(Map('B').innertest)
#print(Map('B').outertest)
