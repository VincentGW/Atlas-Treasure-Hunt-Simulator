import pygame as pg
import random
import time

#Colors
black = (0, 0, 0)
black2 = (45, 45, 45)
black3 = (40, 45, 0)
brown = (100, 85, 50)
brown2 = (150, 95, 50)
blue = (55, 95, 210)
darkblue = (55, 75, 190)
green3 = (55, 105, 25)
green2 = (85, 135, 25)
green1 = (110, 165, 30)
white = (255, 255, 255)
red = (255, 0, 0)
mapcoral = (255, 80, 90)
gold3 = (201, 101, 31)
gold2 = (231, 181, 61)
gold1 = (233, 135, 45)
bazar2 = (180, 80, 65)
bazar1 = (160, 110, 65)

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
inventory = {'Gold':0, 'Fishing Pole':0, 'Fish':0, 'Seaweed':0, 'Coral':0, 'Potion Effects':'Inactive'}
showbazar = None
hasatlas = False
menumode = False
land_tally = 0

#Adjustables
nLand = 750 #Out of 1,000 (lower bound) default 750
nShore = 900 #Out of 1,000 (lower bound) default 900
nShadow = 902 #out of 10,000 (lower bound) default 902
nCoin = 9970 #Out of 10,000 (upper bound) default 9970
nFish = 9350 #Out of 10,000 (range bound) default 9350
nSeaweed = 9100 # Out of 10,000 (range bound) default 9100
nCoral = 925 #Out of 10,000 (lower bound) default 925
nBazar = 897 #Out of 900 (upper bound) default 897
nTree = 1 #Out of 750 (lower bound) default 1
nHole = 748 #Out of 750 (upper bound) default 748

#Other Variables
Display = pg.display.set_mode((x_resolution, y_resolution))

#User Defined Functions
def DrawRect(color, origin_list, border):
    pg.draw.rect(Display, color, origin_list, border)
    
def DrawCirc(color, origin, radius):
    pg.draw.circle(Display, color, origin, radius)
    
def Draw_Cursor(coords, scale):
    DrawRect(red, [coords[0]*scale, coords[1]*scale, scale - scale/50, scale - scale/50], 2)
    
def DrawCoin(tile):
    DrawCirc(gold3, (tile.x*scale + (scale/2+1), tile.y*scale + (scale/2+1)), 7); DrawCirc(gold2, (tile.x*scale + (scale/2), tile.y*scale + (scale/2)), 7)
    pg.draw.line(Display, gold1, (tile.x*scale + scale/2 + 4, tile.y*scale + scale/2 - 4), (tile.x*scale + scale/2 - 2, tile.y*scale + scale/2 - 2)); pg.draw.line(Display, gold1, (tile.x*scale + scale/2 + 2, tile.y*scale + scale/2 + 1.5), (tile.x*scale + scale/2 - 4, tile.y*scale + scale/2 + 4))

def DrawTree(tile):
    DrawCirc(green3, (tile.x*scale + (scale/2), tile.y*scale + (scale/2)), 12); DrawCirc(green2, (tile.x*scale + (scale/2), tile.y*scale + (scale/2)), 8); DrawCirc(green1, (tile.x*scale + (scale/2), tile.y*scale + (scale/2)), 4)
    
def DrawHole(tile):
    DrawCirc(brown, (tile.x*scale + (scale/2-1), tile.y*scale + (scale/2-1)), 12); DrawCirc(black2, (tile.x*scale + (scale/2), tile.y*scale + (scale/2)), 12); DrawCirc(black3, (tile.x*scale + (scale/2), tile.y*scale + (scale/2)), 10)
    
def DrawShadow(tile):
    DrawCirc(darkblue, (tile.x*scale + (scale/2-1), tile.y*scale + (scale/2-1)), 16)

def DrawBazar(tile):
    DrawRect(bazar2, [tile.x*scale + (scale/4), tile.y*scale + (scale/4), scale/2, scale/2], 0); DrawRect(bazar1, [tile.x*scale + (scale/3), tile.y*scale + (scale/3), int(scale/3), int(scale/3)], 0)
    
def rr(a, b):
    return random.randrange(a, b, 1)

def blink():
    t = time.time()
    blink = 0
    digits = int(repr(t)[11:13])
    if 0 < digits < 49:
        blink = 0
    elif 50 < digits < 99:
        blink = 1
    return blink

