from api.lib import *

win = Window(size=[1400,900], flag=Flags.win_resize)
datas = DataLoader().Load_from_file('mapcreatordata\mapdatas.data')

def get_win_size():
    return win.get_size()

def get_win_center():
    return win.center

class Button:
    def __init__(self, sprite: Sprite, scale, clicked = False) -> None:
        self.sprite = sprite
        self.sprite.scale = scale
        self.pos = [0, 0]
        self.vabor = False
        self.c = clicked
        self.clicked = False
        self.mouse_events = MouseEventHandler()
        self.mouse_events.AddEvent(Mouse(Mouse.left, Mouse.click_event, 'click'))
        
        self.click = False
        
    def update(self, pos):
        self.pos = pos
        self.vabor = False
        self.mouse_events.EventsUpdate()
        self.click = False
        if in_rect(self.pos, self.sprite.size, Mouse.pos):
            self.vabor = True
            self.click = self.mouse_events.GetEventById('click')
            
            if self.mouse_events.GetEventById('click'):
                self.clicked = not self.clicked
            
        
    def render(self, surf):
        if not self.vabor:
            Draw.draw_rect(surf, self.pos, self.sprite.size, (150,150,150), radius=8)
        else:
            Draw.draw_rect(surf, self.pos, self.sprite.size, (180,180,180), radius=8, outline=[(255,255,255),2])
        if self.c:
            if self.clicked:
                Draw.draw_rect(surf, self.pos, self.sprite.size, (150,150,150), radius=8, outline=[(255,255,255),3])
        self.sprite.center = [self.pos[0]+self.sprite.size[0]/2,self.pos[1]+self.sprite.size[1]/2]
        self.sprite.render(surf)

class TextButton:
    def __init__(self, text, font_size, size=[200,30]) -> None:

        self.pos = [0, 0]
        self.size = size
        
        self.string_text = text
        self.font_size = font_size
        self.text = Text('arial', font_size, self.string_text, (200,200,200), True)
        
        self.mouse_events = MouseEventHandler()
        self.mouse_events.AddEvent(Mouse(Mouse.left, Mouse.click_event, 'click'))
        
        self.click = False
        self.clicked = False
        self.vabor = False
        
    def update(self, pos=None):
        if pos is not None:
            self.pos = pos
        self.vabor = False
        self.mouse_events.EventsUpdate()
        self.click = False
        if in_rect(self.pos, self.size, Mouse.pos):
            self.vabor = True
            self.click = self.mouse_events.GetEventById('click')
            
            if self.mouse_events.GetEventById('click'):
                self.clicked = not self.clicked
            
        
    def render(self, surf):
        if not self.vabor:
            Draw.draw_rect(surf, self.pos, self.size, (100,100,100), radius=8)
        else:
            Draw.draw_rect(surf, self.pos, self.size, (150,150,150), radius=8, outline=[(255,255,255),1])
        
        
        self.text.draw(surf, [self.pos[0]+self.size[0]/2,self.pos[1]+self.size[1]/2], True, self.string_text, (200,200,200))

