from Functions import *

#Main running functionality
running = True
bazarmode = False
menu_cursor = None
invtoggle = None
Hermanostoggle = None
landwalk = False
Nether = False
questkeys = [0]
m = None
yn = None
quest = 0
counter = 0
metamap = Metamap().metagrid
nether_metamap = NetherMetamap().metagrid
overworld_atlas = Atlas(metamap)
underworld_atlas = Atlas(nether_metamap)
current_map = metamap[meta_x][meta_y]
current_nethmap = nether_metamap[meta_x][meta_y]
current_map_grid = current_map.grid
current_nethmap_grid = current_nethmap.grid
selected_tile = current_map_grid[x][y]
pg.key.set_repeat(440,220)

while running:
    xbeforemove = x
    ybeforemove = y
    metaxbeforemove = meta_x
    metaybeforemove = meta_y
    if menumode == True:
        m = menu()
        if m == 'y':
            yn = m
        elif m == 'n':
            yn = m
        elif m == False:
            menumode = False
            bazarmode = False
            invtoggle = False
            atlastoggle = False
            spacetoggle = False
            yn = None
            m = None
            counter = 0
            if inventory["Fishing Pole"] == 1 and quest == 0:
                quest = 1
                inventory["Gold"] = inventory["Gold"] - 100
            if inventory["Potion Effects"] == "Active" and quest == 5:
                quest = 6
                inventory["Gold"] = inventory["Gold"] - 100
                inventory["Coral"] = inventory["Coral"] - 10
                landwalk = True
            if selected_tile.hermanos == True:
                if questkeys[0] < 5:
                    quest = quest + 1
                selected_tile.hermanos = False

    else:
        keys = key_parser(x,y)
        x = keys[0]
        y = keys[1]
        running = keys[2]
        invtoggle = keys[3]
        spacetoggle = keys[4]
        atlastoggle = keys[5]
        move_bool = keys[6]
        
    try:
        bound = boundary_checker(x, y, xbeforemove, ybeforemove, meta_x, meta_y, metaxbeforemove, metaybeforemove, metamap, landwalk)
        x = bound[0]
        y = bound[1]
        meta_x = bound[2]
        meta_y = bound[3]
    except:
        x = xbeforemove
        y = ybeforemove
        meta_y = metaybeforemove
        meta_x = metaxbeforemove

    if Nether == True:
        current_nethmap = nether_metamap[meta_x][meta_y]
        current_nethmap_grid = current_nethmap.grid
        selected_tile = current_nethmap_grid[x][y]
    else:
        current_map = metamap[meta_x][meta_y]
        current_map_grid = current_map.grid
        selected_tile = current_map_grid[x][y]

    if selected_tile.bazar == True:
        if landwalk == True:
            None
        else:    
            x = xbeforemove
            y = ybeforemove
            bazarmode = True
            menumode = True

    if landwalk == False:
        if selected_tile.ttype == 'Water':
            None
        elif not selected_tile.ttype == 'Water':
            x = xbeforemove
            y = ybeforemove
    elif landwalk == True:
        land_tally = land_tally_limiter(move_bool, land_tally)
        if land_tally == 4000:
            landwalk = False
        
    if selected_tile.coin == True:
        selected_tile.coin = False
        inventory["Gold"] = inventory["Gold"] + 10
    
    Display.fill(black)
    if Nether == True:
        mapdraw(current_nethmap_grid)
    else:
        mapdraw(current_map_grid)
        itemdraw(current_map_grid)
    coords = [x,y]
    metacoords = [meta_x, meta_y]
    Draw_Cursor(coords, scale)
    coords_text = coords_font.render('coords: ' + str(coords), True, white); coords_textRect = coords_text.get_rect(); coords_textRect.center = (x_resolution - 755, y_resolution - 7)
    Display.blit(coords_text, coords_textRect)
    if landwalk == True:
        potion_text = coords_font.render('You have ' + str(4000 - land_tally) + ' steps before potion effects end', True, white); potion_textRect = potion_text.get_rect(); potion_textRect.center = (x_resolution - scale*2, y_resolution - 7)
        Display.blit(potion_text, potion_textRect)
    if invtoggle == True:
        menumode = True
        display_inventory(inventory)
    if bazarmode == True:
        bazar(yn, quest)
    if spacetoggle == True:
        if not selected_tile.hermanos == True:
            menumode = True
            spacebar_text = space(selected_tile, counter)
            space_text = coords_font.render(f'{spacebar_text[0]}', True, white); space_textRect = space_text.get_rect(); space_textRect.center = (x_resolution/2, y_resolution - y_resolution/24)
            Display.blit(space_text, space_textRect)
            counter = spacebar_text[1]
        else:
            menumode = True
            questkeys = hermanos(quest, hasatlas)
            quest = questkeys[0]
            hasatlas = questkeys[1]
    if atlastoggle == True:
        if hasatlas == True:
            menumode = True
            blnk = blink()
            if Nether == False:
                overworld_atlas.draw_atlas(coords, metacoords, blnk, Nether)
            else:
                underworld_atlas.draw_atlas(coords, metacoords, blnk, Nether)
    
    if selected_tile.hole == True and keys[4] == True:
        Nether = True
        spacetoggle = False
        menumode = False
        landwalk = False
        
    if selected_tile.goal == True:
        Credits()
        menumode = True
        
    pg.display.update()