#Objects
class Tile:
    def __init__(self, coors, land_seed, touch_seed):
        self.name = 'Tile ' + str(coors)
        self.sea = (rr(50,55), rr(85,100), rr(195,215))
        self.land = (rr(125,150), rr(140,180), rr(70,75))
        self.shore = (rr(200,220), rr(160,175), rr(120,130))
        self.coin = None
        self.fish = None
        self.seaweed = None
        self.coral = None
        self.bazar = None
        self.tree = None
        self.hole = None
        self.hermanos = None
        Tile.goal = False
        self.locate = coors
        self.x = coors[0]
        self.y = coors[1]
        self.ttype = str()
        self.land_seed = land_seed
        self.touch_seed = touch_seed
        self.randint = rr(1, 10000)
        if self.land_seed == 1:
            self.randint = 0
        if 1 in self.touch_seed:
            self.randint = rr(0,1000)
        if self.randint < nLand:
            self.ttype = 'Land'
        elif self.randint < nShore:
            self.ttype = 'Shore'
        else:
            self.ttype = 'Water'
            
        if self.ttype == 'Water':
            if self.randint > nCoin:
                self.coin = True
            if self.randint > nFish and self.randint < nCoin:
                self.fish = True
            if self.randint > nSeaweed and self.randint < nFish:
                self.seaweed = True
            if self.randint > nShadow and self.randint < nCoral:
                self.coral = True
            if self.randint < nShadow:
                self.hermanos = True
            
        if self.ttype == 'Shore' and self.randint > nBazar:
            self.bazar = True
        
        if self.ttype == 'Land':
            if self.randint < nTree:
                self.tree = True
            if self.randint > nHole:
                self.hole = True
            
    def draw(self, a, b):
        if self.ttype == 'Water':
            DrawRect(self.sea, [a*scale, b*scale, 49, 49], 0)
        elif self.ttype == 'Shore':
            DrawRect(self.shore, [a*scale, b*scale, 49, 49], 0)
        else:
            DrawRect(self.land, [a*scale, b*scale, 49, 49], 0)
            
class NetherTile:
    def __init__(self, coors, land_seed, touch_seed):
        self.name = 'Tile ' + str(coors)
        self.sea = (rr(10,50), rr(10,50), rr(10,50))
        self.land = (rr(140,200), rr(140,200), rr(140,200))
        self.bright = (rr(229,230), rr(229,230), rr(0,1))
        self.coin = None
        self.fish = None
        self.seaweed = None
        self.coral = None
        self.bazar = None
        self.tree = None
        self.hole = None
        self.hermanos = None
        self.goal = None
        self.locate = coors
        self.x = coors[0]
        self.y = coors[1]
        self.ttype = str()
        self.land_seed = land_seed
        self.touch_seed = touch_seed
        self.randint = rr(1, 10000)
        if self.land_seed == 1:
            self.randint = 0
        if 1 in self.touch_seed:
            self.randint = rr(0,1500)
        if self.randint < nLand:
            self.ttype = 'Land'
        else:
            self.ttype = 'Water'
            
        if self.ttype == 'Water':
            if self.randint > 9990:
                self.goal = True    
                
    def draw(self, a, b):
        if self.ttype == 'Water':
            DrawRect(self.sea, [a*scale, b*scale, 49, 49], 0)
            if self.goal == True:
                DrawRect(self.bright, [a*scale, b*scale, 49, 49], 0)
                DrawCirc((rr(200,201), rr(185,186), rr(0,1)), (a*scale + (scale/2-1), b*scale + (scale/2-1)), 20)
        else:
            DrawRect(self.land, [a*scale, b*scale, 49, 49], 0)