class Table:
    def __init__(self, size, start_pos, name,) -> None:
        self.size = size
        self.start_pos = start_pos
        self.pos = start_pos
        self.bg_color = [160,160,160]
        self.start_size = copy(size)
        
        self.opened = False
        self.pressed = False
        
        self.string_text = name
        self.text = Text('arial', 20, name, [255,255,255], True)
        
        self.mouse_events = MouseEventHandler()
        self.mouse_events.AddEvent(Mouse(Mouse.left, Mouse.click_event, 'click1'))
        self.mouse_events.AddEvent(Mouse(Mouse.left, Mouse.press_event, 'press1'))
        
        self.closed_vabor = False
        self.close_rect = [self.pos[0]+self.size[0]-20,self.pos[1]]
        self.cl = False
        
        
        self.sizing_pressed = False
        
    
    def render(self, render_event: None = None, surf = None):
        if self.opened:
            Draw.draw_rect(surf, self.pos, self.size, self.bg_color, radius=5)
            Draw.draw_rect(surf, self.pos, [self.size[0],20], [100,100,100], radius=(5,5,0,0))
            
            self.text.draw(surf, [self.pos[0]+self.size[0]/2, self.pos[1]+10], text=self.string_text,centering=True)
            
            if not self.closed_vabor:
                Draw.draw_rect(surf, self.close_rect, [20,20], (200,100,100),radius=(0,5,0,0))
            else:
                Draw.draw_rect(surf, self.close_rect, [20,20], (200,150,150),radius=(0,5,0,0))
                
            if self.cl:
                Draw.draw_rect(surf, self.pos, self.size, [150,150,250],2, radius=(5,5,5,5))
                
            if render_event is not None:
                render_event(self.pos, self.size, surf)
            
    def update(self):
        ms = Mouse.speed
        self.mouse_events.EventsUpdate()
        click = self.mouse_events.GetEventById('click1')
        press = self.mouse_events.GetEventById('press1')
        
        self.close_rect = [self.pos[0]+self.size[0]-20,self.pos[1]]
        self.sizing_rect = [self.pos[0]+self.size[0]-20,self.pos[1]+self.size[1]-20]
        self.closed_vabor = False
        if in_rect(self.close_rect, [20,20], Mouse.pos):
            self.closed_vabor = True
            
            if click:
                self.opened = False
                
        self.cl = False
        if in_rect(self.pos, [self.size[0],20], Mouse.pos) and press:
            self.cl = True
        
        if in_rect(self.pos, [self.size[0],20], Mouse.pos) and click:
            self.pressed = True
        if not press:
            self.pressed = False
            
        self.pos[0] = min(max(self.pos[0],0), win.get_size()[0]-self.size[0])
        self.pos[1] = min(max(self.pos[1],0), win.get_size()[1]-self.size[1])
        self.size[0] = max(self.size[0],self.start_size[0])
        self.size[1] = max(self.size[1],self.start_size[1])
        
        if self.opened:
            
            if self.pressed:
                
                self.pos[0]+=ms[0]
                self.pos[1]+=ms[1]
        
            if in_rect(self.sizing_rect, [20,20], Mouse.pos):
                
                if click:
                    self.sizing_pressed = True
            if not press:
                self.sizing_pressed = False
            
            if self.sizing_pressed:
                self.size[0]+=ms[0]
                self.size[1]+=ms[1]

class TextInput:
    def __init__(self, size) -> None:
        self.size = size
        self.text = ''

        self.bg_color = [180,180,180]
        self.pos = [0,0]
        self.vabor = False
        self.mouse_events = MouseEventHandler()
        self.mouse_events.AddEvent(Mouse(Mouse.left, Mouse.click_event, 'click'))
        
        self.view_text = Text('arial',20, '','white',True)
        self.end_press = None
        self.timer = 0
        
    def update(self):
        if self.vabor:
            inp = win.press_key
            
            if inp is not None:
                if inp == 'backspace':
                    self.text = self.text[:-1]
                elif inp == 'left shift':
                    self.end_press = inp
                elif inp == 'left ctrl':
                    self.end_press = inp
                else:
                    if self.end_press == 'left shift' and inp=='=':
                        
                        inp = '+' 
                    elif self.end_press == 'left shift' and inp=='9':
                        
                        inp = '(' 
                    elif self.end_press == 'left shift' and inp=='0':
                        
                        inp = ')' 
                        
                    elif self.end_press == 'left shift':
                        inp = inp.upper()
                    if self.end_press == 'left ctrl' and inp == 'v':
                        self.text = paste()
                    else:
                    
                    
                        self.text+=inp
                    self.end_press = None
                
        self.timer+=0.1
        self.mouse_events.EventsUpdate()
        
        
        if self.mouse_events.GetEventById('click'):
            if in_rect(self.pos, self.size, Mouse.pos):
                self.vabor = not self.vabor
            else:
                self.vabor = False
        
        
    def render(self, surf):
        Draw.draw_rect(surf, self.pos, self.size, self.bg_color, radius = 5)
        if self.vabor:
            Draw.draw_rect(surf, self.pos, self.size, (200,250,250),1,radius=5 )
        text_surf = self.view_text.render(self.text, 'white', self.size[0]-5)
        surf.blit(text_surf, [self.pos[0]+5,self.pos[1]])
        if self.vabor:
            d = abs(12*sin(self.timer))
            Draw.draw_vline(surf, self.pos[0]+text_surf.get_width()+7, self.pos[1]+d, self.pos[1]+24-d,2, (200,250,250))

