from api.lib import *
from api.libvfx import *


import pygame.system


win = Window([1600,950], 'Tanks Blitz')






GLOBAL_PARTICLE_SIMULATE_SPACE = ParticleSpace([0,0],[1600,950], win, 1)
GLOBAL_PARTICLE_SPAWNER = ParticleSpawner()
GLOBAL_KILL_PARTICLE = Particle()
GLOBAL_KILL_PARTICLE.COLOR_FROM_DICT = [
    Color.rgba(255,200,150).rgb,
    Color.rgba(200,150,100).rgb,
    Color.rgba(200,100,100).rgb
]
GLOBAL_KILL_PARTICLE.SPEED = Vector2(0,2)
GLOBAL_KILL_PARTICLE.SPEED_DURATION = 180
GLOBAL_KILL_PARTICLE.SHAPE = particle_shapes.CIRCLE
GLOBAL_KILL_PARTICLE.RADIUS = 15
GLOBAL_KILL_PARTICLE.RADIUS_RANDOMER = 20
GLOBAL_KILL_PARTICLE.RADIUS_RESIZE = -0.6
GLOBAL_KILL_PARTICLE.RESIZE_START_TIME = 30
GLOBAL_KILL_PARTICLE.SPEED_FRICTION = 0.9
GLOBAL_KILL_PARTICLE.SPEED_RANDOMER = 8

GLOBAL_KILLED_PARTICLE = Particle()
GLOBAL_KILLED_PARTICLE.COLOR_FROM_DICT = [
    Color.rgba(100,100,100).rgb,
    Color.rgba(150,150,150).rgb,
    Color.rgba(220,220,220).rgb
]
GLOBAL_KILLED_PARTICLE.SPEED = Vector2(0,1)
GLOBAL_KILLED_PARTICLE.SPEED_DURATION = 18
GLOBAL_KILLED_PARTICLE.SPEED_ANGLE = -90
GLOBAL_KILLED_PARTICLE.SHAPE = particle_shapes.CIRCLE
GLOBAL_KILLED_PARTICLE.RADIUS = 5
GLOBAL_KILLED_PARTICLE.RADIUS_RANDOMER = 4
GLOBAL_KILLED_PARTICLE.RADIUS_RESIZE = -0.6
GLOBAL_KILLED_PARTICLE.RESIZE_START_TIME = 30
GLOBAL_KILLED_PARTICLE.SPEED_FRICTION = 0.99
GLOBAL_KILLED_PARTICLE.SPEED_RANDOMER = 2



GLOBAL_DAMAGE_PARTICLE = Particle()
GLOBAL_DAMAGE_PARTICLE.COLOR_FROM_DICT = [
    Color.rgba(255,200,150).rgb,
    Color.rgba(200,150,100).rgb,
    Color.rgba(200,100,100).rgb
]
GLOBAL_DAMAGE_PARTICLE.SPEED = Vector2(0,1)
GLOBAL_DAMAGE_PARTICLE.SPEED_DURATION = 20
GLOBAL_DAMAGE_PARTICLE.SHAPE = particle_shapes.CIRCLE
GLOBAL_DAMAGE_PARTICLE.RADIUS = 5
GLOBAL_DAMAGE_PARTICLE.RADIUS_RANDOMER = 4
GLOBAL_DAMAGE_PARTICLE.RADIUS_RESIZE = -0.6
GLOBAL_DAMAGE_PARTICLE.RESIZE_START_TIME = 15
GLOBAL_DAMAGE_PARTICLE.SPEED_FRICTION = 0.9
GLOBAL_DAMAGE_PARTICLE.SPEED_RANDOMER = 6