class Map:
    def __init__(self, metcoords):
        self.name = 'Metacoords: ' + str(metcoords)
        self.innertest = 'Num unique to ' + str(metcoords) + ' : ' + str(rr(1,99))
        self.grid = []
        self.seeder = []
        self.x = metcoords[0]
        self.y = metcoords[1]
        for xf in range(0, 16):
            s_vertical = []
            for yf in range(0,12):
                island_seed = rr(1,1000)
                if island_seed < 40:
                    island_seed = 1
                else:
                    island_seed = 0
                s_vertical.append(island_seed)
            self.seeder.append(s_vertical)
        
        for x in range(0, 16):
            vertical = []
            for y in range(0,12):
                coor = (x,y)
                ls = self.seeder[x][y]
                try:
                    ts = (self.seeder[x-1][y-1],self.seeder[x-1][y],self.seeder[x-1][y+1],self.seeder[x][y-1],self.seeder[x][y+1],self.seeder[x+1][y-1],self.seeder[x+1][y],self.seeder[x+1][y+1])
                except:
                    ts = (0,0,0,0,0,0,0,0)
                vertical.append(Tile(coor,ls,ts))
            self.grid.append(vertical)
            
class NetherMap:
    def __init__(self, metcoords):
        self.name = 'Metacoords: ' + str(metcoords)
        self.innertest = 'Num unique to ' + str(metcoords) + ' : ' + str(rr(1,99))
        self.grid = []
        self.seeder = []
        self.x = metcoords[0]
        self.y = metcoords[1]
        for xf in range(0, 16):
            s_vertical = []
            for yf in range(0,12):
                island_seed = rr(1,1000)
                if island_seed < 40:
                    island_seed = 1
                else:
                    island_seed = 0
                s_vertical.append(island_seed)
            self.seeder.append(s_vertical)
        
        for x in range(0, 16):
            vertical = []
            for y in range(0,12):
                coor = (x,y)
                ls = self.seeder[x][y]
                try:
                    ts = (self.seeder[x-1][y-1],self.seeder[x-1][y],self.seeder[x-1][y+1],self.seeder[x][y-1],self.seeder[x][y+1],self.seeder[x+1][y-1],self.seeder[x+1][y],self.seeder[x+1][y+1])
                except:
                    ts = (0,0,0,0,0,0,0,0)
                vertical.append(NetherTile(coor,ls,ts))
            self.grid.append(vertical)

class Metamap:
    def __init__(self):
        self.name = 'The only overworld Metamap'
    
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

class NetherMetamap:
    def __init__(self):
        self.name = 'The only underworld Metamap'
    
    def metachart():
        built_metamap = []
        for x in range(0, 16):
            vertical = []
            for y in range(0,12):
                coor = (x,y)
                vertical.append(NetherMap(coor))
            built_metamap.append(vertical)
        return built_metamap

    metagrid = metachart()

class Atlas:
    def __init__(self, metamap_grid):
        self.name = 'This is the Atlas'
        self.atlas = metamap_grid
    
    def draw_atlas(self, coords, metacoords, blink, Nether_mode):
        mapblue = []
        mapland = []
        mapshore = []
        off = x_resolution/scale*(11/4)
        Layer_2 = pg.Surface((x_resolution, y_resolution))
        Layer_2.set_alpha(150)
        Layer_2.fill((0,0,0))
        Display.blit(Layer_2, (0,0))
        coords = coords
        metacoords = metacoords
        atl = self.atlas
        for vertical in atl:
            for map in vertical:
                chunk_x = map.x
                chunk_y = map.y
                for tile_vertical in map.grid:
                    for tile in tile_vertical:
                        dot_x = tile.x
                        dot_y = tile.y
                        if coords[0] == dot_x and coords[1] == dot_y and metacoords[0] == chunk_x and metacoords[1] == chunk_y and blink == 1:
                            pg.draw.rect(Display, red, [x_resolution/8 + off + chunk_x*32 + dot_x*2, y_resolution/4 + chunk_y*24 + dot_y*2, 2, 2], 0)
                        else:
                            if not tile.ttype == "Water":
                                if tile.ttype == "Land":
                                    mapland = tile.land
                                    pg.draw.rect(Display, mapland, [x_resolution/8 + off + chunk_x*32 + dot_x*2, y_resolution/4 + chunk_y*24 + dot_y*2, 2, 2], 0)
                                if tile.ttype == "Shore":
                                    mapshore = tile.shore
                                    pg.draw.rect(Display, mapshore, [x_resolution/8 + off + chunk_x*32 + dot_x*2, y_resolution/4 + chunk_y*24 + dot_y*2, 2, 2], 0)
                            else:
                                if tile.coral == None:
                                    mapblue = tile.sea
                                    pg.draw.rect(Display, mapblue, [x_resolution/8 + off + chunk_x*32 + dot_x*2, y_resolution/4 + chunk_y*24 + dot_y*2, 2, 2], 0)
                                elif tile.coral == True:
                                    pg.draw.rect(Display, mapcoral, [x_resolution/8 + off + chunk_x*32 + dot_x*2, y_resolution/4 + chunk_y*24 + dot_y*2, 2, 2], 0)

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
            if tile.coin == True:
                DrawCoin(tile)
            if tile.bazar == True:
                DrawBazar(tile)
            if tile.hole == True:
                DrawHole(tile)
            if tile.tree == True:
                DrawTree(tile)
            if tile.hermanos == True and inventory["Fishing Pole"] > 0:
                DrawShadow(tile)
                
            ydraw = ydraw + 1
        xdraw = xdraw + 1
                
