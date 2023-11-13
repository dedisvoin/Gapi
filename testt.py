from api.lib import *

win = Window(size=[1920/2,1080/2])

sheats = DataLoader().Load_from_file(r'api\test.data')

tiles_scale(sheats['t1'], 6)
tiles_scale(sheats['t2'], 6)

m = [
    [1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,1,1],
    [1,0,1,1,0,0,0,1,1],
    [1,0,1,0,0,1,0,1,1],
    [1,0,0,0,0,1,0,0,1],
    [1,2,2,2,2,1,0,0,1],
    [1,0,2,2,0,0,0,0,1],
    [1,0,2,2,0,1,1,0,1],
    [1,0,0,0,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1],
]


m1 = create_map_surf_by_tilesheats_and_array_no_connect({1:sheats['t1'],2:sheats['t2']}, m)
m2 = create_map_surf_by_tilesheats_and_array({1:sheats['t1'],2:sheats['t2']}, m)

while win(fps='max'):

    win.surf.blit(m1, [65,0])
    win.surf.blit(m2, [500,0])
    

    