Mouse.set_hide()
class BulletSpace:
    def __init__(self) -> None:
        self.bullets = []
    
    def add(self, bullet):
        self.bullets.append(bullet)
        
    def render(self, win):
        for bullet in self.bullets:
            Draw.draw_rc_rect(win.surf, bullet['pos'], [15,6], 270-bullet['speed'].get_angle(), Color.rgba(255,200,150))
            
    def update(self, tanks_space):
        for i, bullet in enumerate( self.bullets ):
            bullet['pos'][0]+=bullet['speed'].x
            bullet['pos'][1]+=bullet['speed'].y
            
            for tank in tanks_space.tanks:
                if distance(tank.pos, bullet['pos'])<tank.collide_radius and not tank.killed:
                    if tank.id!=bullet['id']:
                        GLOBAL_DAMAGE_PARTICLE.COLOR_FROM_DICT = GLOBAL_DAMAGE_PARTICLE.COLOR_FROM_DICT = [
                            Color.rgba(255,200,150).rgb,
                            Color.rgba(200,150,100).rgb,
                            Color.rgba(200,100,100).rgb,
                            tank.color
                        ]
                        GLOBAL_DAMAGE_PARTICLE.SPEED_ANGLE = 270-bullet['speed'].get_angle()
                        GLOBAL_PARTICLE_SPAWNER._pos = bullet['pos']
                        GLOBAL_PARTICLE_SPAWNER._type = particle_spawner_types.RECT
                        GLOBAL_PARTICLE_SIMULATE_SPACE.add(GLOBAL_DAMAGE_PARTICLE, GLOBAL_PARTICLE_SPAWNER, int(bullet['speed'].lenght))
                        tank.hp-=bullet['damage']
                        del self.bullets[i]
                        break
                
class TanksSpace:
    def __init__(self) -> None:
        self.tanks = []
        
    def add(self, tanks):
        self.tanks.append(tanks)
        
    def update(self):
        GLOBAL_PARTICLE_SIMULATE_SPACE.tick()
        for tank1 in self.tanks:
            if tank1.hp<=0 and not tank1.killed:
                GLOBAL_PARTICLE_SPAWNER._type = particle_spawner_types.RECT
                GLOBAL_PARTICLE_SPAWNER._pos = tank1.pos
                GLOBAL_PARTICLE_SIMULATE_SPACE.add(GLOBAL_KILL_PARTICLE, GLOBAL_PARTICLE_SPAWNER, 20,1)
                tank1.killed = True
                
            if tank1.killed:
                GLOBAL_PARTICLE_SPAWNER._type = particle_spawner_types.CIRCLE
                GLOBAL_PARTICLE_SPAWNER._radius = tank1.collide_radius
                GLOBAL_PARTICLE_SPAWNER._pos = tank1.pos
                GLOBAL_PARTICLE_SIMULATE_SPACE.add(GLOBAL_KILLED_PARTICLE, GLOBAL_PARTICLE_SPAWNER, 1,10)
            
            
            for tank2 in self.tanks:
                if tank1.id!=tank2.id:
                    if not tank1.killed:
                        if distance(tank2.pos, tank1.pos)<tank1.collide_radius+tank2.collide_radius:
                            normal_vector = Vector2.Normal(tank2.pos, tank1.pos)
                            normal_vector.normalyze()
                            normal_vector*=((tank1.collide_radius+tank2.collide_radius)-distance(tank2.pos, tank1.pos))
        

                            tank2.pos[0]+=(normal_vector.x/2)
                            tank2.pos[1]+=(normal_vector.y/2)
                            tank2.s.x = -normal_vector.x
                            tank2.s.y = -normal_vector.y
                            
                            
                    else:
                        if distance(tank2.pos, tank1.pos)<tank1.collide_radius+tank2.collide_radius:
                            normal_vector = Vector2.Normal(tank2.pos, tank1.pos)
                            normal_vector.normalyze()
                            normal_vector*=((tank1.collide_radius+tank2.collide_radius)-distance(tank2.pos, tank1.pos))
        

                            
                            
                            
                        
                        
                        


class MapSpace:
    def __init__(self) -> None:
        self.space = []
        
    def add_rect(self, rect):
        self.space.append(rect)
        
    def render_map(self,win):
        for rect in self.space:
            Draw.draw_rect(win.surf, rect.xy, rect.wh,'white')


