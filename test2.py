
from api.lib import *
win = Window([1920,1080])

Colliders.GRAVITY = Vector2(0,1)
cs = Colliders(win.surf)


player = Colliders.CRect([100,50],[50,50],Vector2(0,0), False, Vector2(0,0))

cs.add(Colliders.CRect([40,400], [800,100], trenie=Vector2(0.6,0.1)))
cs.add(Colliders.CRect([400,100], [80,800],trenie=Vector2(0.5,1)))
cs.add(player)
cs.add(Colliders.CRect([300,300], [100,30],trenie=Vector2(0.5,1),colliding_down=False))
cs.add(Colliders.CRect([400,300], [100,30],trenie=Vector2(0.5,1),colliding_down=False))

cs.printing()

c = Camera()

camera_pos = [0,0]

while win():
    
    c.simulate([player.center_x+camera_pos[0], player.center_y+camera_pos[1]], win.center,0.1)
    
    camera_pos[0]-=c.sx
    camera_pos[1]-=c.sy
    
    if Keyboard.key_pressed('up') and player.get_collides()['down']:
        player._speed.y = -20
        
    if Keyboard.key_pressed('left'):
        player._speed.x = -5
        
    if Keyboard.key_pressed('right'):
        player._speed.x = 5
        
    if Keyboard.key_pressed('s'):
        player.h-=0.1
        
    for collider in cs._space:
        pos = [
            collider.x+camera_pos[0],
            collider.y+camera_pos[1]
        ]
    
        Draw.draw_rect(win.surf, pos, collider.wh, 'orange',2)
        
    cs.update()
    