from api.lib import *

win = Window()

p1 = [200,200]
p2 = [500,500]

while win(fps='max'):
    Draw.draw_line(win.surf, p1, p2, 'red')
    
    distance_to_line_stop(p1, p2, Mouse.pos)