def display_inventory(inv):
    headerpos = (x_resolution/2, y_resolution/2 - 40)
    goldpos = (x_resolution/2, y_resolution/2 + 40)
    polepos = (x_resolution/2, y_resolution/2 + 80)
    fishpos = (x_resolution/2, y_resolution/2 + 120)
    sweedpos = (x_resolution/2, y_resolution/2 + 160)
    coralpos = (x_resolution/2, y_resolution/2 + 200)
    Layer_2 = pg.Surface((x_resolution, y_resolution))
    Layer_2.set_alpha(130)
    Layer_2.fill((0,0,0))
    inv_head = inv_font.render('~Inventory~', True, white)    
    inv_gold = inv_font.render( "Gold - " + str(inventory["Gold"]), True, white)
    inv_pole = inv_font.render( "Fishing Pole - " + str(inventory["Fishing Pole"]), True, white)
    inv_fish = inv_font.render( "Fish - " + str(inventory["Fish"]), True, white)
    inv_sweed = inv_font.render( "Seaweed - " + str(inventory["Seaweed"]), True, white)
    inv_coral = inv_font.render( "Coral - " + str(inventory["Coral"]), True, white)
    inv_headRect = inv_head.get_rect(); inv_goldRect = inv_gold.get_rect(); inv_poleRect = inv_pole.get_rect(); inv_fishRect = inv_fish.get_rect(); inv_sweedRect = inv_sweed.get_rect(); inv_coralRect = inv_coral.get_rect()
    inv_headRect.center = headerpos; inv_goldRect.center = goldpos; inv_poleRect.center = polepos; inv_fishRect.center = fishpos; inv_sweedRect.center = sweedpos; inv_coralRect.center = coralpos
    Layer_2.blit(inv_head, inv_headRect); Layer_2.blit(inv_gold, inv_goldRect)
    if inventory["Fishing Pole"] > 0:
        Layer_2.blit(inv_pole, inv_poleRect); Display.blit(inv_pole, inv_poleRect)
    if inventory["Fish"] > 0:
        Layer_2.blit(inv_fish, inv_fishRect); Display.blit(inv_fish, inv_fishRect)    
    if inventory["Seaweed"] > 0:
        Layer_2.blit(inv_sweed, inv_sweedRect); Display.blit(inv_sweed, inv_sweedRect)
    if inventory["Coral"] > 0:
        Layer_2.blit(inv_coral, inv_coralRect); Display.blit(inv_coral, inv_coralRect)
    
    
    Display.blit(inv_head, inv_headRect); Display.blit(inv_gold, inv_goldRect);
    Display.blit(Layer_2, (0,0))
    pg.display.update()
    
def menu():
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
            if event.key == pg.K_y:
                return 'y'
            elif event.key == pg.K_n:
                return 'n'
            elif event.key == pg.K_a:
                return False
            if event.key == pg.K_SPACE:
                return False
            elif event.key == pg.K_RETURN:
                return False
    return True

def key_parser(x_in, y_in):
    x = x_in
    y = y_in
    running = True
    k_return = False
    k_space = None
    k_a = None
    move_bool = False
    #Key presses
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
            if event.key == pg.K_RETURN:
                k_return = True
            if event.key == pg.K_LEFT:
                x = x-1
                move_bool = True
            if event.key == pg.K_RIGHT:
                x = x+1
                move_bool = True
            if event.key == pg.K_UP:
                y = y-1
                move_bool = True
            if event.key == pg.K_DOWN:
                y = y+1
                move_bool = True
            if event.key == pg.K_a:
                k_a = True
            if event.key == pg.K_SPACE:
                k_space = True
    return x, y, running, k_return, k_space, k_a, move_bool