class T_Body:
    def __init__(self, pos, size, color, mass, speed, rotate_speed, gun:'T_Gun', gun_dx = 0, dummy=False, hp=1000, view_radius: int = 300) -> None:
        self.size = size
        self.color = color
        self.mass = mass
        self.speed = Vector2(0,speed)
        self.pos = pos
        self.angle = 0
        self.rotate_speed = rotate_speed
        self.s = Vector2(0,0)
        self.speed_angle = self.angle
        self.gun = gun
        self.gun_dx = gun_dx
        self.id = random.randint(0,9999999999)
        self.gun.id = self.id
        
        self.killed = False
        
        self.hp = hp
        self.start_hp = copy(self.hp)
        
        self.space = ParticleSpace([0,0],[1500,950], win, 1)
        self.spavner = ParticleSpawner(pos_=[0,0], size_=[1,1])
        
        self.pl_particle = Particle()
        self.pl_particle.SHAPE = particle_shapes.CIRCLE
        self.pl_particle.RADIUS = 5
        self.pl_particle.RADIUS_RANDOMER = 3
        self.pl_particle.SIZE_RESIZE = 0.02
       
        self.pl_particle.COLOR_FROM_DICT = [[190,190,190],[200,200,200],[150,150,150]]
        
        
        self.dummy = dummy
        if self.dummy:
            self.gun_angle = random.randint(0,360)
            
        self.collide_radius = self.size[1]
        
        self.kill_color = Color.rgba(*self.color.rgb).chb
        
        
        self.view_radius = view_radius
        self.viev_radius_duration = 40
        self.viev_angle_duration = 5
        self.view_polygone = []
        
        
    def render(self, win):
        if len(self.view_polygone)>2:
            Draw.draw_polygone(win.surf, self.view_polygone, 'red', 3)
        self.space.render()
        self.space.update(lambda x,y:...)
        
        if self.killed:
            color = self.kill_color
        else:
            color = self.color
        Draw.draw_rc_rect(win.surf, self.pos, [self.size[0]-10,self.size[1]+8], self.angle, [100,100,100])
        Draw.draw_rc_rect(win.surf, self.pos, self.size, self.angle, color)
        
        self.gun.render(win)
    
    def render_hp(self,win):
        hp_line_width = 100
        hp_draw_pos = [self.pos[0]-hp_line_width/2,self.pos[1]+50]
        Draw.draw_hline(win.surf, hp_draw_pos[1], hp_draw_pos[0], hp_draw_pos[0]+hp_line_width, 5,(200,200,200))
        Draw.draw_hline(win.surf, hp_draw_pos[1], hp_draw_pos[0], hp_draw_pos[0]+hp_line_width*self.hp/self.start_hp, 5,(200,100,100))
    
    def render_ui(self):
        if not self.dummy:
            self.gun.render_ui(win)
        
        if not self.killed:
            self.render_hp(win)
            
    def view_polygone_update(self, map):
        
                
        
        
        
        
        self.view_polygone = []
        count = 360//self.viev_angle_duration
        step = self.view_radius//self.viev_radius_duration
        center = copy(self.pos)
        
        normal_vector = Vector2(0,10)
        normal_vector.normalyze()
        for i in range(count):
            normal_vector.rotate(self.viev_angle_duration)
            
            
            for a in range(step):
                breked = False
                normal_vector.normalyze()
                if a!=0:
                    normal_vector*=a*self.viev_radius_duration
                    
                    p = [center[0]+normal_vector.x,center[1]+normal_vector.y]
                    for rect in map:
                        if in_rect(rect.xy, rect.wh, p):
                            breked = True
                            breked
                    if breked:
                        break
            self.view_polygone.append(p)
        
        
                
        
        
    def update(self, bullet_space, map_space):
        self.view_polygone_update(map_space.space)
        if self.killed:
            self.gun.killed = True
        
        if not self.dummy:
            self.gun.update()
            
                
            if Keyboard.key_pressed('up'):
                self.s = copy(self.speed)
                self.speed_angle = self.angle
                
                normal = Vector2.Normal(self.pos, [self.pos[0]+self.s.y,self.pos[1]+self.s.x])
                normal.normalyze()
                normal*=self.size[1]/2
                normal.set_angle(self.angle)
                
                n2 = copy(normal)
                n2.rotate(90)
                n2.normalyze()
                n2*=self.size[0]/2-18
                
                self.pl_particle.SPEED_ANGLE = self.angle-180
                self.pl_particle.SPEED = Vector2(0,-0.6)
                self.pl_particle.SPEED_FRICTION = 0.98
                self.pl_particle.SPEED_DURATION = 60
                
            
                self.spavner._pos = [self.pos[0]-normal.x+n2.x, self.pos[1]-normal.y+n2.y]
                self.space.add(self.pl_particle, self.spavner, 1,5)
                    
                self.spavner._pos = [self.pos[0]-normal.x-n2.x, self.pos[1]-normal.y-n2.y]
                self.space.add(self.pl_particle, self.spavner, 1,5)
                    
            if Keyboard.key_pressed('down'):
                self.s = copy(self.speed)*0.5
                self.speed_angle = self.angle-180
            
            if Keyboard.key_pressed('left'):
                self.angle-=self.rotate_speed
                self.gun.rasbros+=self.rotate_speed/10
                self.s*=0.8
                self.gun.angle-=self.rotate_speed
                
            if Keyboard.key_pressed('right'):
                self.angle+=self.rotate_speed
                self.gun.rasbros+=self.rotate_speed/10
                self.s*=0.8
                self.gun.angle+=self.rotate_speed

            self.s*=1-1/self.mass
            self.gun.rasbros+=self.s.lenght/self.mass
            self.s.set_angle(self.speed_angle)
            

            
            self.gun.gunned(bullet_space)
        else:
            self.gun.angle = self.gun_angle
            self.s*=1/self.mass
        
        self.collide_rects = []
        self.pos[1]+=self.s.y
            
        for rect in map_space.space:
                if rect.collide_rect(Rect(self.pos[0]-self.collide_radius,self.pos[1]-self.collide_radius,self.collide_radius*2,self.collide_radius*2)):
                    self.collide_rects.append(rect)
            
        for c_rect in self.collide_rects:          
                if self.s.y>0:
                    self.pos[1]=c_rect.y_up-self.collide_radius
                    
                elif self.s.y<0:
                    self.pos[1]=c_rect.y_down+self.collide_radius
                self.s.y = 0
                
            
            
            
        self.collide_rects = []
        self.pos[0]+=self.s.x       
                
        for rect in map_space.space:
                if rect.collide_rect(Rect(self.pos[0]-self.collide_radius,self.pos[1]-self.collide_radius,self.collide_radius*2,self.collide_radius*2)):
                    self.collide_rects.append(rect)
            
        for c_rect in self.collide_rects:          
                if self.s.x>0:
                    self.pos[0]=c_rect.x_left-self.collide_radius
                elif self.s.x<0:
                    self.pos[0]=c_rect.x_right+self.collide_radius
                self.s.x = 0
                
        
        
        gun_dx_znak = sign(self.gun_dx)
        gun_dx_vector = Vector2(0,self.gun_dx)
        gun_dx_vector.set_angle(self.angle)
        gun_dx_vector*=gun_dx_znak
            
        self.gun.pos = [self.pos[0]+gun_dx_vector.x,self.pos[1]+gun_dx_vector.y]
        
