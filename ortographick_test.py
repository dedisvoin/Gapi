from api.lib import *



win = Window([1400,800])

poly_size = [40,1]

def draw_up_poly(pos, size, color=(100,100,100)):
    p1 = posing(pos, -size[0]/2)
    p2 = posing(pos, dy=-size[1]/2)
    p3 = posing(pos, size[0]/2)
    p4 = posing(pos, dy=size[1]/2)
    
    Draw.draw_polygone(win.surf, [p1,p2,p3,p4], color,)


def draw_poly_place(gpos=[600,300],size=[20,20]):


    for i in range(size[0]):
        for j in range(size[1]):   
            pos = [
                    gpos[0]+j*poly_size[0]/2+i*poly_size[0]/2,
                    gpos[1]+j*poly_size[1]/2-i*poly_size[1]/2
            ]
            draw_up_poly(pos, poly_size, color=(200,200,200))
      
def tile(pos,size,color,add_size):
    color2 = [
        color[0]-30,
        color[1]-30,
        color[2]-30
    ]
    color3 = [
        color[0]+30,
        color[1]+30,
        color[2]+30+add_size/3
    ]
    size = [
        max(0,size[0]),
        max(0,size[1])
    ]
    draw_up_poly(posing(pos,dy=-add_size), [size[0],size[1]], color3)  
    
    left_pos1 = posing(pos, -size[0]/2, dy=-add_size)
    left_pos2 = posing(pos, dy=size[1]*1.5)
    left_pos3 = posing(pos, -size[0]/2, size[1])
    left_pos4 = posing(pos, dy=size[1]/2-add_size)
    
    right_pos1 = posing(pos, size[0]/2,dy=-add_size)
    right_pos2 = posing(pos, size[0]/2, size[1])
    right_pos3 = posing(pos, dy=size[1]*1.5)
    right_pos4 = posing(pos, dy=size[1]/2-add_size)
    
    Draw.draw_polygone(win.surf, [left_pos2, left_pos3, left_pos1, left_pos4], color2)
    Draw.draw_polygone(win.surf, [right_pos1, right_pos2, right_pos3, right_pos4], color)
    
map = []   
for i in range(20):
    map1 = []
    for j in range(20):
        if random.randint(10,10)>5:
            map1.append([random.randint(60,60),random.randint(10,300),random.randint(0,100)])
        else:
            map1.append(0)
    map.append(map1)

def draw_tile_map(map2,gpos):
    for i in range(len(map2[0])):
        for j in range(len(map2)):
            if map2[i][j] != 0:
                pos = [
                        gpos[0]-j*poly_size[0]/2+i*poly_size[0]/2+len(map)*poly_size[0]/2-poly_size[0]/2,
                        gpos[1]+j*poly_size[1]/2+i*poly_size[1]/2-(len(map[0]))*poly_size[1]/2-poly_size[1]/2
                ]
                tile(pos, poly_size, (160,160,100), deepcopy(map2[i][j][0]))
              
            

t = 0

while win(fps='max'):
    gp = [300,400]
    draw_poly_place(gp)
    if Keyboard.key_pressed('up'):
        poly_size[1]-=1
    if Keyboard.key_pressed('down'):
        poly_size[1]+=1
        
    if Keyboard.key_pressed('left'):
        poly_size[0]-=1
    if Keyboard.key_pressed('right'):
        poly_size[0]+=1

    draw_tile_map(map, gp)
    
    t+=0.1
    for i in range(len(map[0])):
        for j in range(len(map)):
            if map[i][j]!=0:
                map[i][j][0]+=cos(t+i/2+(1-j/4))
                