def boundary_checker(xin, yin, xbeforemovein, ybeforemovein, metaxin, metayin, metaxbeforemovein, metaybeforemovein, metamapin, landwalkin):
    landwalk = landwalkin
    x = xin; y = yin
    meta_x = metaxin; meta_y = metayin
    xbeforemove = xbeforemovein; ybeforemove = ybeforemovein
    metaxbeforemove = metaxbeforemovein; metaybeforemove = metaybeforemovein
    metamap = metamapin
    if landwalk == True:
        if x == 16:
            meta_x = meta_x + 1
            if meta_x == 16:
                meta_x = 0
            x = 0
        if x == -1:
            meta_x = meta_x - 1
            if meta_x == -1:
                meta_x = 15
            x = 15
        if y == 12:
            meta_y = meta_y + 1
            if meta_y == 12:
                meta_y = 0
            y = 0
        if y == -1:
            meta_y = meta_y - 1
            if meta_y == -1:
                meta_y = 11
            y = 11
        return x, y, meta_x, meta_y
    elif landwalk == False:
        if x == 16:
            meta_x = meta_x + 1
            if meta_x == 16:
                meta_x = 0
            x = 0
            tilechecker = metamap[meta_x][meta_y].grid
            if not tilechecker[x][y].ttype == 'Water':
                meta_x = metaxbeforemove
                x = xbeforemove
        if x == -1:
            meta_x = meta_x - 1
            if meta_x == -1:
                meta_x = 15
            x = 15
            tilechecker = metamap[meta_x][meta_y].grid
            if not tilechecker[x][y].ttype == 'Water':
                meta_x = metaxbeforemove
                x = xbeforemove
        if y == 12:
            meta_y = meta_y + 1
            if meta_y == 12:
                meta_y = 0
            y = 0
            tilechecker = metamap[meta_x][meta_y].grid
            if not tilechecker[x][y].ttype == 'Water':
                meta_y = metaybeforemove
                y = ybeforemove
        if y == -1:
            meta_y = meta_y - 1
            if meta_y == -1:
                meta_y = 11
            y = 11
            tilechecker = metamap[meta_x][meta_y].grid
            if not tilechecker[x][y].ttype == 'Water':
                meta_y = metaybeforemove
                y = ybeforemove
                
        
        return x, y, meta_x, meta_y
    
def bazar(yn, quest):
    yn = yn
    quest = quest
    Layer_2 = pg.Surface((x_resolution, y_resolution))
    Layer_2.set_alpha(130)
    Layer_2.fill((0,0,0))
    bazar_header = inv_font.render('~Sandy Bazar~', True, white)
    if quest == 0:
        if inventory["Gold"] < 99:
            bazar_text = inv_font.render("For 100 gold, you can have this tool that I found.", True, white)
        else:
            bazar_text = inv_font.render("Want to buy this nifty fishing pole for 100 gold? y/n", True, white)
            if yn == 'y':
                inventory["Fishing Pole"] = 1
                bazar_text = inv_font.render("Thank you! (Use spacebar to fish)", True, white)
            elif yn == 'n':
                bazar_text = inv_font.render("Okay! Maybe next time.", True, white)
    else:
        bazar_text = inv_font.render("I'm afraid I'm out of wares! But keep a lookout for coral...", True, white)

    if quest > 4:
        if inventory["Gold"] > 99 and inventory ["Coral"] > 10:
            bazar_text = inv_font.render("Want me to make you a potion that will let you dwell on land? y/n", True, white)
            if yn == 'y':
                inventory["Potion Effects"] = "Active"
                bazar_text = inv_font.render("The formula is unstable, so you'll have to drink it now... have fun!", True, white)
            elif yn == 'n':
                bazar_text = inv_font.render("Okay! Maybe next time.", True, white)       
        else:
            bazar_text = inv_font.render("For 10 coral and 100 gold, I can make you a potion that will change everything!", True, white)
            
    bazar_headRect = bazar_header.get_rect(); bazar_textRect = bazar_text.get_rect()
    bazar_headRect.center = (x_resolution/2, y_resolution/2 - 40); bazar_textRect.center = (x_resolution/2, y_resolution/2 + 40)
    Layer_2.blit(bazar_header, bazar_headRect); Layer_2.blit(bazar_text, bazar_textRect)
    Display.blit(bazar_header, bazar_headRect); Display.blit(bazar_text, bazar_textRect)
    Display.blit(Layer_2, (0,0))
    pg.display.update()
    