class T_Gun:
    def __init__(self, uron, snaryd_count, vp, rotate_speed, lenght,
                 color, width, size, min_rasbros, max_rasbros,rasbros_min_speed,
                 bullet_speed = 20, strelba_kd=60, type='dozar') -> None:
        self.uron = uron
        self.bullet_speed = bullet_speed
        self.stralba_kd = strelba_kd
        self.strelba_kd_time = 1
        self.gotov_strelyt = False
        
        
        self.type = type
        self.vp = vp
        self.snaryd_count = snaryd_count
        self.sarajen_count = 0
        
        self.time = 0
        self.pos = [0,0]
        self.lenght = lenght
        self.width = width
        self.size = size
        
        self.id = None
        
        self.color = color
        
        self.angle = 0
        self.rotate_speed = rotate_speed
        self.mouse_angle = 0
        self.rasbros = 0
        
        self.min_rasbros = min_rasbros
        self.max_rasbros = max_rasbros
        self.rasbros_min_speed = rasbros_min_speed
        
        self.space = ParticleSpace([0,0],[1500,950], win, 1)
        self.spavner = ParticleSpawner(pos_=[0,0], size_=[1,1])
        self.killed = False
        
        self.kd_zakonch = False
        
        # PARTICLES ---------------------------------------------------------------------------------------------------------------
        self.pl_particle = Particle()
        self.pl_particle.SHAPE = particle_shapes.CIRCLE
        self.pl_particle.RESIZE_START_TIME = 1
        self.pl_particle.RADIUS = 2
        self.pl_particle.RADIUS_RANDOMER = 5
        self.pl_particle.SIZE_RESIZE = 0.01
    
        self.pl_particle.COLOR_FROM_DICT = [Color.rgba(255,200,150).rgb,Color.rgba(200,150,100).rgb,Color.rgba(200,100,100).rgb]
        # PARTICLES ---------------------------------------------------------------------------------------------------------------
        
        self.kd_time_text = Text('arial',17, '',self.color.rgb,True)
        
        
        self.udar_speed = Vector2(0,0)
        self.udar_umenhs = 0.9
        
        self.kill_color = Color.rgba(*self.color.rgb).chb
        
    def update(self):
        self.mouse_angle = angle_to_float(self.pos, Mouse.position())
        snak = sign(360-self.mouse_angle-self.angle-90-180)
        rs = snak*min(self.rotate_speed,abs(360-self.mouse_angle-self.angle-90-180))
        self.angle += rs
        
        self.rasbros+=abs(rs)
        self.rasbros-=self.rasbros_min_speed
        self.rasbros = min(max(self.min_rasbros,self.rasbros), self.max_rasbros)
        
        self.perezaradka()
    
    def perezaradka(self):
        self.time+=1
        if self.type == 'dozar':
            if self.sarajen_count<self.snaryd_count:
                if self.time%self.vp==0:
                    self.sarajen_count+=1
                    self.time = 1

            else:
                self.time = self.vp
                
        if self.type == 'baraban':
            if not self.gotov_strelyt:
                if self.time%self.vp==0:

                    if self.sarajen_count!=self.snaryd_count:
                        self.sarajen_count+=1
                        self.time = 1
                    else:
                        self.gotov_strelyt = True
            else:
                self.time = self.vp
                
                
                
            
    def render_snarayds(self, win):
        vector = Vector2(0,self.max_rasbros+25)
        mp = Mouse.position()
        vector.rotate(5)
        for i in range(self.sarajen_count):
            Draw.draw_circle(win.surf, [mp[0]+vector.x,mp[1]+vector.y], 7, Color.rgba(100,250,100), 0)
            vector.rotate(10)
        
        vector = Vector2(0,self.max_rasbros+25)
        mp = Mouse.position()
        vector.rotate(5)
        for i in range(self.snaryd_count):
            Draw.draw_circle(win.surf, [mp[0]+vector.x,mp[1]+vector.y], 7, self.color, 2)
            vector.rotate(10)
            
    def render(self, win):
        self.udar_speed.set_angle(self.angle)
        self.udar_speed*=self.udar_umenhs
        pos = [self.pos[0]-self.udar_speed.x,self.pos[1]-self.udar_speed.y]
        
        if self.killed:
            color = self.kill_color
        else:
            color = self.color
        
        Draw.draw_rc_rect(win.surf, pos, self.size, self.angle, color)
        Draw.draw_rp_line(win.surf, pos, self.lenght, self.angle, color, self.width, False)
        self.space.render()
        self.space.update(lambda x,y: ...)
        
    def gun_napr_render(self ,win):
        vector = Vector2(100,0)
        vector.set_angle(self.angle)
        vector.normalyze()
        vec1 = copy(vector)
        vec2 = copy(vector)
        
        vec3 = copy(vector)
        vec4 = copy(vector)
        
        lenght = distance(self.pos, Mouse.position())
        
        vec1*=lenght-self.max_rasbros
        vec2*=lenght+self.max_rasbros
        
        vec3*=lenght-self.rasbros
        vec4*=lenght+self.rasbros

        Draw.draw_line(win.surf, [self.pos[0]+vec1.x,self.pos[1]+vec1.y], [self.pos[0]+vec2.x,self.pos[1]+vec2.y], self.color, 2)
        Draw.draw_line(win.surf, [self.pos[0]+vec3.x,self.pos[1]+vec3.y], [self.pos[0]+vec4.x,self.pos[1]+vec4.y], Color.rgba(255,100,100).rgb, 2)
        
    def render_ui(self, win):
        Draw.draw_circle(win.surf, Mouse.position(), self.rasbros, Color.rgba(255,100,100), 2)
        
        Draw.draw_arc(win.surf, Mouse.position(), self.color, 0, 360*self.time/self.vp, self.max_rasbros+15, 10,40)
        Draw.draw_arc(win.surf, Mouse.position(), Color.rgba(200,200,200), 0, 360*self.strelba_kd_time/self.stralba_kd, self.max_rasbros, 5,40)
        if self.sarajen_count!=self.snaryd_count:
            self.kd_time_text.draw(win.surf, [Mouse.position()[0]+5,Mouse.position()[1]+self.max_rasbros+15], False, f'{int((self.time%self.vp/self.vp)*100)}%',self.color.rgb)
        
        self.gun_napr_render(win)
        self.render_snarayds(win)
        
    def construct_bullet(self):
        vector = Vector2(100,0)
        vector.set_angle(self.angle)
        vector.normalyze()
        
        speed = copy(vector)

        vector*=self.lenght
        spavn_pos = [self.pos[0]+vector.x,self.pos[1]+vector.y]
        speed*=self.bullet_speed
        
        
        
        dop_angle = random.randint(0, 
                                   int(
                                       math.degrees( 
                                                    math.atan(
                                                        self.rasbros/distance(spavn_pos, Mouse.position())
                                                        )
                                                    )
                                       
                                       )
                                   
                                   )*random.randint(-1000,1000)/1000
        
        
        
        speed.rotate(dop_angle)
        bullet = {
            'pos':spavn_pos,
            'speed':speed,
            'id':self.id,
            'damage':self.uron
        }
        return bullet
        
    def gunned(self, bulletspace):
        if self.type == 'baraban':
            if self.snaryd_count == self.sarajen_count:
                self.gotov_strelyt = True
            if self.sarajen_count == 0:
                self.gotov_strelyt = False
                
            if not self.kd_zakonch:
                self.strelba_kd_time+=1
                if self.strelba_kd_time%self.stralba_kd==0:
                    self.kd_zakonch = True
                    self.strelba_kd_time = 1
            else:
                self.strelba_kd_time = self.stralba_kd
                
            if Mouse.click() and self.gotov_strelyt and self.kd_zakonch:
                    self.udar_speed = Vector2(15,0)
                    p = self.construct_bullet()
                    self.spavner._pos = p['pos']
                    self.pl_particle.SPEED = Vector2(0,0.1)
                    self.pl_particle.SPEED_DURATION = 15
                    self.pl_particle.SPEED_ANGLE = 270-p['speed'].get_angle()+180
                    self.pl_particle.SPEED_RANDOMER = 1
                    self.space.add(self.pl_particle, self.spavner, 20,1)
                    bulletspace.add(p)
                    self.sarajen_count-=1
                    self.kd_zakonch = False
                    
        
        if self.type == 'dozar':
            if not self.gotov_strelyt:
                self.strelba_kd_time+=1
                if self.strelba_kd_time%self.stralba_kd==0:
                    self.gotov_strelyt = True
                    self.strelba_kd_time = 1
            else:
                self.strelba_kd_time = self.stralba_kd
            
        
        
        
            if self.sarajen_count!=0:
                if Mouse.press() and self.gotov_strelyt:
                    self.udar_speed = Vector2(15,0)
                    p = self.construct_bullet()
                    self.spavner._pos = p['pos']
                    self.pl_particle.SPEED = Vector2(0,0.1)
                    self.pl_particle.SPEED_DURATION = 15
                    self.pl_particle.SPEED_ANGLE = 270-p['speed'].get_angle()+180
                    self.pl_particle.SPEED_RANDOMER = 1
                    self.space.add(self.pl_particle, self.spavner, 20,1)
                    bulletspace.add(p)
                    self.sarajen_count-=1
                    self.gotov_strelyt = False
                
        
    