class DownTable:
    def __init__(self) -> None:
        self.pos = [0, 0]
        self.buttons_count = 6
        self.buttons_size = 60
        self.btns_scale = 2.5
        
        self.btn_tiles = Button(datas['tiles_btn'],self.btns_scale)
        self.tbl_tiles = Table([230,500],[200,200],'Tiles')
        self.tbl_tiles_load_btn = TextButton('load', 20, [150,25])
        self.tbl_tiles_load_tb = TextInput([335,25])
        self.tile_name_text = Text('arial',16, '', 'white',True)
        self.loaded_tilesheats = []
        self.my_tile_sheats = []
        
    def update(self, win_size, win_center):
        self.size = [self.buttons_size*self.buttons_count, self.buttons_size]
        self.pos = [
            win_center[0]-self.size[0]/2,
            win_center[1]+win_size[1]/2-self.buttons_size-20
        ]
        
        self.btn_tiles.update(pos=[self.pos[0]+5,self.pos[1]+5])
        self.tbl_tiles.update()
        self.tbl_tiles_load_tb.update()
        self.tbl_tiles_load_btn.update()
        
    
    
    def load_tile_sheats(self):
        tsh = DataLoader().Load_from_file_tilesheats(self.tbl_tiles_load_tb.text)
        self.loaded_tilesheats = []
        self.my_tile_sheats = []
        for tile_sheat_name in tsh:
            tlsh1 = copy(tsh[tile_sheat_name])
            tlsh2 = copy(tsh[tile_sheat_name])
            
            tiles_scale(tlsh1, 5)
            
            self.loaded_tilesheats.append([tile_sheat_name, tlsh1])
            self.my_tile_sheats.append([tile_sheat_name, tlsh2])
            
    def render_loaded_tile_sheats(self, pos, size, surf):
        position = copy([pos[0]+10,pos[1]+30])
        for i, tile_sheat in enumerate(self.loaded_tilesheats):
            
            Draw.draw_rect(surf, position, [70,70], (90,90,90),radius=5)
            if in_rect(position,[70,70],Mouse.pos):
                Draw.draw_rect(surf, position, [70,70], (255,255,255),1,radius=5)
            
            tile_sheat[1].tiles['one'].center = [position[0]+35, position[1]+35]
            tile_sheat[1].tiles['one'].center = [position[0]+35, position[1]+35]
            tile_sheat[1].tiles['one'].render(surf)
            self.tile_name_text.draw(surf, [position[0]+35, position[1]+35+35-7], True, tile_sheat[0],'white')
            
            position[0]+=70
            
            if (position[0]+70-10)>(self.tbl_tiles.pos[0]+self.tbl_tiles.size[0]-20):
                position[1]+=70
                position[0] = pos[0]+10
            
            
    
    def render_tbl_tiles(self, pos, size, surf):
        self.tbl_tiles_load_btn.pos = [pos[0]+size[0]-self.tbl_tiles_load_btn.size[0]-5, pos[1]+size[1]-self.tbl_tiles_load_btn.size[1]-5]
        self.tbl_tiles_load_tb.pos = [pos[0]+5, pos[1]+size[1]-self.tbl_tiles_load_btn.size[1]-5]
        self.tbl_tiles_load_tb.size[0] = size[0]-10-150-5
        
        Draw.draw_rect(surf, [pos[0]+5,pos[1]+25],[size[0]-10,size[1]-60],(130,130,130),radius=5)
        
        self.tbl_tiles_load_btn.render(surf)
        self.tbl_tiles_load_tb.render(surf)
        self.render_loaded_tile_sheats(pos, size, surf)
        
        if self.tbl_tiles_load_btn.click:
            self.load_tile_sheats()
    
    def render(self, win_surf_, win_size, win_center):
        self.update(win_size, win_center)
        
        
        
        self.tbl_tiles.render(render_event=self.render_tbl_tiles,surf=win_surf_)
        
        Draw.draw_rect(win_surf_, self.pos, self.size, (200,200,200), radius=10)
        
        self.btn_tiles.render(win_surf_)
        if self.btn_tiles.click:
            self.tbl_tiles.opened = True
            

dt = DownTable()

while win(fps=60,base_color=(220,220,220)):
    win_size = get_win_size()
    win_center = get_win_center()
    dt.render(win.surf, win_size, win_center)
    
    