def hermanos(quest, hasatlas):
    quest = quest
    hasatlas = hasatlas
    Layer_2 = pg.Surface((x_resolution, y_resolution))
    Layer_2.set_alpha(130)
    Layer_2.fill((0,0,0))
    if quest < 2:
        hermano_header = inv_font.render('~FERNANDO THE MAGIC TALKING FISH~', True, white)
        hermano_text = inv_font.render("Hola, mi hermano has a map you may find useful... Not sure where he went.", True, white)
    elif quest < 3:
        hermano_header = inv_font.render('~MIGUEL THE MAGIC TALKING FISH~', True, white)
        hermano_text = inv_font.render("Lo siento, I am not the hermano you are looking for... Maybe try Julian.", True, white)
    elif quest < 4:
        hermano_header = inv_font.render('~JULIAN THE MAGIC TALKING FISH~', True, white)
        hermano_text = inv_font.render("No Senior, you are looking for a different pescado magico... Keep fishing.", True, white)
    elif quest < 5:
        hermano_header = inv_font.render('~SAN SEBASTIAN THE MAGIC TALKING FISH~', True, white)    
        hermano_text = inv_font.render("No, I'm not related to any of those guys... But I do have a map. (Press A to view)", True, white)
        hasatlas = True
    else:
        hermano_header = inv_font.render('~SOME TALKING FISH~', True, white)
        hermano_text = inv_font.render("The pink dots on your map are areas that have been known to harbor coral.", True, white)
            
    hermano_headRect = hermano_header.get_rect(); hermano_textRect = hermano_text.get_rect()
    hermano_headRect.center = (x_resolution/2, y_resolution/2 - 40); hermano_textRect.center = (x_resolution/2, y_resolution/2 + 40)
    Layer_2.blit(hermano_header, hermano_headRect); Layer_2.blit(hermano_text, hermano_textRect)
    Display.blit(hermano_header, hermano_headRect); Display.blit(hermano_text, hermano_textRect)
    Display.blit(Layer_2, (0,0))
    pg.display.update()
    
    return quest, hasatlas

def space(tile, counter):
    counter = counter
    text = ""
    if inventory["Fishing Pole"] == 0:
        text = "There's nothing here"
        return text, counter
    else:
        if tile.fish == True:
            inventory["Fish"] = inventory["Fish"] + 1
            tile.fish = False
            counter = counter + 1
            text = "You caught something"
            return text, counter
        if tile.seaweed == True:
            inventory["Seaweed"] = inventory["Seaweed"] + 1
            tile.seaweed = False
            counter = counter + 1
            text = "You caught something"
            return text, counter
        if tile.coral == True:
            inventory["Coral"] = inventory["Coral"] + 1
            tile.coral = False
            counter = counter + 1
            text = "You caught something"
            return text, counter
        
        elif counter == 1:
            text = "You caught something"
            return text, counter
        
        else:
            text = "Nothing's biting"
            return text, counter

def land_tally_limiter(inp, recurs):
    land_tally = recurs
    if inp == True:
        land_tally = land_tally + 1
        
    return land_tally
    
def Credits():
    Display.fill((200, 200, 0))
    credits_header = inv_font.render('~Credits~', True, brown)
    credits_text = inv_font.render("A game by Vincent Wisehoon", True, brown)
    credits_text2 = inv_font.render("Good Game", True, brown)            
    credits_headRect = credits_header.get_rect(); credits_textRect = credits_text.get_rect(); credits_text2Rect = credits_text2.get_rect()
    credits_headRect.center = (x_resolution/2, y_resolution/2 - 80); credits_textRect.center = (x_resolution/2, y_resolution/2); credits_text2Rect.center = (x_resolution/2, y_resolution/2 + 80)
    Display.blit(credits_header, credits_headRect); Display.blit(credits_text, credits_textRect); Display.blit(credits_text2, credits_text2Rect) 
    pg.display.update()