AMX1358_g = T_Gun(90,7, 10, 7, 55, Color.rgba(160,160,200),5,[30,20],20,70,1,type='baraban')
AMX1358_b = T_Body([400,400],[60,30],Color.rgba(190,190,210), 10, 6, 1.5, AMX1358_g,-15,view_radius=500)

AMX1358_g_2 = T_Gun(90,7, 10, 7, 55, Color.rgba(160,160,200),5,[30,20],20,70,1,type='baraban')
AMX1358_b_2 = T_Body([900,400],[60,30],Color.rgba(190,190,210), 10, 6, 1.5, AMX1358_g_2,-15,view_radius=500,dummy=True,)


KV2_g = T_Gun(600,1, 1000, 0.2, 40, Color.rgba(140,60,120),8,[40,25],35,130,0.1,9,10)
KV2_b = T_Body([600,400],[80,36],Color.rgba(160,80,140), 60, 1, 0.2, KV2_g, gun_dx=8,dummy=True,)



b_space = BulletSpace()
t_space = TanksSpace()
m_space = MapSpace()
m_space.add_rect(Rect(400,600,300,100))
m_space.add_rect(Rect(700,100,100,400))


t_space.add(KV2_b)
t_space.add(AMX1358_b)
t_space.add(AMX1358_b_2)


while win(base_color=(180,240,180), fps=60):
    t_space.update()
    b_space.render(win)
    
    AMX1358_b.render(win)
    AMX1358_b.update(b_space, m_space)
    
    AMX1358_b_2.render(win)
    AMX1358_b_2.update(b_space, m_space)
    
    KV2_b.render(win)
    KV2_b.update(b_space, m_space)
    
    AMX1358_b.render_ui()
    AMX1358_b_2.render_ui()
    KV2_b.render_ui()
    
    
    
    b_space.update(t_space)
    
    m_space.render_map(win)
    
    GLOBAL_PARTICLE_SIMULATE_SPACE.render()
    GLOBAL_PARTICLE_SIMULATE_SPACE.update(lambda x, y: ...)
