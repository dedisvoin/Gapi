from typing import Dict, Tuple
import pygame

try:
    from .lib import *
except:
    from lib import *

class particle_shapes:
    CIRCLE = 'CIRCLE_SHAPE'
    RECT = "RECT_SHAPE"
    IMAGE = "IMAGE_SHAPE"
    BLEND_CIRCLE = 'BLEND_CIRCLE_SHAPE'

class particle_spawner_types:
    RECT = "RECT_SPAWNER"
    CIRCLE = 'CIRCLE_SPAWNER'
    LINE = 'LINE_SPAWNER'
    POLYGONE = "POLYGONE_SPAWNER"
    
class sprite_angle_types:
    TO_VECTOR = 'TO_VECTOR'
    TO_ROTATE = 'TO_ROTATE'
    
class light_modes:
    ADD = pygame.BLEND_ADD
    RGB_MIN = pygame.BLEND_RGB_MIN
    RGB_MAX = pygame.BLEND_RGB_MAX


class _particle:
    def __init__(self) -> None:
        
        # All particle propertis -----------------------------------------
        
        self.RESIZE_START_TIME: int = 0
        self.SHAPE: particle_shapes = particle_shapes.CIRCLE
        self.COLOR_FROM_DICT: Tuple[list | str, ...] = []
        self.COLOR_RANDOM: bool = False
        self.COLOR: Color | Tuple[float, float, float] | str = 'gray'
        self.POS: Tuple[float, float] = [0,0]
        self.TIMER: float = 0
        self.SHAPE_RENDERER: bool = True
        
        # All particle propertis -----------------------------------------
        
        # Images ---------------------------------------------------------
        
        self.SPRITE: Sprite = None
        self.SPRITE_LIST: Tuple[Sprite, ...] = []
        self.SPRITE_START_SCALE: float = 1
        self.SPRITE_SCALE_RESIZE: float = -0.01
        self.SPRITE_ANGLE_TYPE: sprite_angle_types = sprite_angle_types.TO_ROTATE
        self.SPRITE_ROTATE_ANGLE: float = 0.1
        self.SPRITE_START_ANGLE: float = 0
        self.SPRITE_ADD_ANGLE: float = 0
        self.SPRITE_SCALE_RANDOMER: int = 0

        # Images ---------------------------------------------------------
        
        # Lines ----------------------------------------------------------
        
        self.LINES: bool = False
        self.LINES_COLOR: Color | Tuple[float, float, float] | str = [100,100,100]
        self.LINES_COLOR_FROM_PARTICLE_COLOR: bool = True
        
        # Lines ----------------------------------------------------------
        
        # Shadows --------------------------------------------------------
        
        self.SHADOW_COLOR: Color | Tuple[float, float, float] | str = (0,0,0)
        self.SHADOWING: bool = False
        self.SHADOW_DX: float = 5
        self.SHADOW_DY: float = 5
        
        # Shadows --------------------------------------------------------
        
        # Light propertis ------------------------------------------------
        
        self.LIGHTNING: bool = False
        self.LIGHT_SHAPE: particle_shapes = particle_shapes.CIRCLE
        self.LIGHT_COLOR: Color | Tuple[float, float, float] | str = [255,0,0]
        self.LIGHT_STRANGE: float = 1
        self.LIGHT_STRANGE_BY_SIZE: bool = True
        self.LIGHT_COLOR_FROM_PARTICLE_COLOR: bool = True
        self.LIGHT_MODE:light_modes = light_modes.ADD
        self.LIGHT_SIZE: float = 20
        self.BLEND_LIGHT_CIRCLES = 10
        self.BLEND_LIGHT_SURF = None
        
        # Light propertis ------------------------------------------------
        
        # Speed propertis ------------------------------------------------
        
        self.SPEED_RANDOM_ROTATION_ANGLE: Tuple[int ,int] = False
        self.SPEED_ROTATION_ANGLE: float = 0
        self.SPEED_ROTATION: bool = 0
        self.SPEED_DURATION: int = 0
        self.SPEED_FRICTION: float = 1
        self.SPEED_ANGLE: int = 0
        self.SPEED: Vector2 = Vector2(0,0)
        self.SPEED_RANDOMER: float = 0
        self.GRAVITY_VECTOR: Tuple[float, float] = [0,0]

        # Speed propertis ------------------------------------------------
        
        # Circle particle propertis --------------------------------------
        
        self.RADIUS_RANDOMER: float = 0
        self.RADIUS_RESIZE: float = -0.2
        self.RADIUS: float = 10
        self.START_RADIUS: float = 10
        
        # Circle particle propertis --------------------------------------
        
        # Rect particle propertis ----------------------------------------
        
        self.SIZE_RESIZE: Tuple[float, float] = [-0.2, -0.2]
        self.SIZE_RANDOMER: Tuple[int, int] = [20,20]
        self.SIZE: Tuple[float, float] = [10,10]
        self.START_SIZE: Tuple[float, float] = [10,10]
        
        # Rect particle propertis --------------------------------------
        
    def set(self, arg_name: str, value_: any):
        arg_name = arg_name.upper()
        if arg_name in self.__dict__.keys():
            self.__dict__[arg_name] = value_
        else:
            print(f'Do not found {arg_name}!')
            
    def set_all(self, args: Dict):
        for name in args:
            self.set(name, args[name])
        
    def __str__(self) -> str:
        return str(self.__dict__)
    
class Particle(_particle):
    def __init__(self) -> None:
        super().__init__()
    
    def __str__(self) -> str:
        return super().__str__()
    
    def init(self):
        ...
    
class ParticleSpawner:
    def __init__(self, 
                type_: particle_spawner_types = particle_spawner_types.RECT, 
                pos_: tuple[int,int] = [0,0], size_: Tuple[int,int] = [0,0],
                radius_: int = 0,
                pos1_: Tuple[int,int] = [0,0], pos2_: Tuple[int,int] = [0,0], 
                points_ : Tuple[Tuple[float,float], ...] = [] ) -> None:
        
        self._type = type_
        
        self._pos = pos_
        self._size = size_
        self._radius = radius_
        
        self._pos1 = pos1_
        self._pos2 = pos2_
        
        self._points = points_
        
class ParticleSpace:
    def __init__(self, pos_: Tuple[int, int], size_: Tuple[int, int], win_, update_ticks_: int = 1) -> None:
        self._pos = pos_
        self._size = size_
        self._win = win_
        self._update_ticks = update_ticks_
        self._addtimer = 0
        self._space: Tuple[Particle, ...] = []
        
    def __construct_particle__(self, particle_: Particle, spavner_: ParticleSpawner):
        p_dict = {}
        for i in particle_.__dict__:
            p_dict[i] = copy(particle_.__dict__[i])
        
        
        # create position ---------------------------------------------
        
        if spavner_._type == particle_spawner_types.RECT:
            p_dict['POS'][0] = spavner_._pos[0]+random.randint(0,spavner_._size[0])
            p_dict['POS'][1] = spavner_._pos[1]+random.randint(0,spavner_._size[1])
        if spavner_._type == particle_spawner_types.LINE:
            vector = Vector2(spavner_._pos1[0]-spavner_._pos2[0], spavner_._pos1[1]-spavner_._pos2[1])
            vector*=-1
            lenght = int(vector.lenght)
            vector.normalyze()
            dist = random.randint(0, lenght)
            vector*=dist
            pos = [spavner_._pos1[0]+vector.x, spavner_._pos1[1]+vector.y]
            p_dict['POS'] = pos
        if spavner_._type == particle_spawner_types.POLYGONE:
            
            points = spavner_._points
            if len(points)>1:
                r_points = random.randint(0,len(points)-1)
                vector = Vector2(points[r_points][0]-points[r_points-1][0], points[r_points][1]-points[r_points-1][1])
                vector*=-1
                lenght = int(vector.lenght)
                vector.normalyze()
                dist = random.randint(0, lenght)
                vector*=dist
                pos = [points[r_points][0]+vector.x, points[r_points][1]+vector.y]
                p_dict['POS'] = pos 
        if spavner_._type == particle_spawner_types.CIRCLE:
            random_vector = Vector2(0,random.randint(0,spavner_._radius))
            random_vector.set_angle(random.randint(0,360))
            p_dict['POS'][0] = spavner_._pos[0]+random_vector.x
            p_dict['POS'][1] = spavner_._pos[1]+random_vector.y
        
        # create position ---------------------------------------------
        
        # create sprite -----------------------------------------------
        
        p_dict['SPRITE_START_ANGLE'] = random.randint(0,360)
        p_dict['SPRITE_START_SCALE'] += random.randint(0, p_dict['SPRITE_SCALE_RANDOMER']*1000)/1000
        if len(p_dict['SPRITE_LIST'])!=0:
            p_dict['SPRITE'] = random.choice(p_dict['SPRITE_LIST'])
            
        # create sprite -----------------------------------------------   
        
        # create radius -----------------------------------------------
        
        p_dict['RADIUS'] += random.randint(0, p_dict['RADIUS_RANDOMER'])
        p_dict['START_RADIUS'] = copy(p_dict['RADIUS'])
        
        # create radius -----------------------------------------------
        
        # create speed ------------------------------------------------
        
        p_dict['SPEED']+=Vector2([0,random.randint(0, p_dict['SPEED_RANDOMER']*1000)/1000])
        p_dict['SPEED'].set_angle(p_dict['SPEED_ANGLE']+random.randint(-p_dict['SPEED_DURATION'],p_dict['SPEED_DURATION']))
        if p_dict['SPEED_ROTATION']:
            if p_dict['SPEED_RANDOM_ROTATION_ANGLE'] != False:
                p_dict['SPEED_ROTATION_ANGLE'] = random.randint(p_dict['SPEED_RANDOM_ROTATION_ANGLE'][0],p_dict['SPEED_RANDOM_ROTATION_ANGLE'][1])
            
        # create speed ------------------------------------------------
        
        # create size -------------------------------------------------
        
        p_dict['SIZE'][0] += random.randint(0, p_dict['SIZE_RANDOMER'][0])
        p_dict['SIZE'][1] += random.randint(0, p_dict['SIZE_RANDOMER'][1])
        
        p_dict['START_SIZE'] = copy(p_dict['SIZE'])
        
        # create size -------------------------------------------------
        
        # create color ------------------------------------------------
        
        if p_dict['COLOR_RANDOM']:
            p_dict['COLOR'] = Color.random().rgb
        if len(p_dict['COLOR_FROM_DICT'])!= 0:
            p_dict['COLOR'] = random.choice(p_dict['COLOR_FROM_DICT'])
        
        # create color ------------------------------------------------

        # create dummy particle ---------------------------------------
        
        dummy = Particle()
        dummy.set_all(p_dict)
        return copy(dummy)
    
        # create dummy particle ---------------------------------------
    
    def tick(self):
        self._addtimer+=1
    
    def add(self, particle_: Particle, spawner_: ParticleSpawner, count_: int, sleep = 1):

        if self._addtimer%sleep==0:

            for i in range(count_):
                particle = self.__construct_particle__(particle_, spawner_)
                self._space.append(particle)
                
    def _construct_blend_circle(self, light_color, particle, surf):
        start_light_color = copy(light_color)
        color = [0,0,0]
        rad_scale = particle.BLEND_LIGHT_CIRCLES
        color_sum = [
                            -(color[0]-start_light_color[0])/rad_scale,
                            -(color[1]-start_light_color[1])/rad_scale,
                            -(color[2]-start_light_color[2])/rad_scale,
                        ]
        for i in range(rad_scale):
            color[0]+=color_sum[0]
            color[1]+=color_sum[1]
            color[2]+=color_sum[2]
            Draw.draw_circle(surf, [particle.RADIUS+particle.LIGHT_SIZE,particle.RADIUS+particle.LIGHT_SIZE], surf.get_width()/2-surf.get_width()*i/rad_scale, color)
    
    def render(self):
        for i, particle in enumerate( self._space ):
            #? RENDER SHADOW -----------------------------------------------------------------------------------------------------------------
            if particle.SHADOWING:
                if particle.SHAPE == particle_shapes.CIRCLE:
                    Draw.draw_circle(self._win.surf, [particle.POS[0]+particle.SHADOW_DX,particle.POS[1]+particle.SHADOW_DY], particle.RADIUS, particle.SHADOW_COLOR)
                if particle.SHAPE == particle_shapes.RECT:
                    Draw.draw_rect(self._win.surf, center_rect([particle.POS[0]+particle.SHADOW_DX,particle.POS[1]+particle.SHADOW_DY], particle.SIZE,True), particle.SIZE, particle.SHADOW_COLOR)
            #? RENDER SHADOW -----------------------------------------------------------------------------------------------------------------
        
        for i, particle in enumerate( self._space ):
            
            #? RENDER SHAPES -----------------------------------------------------------------------------------------------------------------
            if particle.SHAPE_RENDERER:
                if particle.SHAPE == particle_shapes.CIRCLE:
                    Draw.draw_circle(self._win.surf, particle.POS, particle.RADIUS, particle.COLOR)
                elif particle.SHAPE == particle_shapes.RECT:
                    Draw.draw_rect(self._win.surf, center_rect(particle.POS, particle.SIZE,True), particle.SIZE, particle.COLOR)
                elif particle.SHAPE == particle_shapes.IMAGE:
                    particle.SPRITE.center = particle.POS
                    particle.SPRITE.angle = particle.SPRITE_START_ANGLE
                    particle.SPRITE.scale = particle.SPRITE_START_SCALE
                    particle.SPRITE.render(self._win.surf)
                    
            #? RENDER SHAPES -----------------------------------------------------------------------------------------------------------------
            
            
            
            #? RENDER LINES ------------------------------------------------------------------------------------------------------------------
            if particle.LINES:
                line_color = particle.LINES_COLOR
                if particle.LINES_COLOR_FROM_PARTICLE_COLOR:
                    line_color = particle.COLOR
                    
                if particle.SHAPE == particle_shapes.CIRCLE:
                    size = particle.RADIUS*2
                if particle.SHAPE == particle_shapes.RECT:
                    size = max(particle.SIZE)
                if i-1>=0:
                    Draw.draw_aline(self._win.surf, self._space[i].POS, self._space[i-1].POS, line_color, size)
            #? RENDER LINES ------------------------------------------------------------------------------------------------------------------
                
            #? RENDER LIGHT ------------------------------------------------------------------------------------------------------------------
            if particle.LIGHTNING:
                
                if particle.SHAPE == particle_shapes.CIRCLE:
                    LIGHT_STRANGE = particle.LIGHT_STRANGE
                    if particle.LIGHT_STRANGE_BY_SIZE:
                        LIGHT_STRANGE = (particle.RADIUS/particle.START_RADIUS)*particle.LIGHT_STRANGE
                    
                    LIGHT_STRANGE = max(0,LIGHT_STRANGE)
                    light_color = particle.LIGHT_COLOR
                    if particle.LIGHT_COLOR_FROM_PARTICLE_COLOR:
                        light_color = particle.COLOR
                    light_color = [
                        light_color[0]*LIGHT_STRANGE,
                        light_color[1]*LIGHT_STRANGE,
                        light_color[2]*LIGHT_STRANGE,
                    ]
                    
                    surf = pygame.Surface([(particle.RADIUS+particle.LIGHT_SIZE)*2, (particle.RADIUS+particle.LIGHT_SIZE)*2],flags=pygame.SRCCOLORKEY)
                    
                    if particle.LIGHT_SHAPE == particle_shapes.CIRCLE:
                        Draw.draw_circle(surf, [particle.RADIUS+particle.LIGHT_SIZE,particle.RADIUS+particle.LIGHT_SIZE],particle.RADIUS+particle.LIGHT_SIZE, light_color)

                    if particle.LIGHT_SHAPE == particle_shapes.RECT:
                        Draw.draw_rect(surf, [0,0],surf.get_size(), light_color)
                        
                    if particle.LIGHT_SHAPE == particle_shapes.BLEND_CIRCLE:
                        self._construct_blend_circle(light_color, particle, surf)
                
                if particle.SHAPE == particle_shapes.RECT:
                    LIGHT_STRANGE = particle.LIGHT_STRANGE
                    if particle.LIGHT_STRANGE_BY_SIZE:
                        LIGHT_STRANGE = (particle.RADIUS/particle.START_RADIUS)*particle.LIGHT_STRANGE
                    
                    LIGHT_STRANGE = max(0,LIGHT_STRANGE)
                    light_color = particle.LIGHT_COLOR
                    if particle.LIGHT_COLOR_FROM_PARTICLE_COLOR:
                        light_color = particle.COLOR
                    light_color = [
                        light_color[0]*LIGHT_STRANGE,
                        light_color[1]*LIGHT_STRANGE,
                        light_color[2]*LIGHT_STRANGE,
                    ]
                    
                    size = max(particle.SIZE)
                    surf = pygame.Surface([(size+particle.LIGHT_SIZE)*2, (size+particle.LIGHT_SIZE)*2],flags=pygame.SRCCOLORKEY)
                    
                    if particle.LIGHT_SHAPE == particle_shapes.CIRCLE:
                        Draw.draw_circle(surf, [size+particle.LIGHT_SIZE,size+particle.LIGHT_SIZE],size+particle.LIGHT_SIZE, light_color)

                    if particle.LIGHT_SHAPE == particle_shapes.RECT:
                        Draw.draw_rect(surf, [0,0],surf.get_size(), light_color)
                
                self._win.surf.blit(surf, center_rect(particle.POS, surf.get_size(), True), special_flags=particle.LIGHT_MODE) 
            #? RENDER LIGHT ------------------------------------------------------------------------------------------------------------------
            
    def update(self, del_event_: callable):
        for particle in self._space:
            # speed using -------------------------------------------------
            particle.SPEED.x+=particle.GRAVITY_VECTOR[0]
            particle.SPEED.y+=particle.GRAVITY_VECTOR[1]
            if particle.SPEED_ROTATION:

                particle.SPEED.rotate(particle.SPEED_ROTATION_ANGLE)
            particle.SPEED*=particle.SPEED_FRICTION
            

            particle.POS[0]+=particle.SPEED.x
            particle.POS[1]+=particle.SPEED.y
            # speed using -------------------------------------------------
            
            # sprite methods ----------------------------------------------
            if particle.SPRITE_ANGLE_TYPE == sprite_angle_types.TO_ROTATE:
                particle.SPRITE_START_ANGLE += particle.SPRITE_ROTATE_ANGLE
            elif particle.SPRITE_ANGLE_TYPE == sprite_angle_types.TO_VECTOR:
                particle.SPRITE_START_ANGLE = particle.SPEED.get_angle() + particle.SPRITE_ADD_ANGLE
                
            
            # sprite methods ----------------------------------------------
            
            # timer methods -----------------------------------------------
            particle.TIMER+=1*self._win.delta
            if particle.TIMER>particle.RESIZE_START_TIME:
                if particle.SHAPE == particle_shapes.CIRCLE:
                    particle.RADIUS+=particle.RADIUS_RESIZE*self._win.delta
                if particle.SHAPE == particle_shapes.RECT:
                    particle.SIZE[0]+=particle.SIZE_RESIZE[0]*self._win.delta
                    particle.SIZE[1]+=particle.SIZE_RESIZE[1]*self._win.delta
                if particle.SHAPE == particle_shapes.IMAGE:
                    particle.SPRITE_START_SCALE += particle.SPRITE_SCALE_RESIZE*self._win.delta
            
            
            # timer methods -----------------------------------------------

        start_space = set(self._space)
        self._space = list(filter(lambda elem: elem.RADIUS>0, self._space))
        self._space = list(filter(lambda elem: elem.SPRITE_START_SCALE>0, self._space))
        end_space = set(self._space)
        del_space = start_space - end_space
        if len(del_space)>0:
            del_event_(list(del_space), self)
        
class ParticleTurbulesity:
    class MagnetCircle:
        def __init__(self, pos_: Tuple[int, int], radius_: float, strange_: float = 1) -> None:
            self.pos = pos_
            self.radius = radius_
            self.strange = strange_
            self.type = 'MAGNETCIRCLE'
            
        def draw(self, win):
            Draw.draw_circle(win.surf, self.pos, self.radius, 'red',1)
            
    class MagnetRect:
        def __init__(self, pos_: Tuple[int, int], size_: Tuple[int, int], strange_vector_ = Vector2(0,0)) -> None:
            self.pos = pos_
            self.size = size_
            self.strange_vector = strange_vector_
            self.type = 'MAGNETRECT'
            
        def draw(self, win):
            Draw.draw_rect(win.surf, self.pos, self.size, 'red',1)
            
    def __init__(self) -> None:
        self._space = []
        
    def add(self, obj_: Any):
        self._space.append(obj_)
        
    def simulate(self, particle_space_: ParticleSpace):
        for turbulensity in self._space:
            for particle in particle_space_._space:
                if turbulensity.type == 'MAGNETCIRCLE':
                    if distance(turbulensity.pos, particle.POS)<turbulensity.radius:
                        vector_normal = Vector2.Normal(turbulensity.pos, particle.POS)
                        vector_normal.normalyze()
                        lenght =  (1-(distance(turbulensity.pos, particle.POS)/turbulensity.radius))*turbulensity.strange
                        vector_normal*=lenght
                        particle.SPEED+=vector_normal
                        
                if turbulensity.type == 'MAGNETRECT':
                    if in_rect(turbulensity.pos, turbulensity.size, particle.POS):
                        particle.SPEED+=turbulensity.strange_vector


if __name__ == '__main__':
    
    win = Window()
    
    p = Particle()
    p.set('shape',particle_shapes.IMAGE)
    p.set('color',(255,130,200))
    p.set('speed',Vector2(0,0))
    p.set('size_randomer',[0,0])
    p.set('speed_angle',-90)
    p.set('speed_duration',180)
    
    p.SPEED_FRICTION = 0.99
    p.SPEED_RANDOMER = 2
    p.RESIZE_START_TIME = 100
    p.SPRITE_SCALE_RANDOMER = 2
    p.SPRITE_LIST = [ Sprite('api\ppp.png') ]
    p.SPRITE_START_SCALE = 1
    p.SPRITE_SCALE_RESIZE = -0.1
    p.SPRITE_ROTATE_ANGLE = 0.1
    p.SPRITE_ANGLE_TYPE = sprite_angle_types.TO_ROTATE
    p.SPRITE_ADD_ANGLE = -45
    

    

    space = ParticleSpace([0,0],[800,650],win)
    spawn = ParticleSpawner(type_=particle_spawner_types.CIRCLE,  pos_=[300,300],radius_=50)

    ts = ParticleTurbulesity()
    mag = ParticleTurbulesity.MagnetCircle([160,100],150,0.05)
    mag2 = ParticleTurbulesity.MagnetRect([300,100],[200,100],Vector2(0.01,0))
    ts.add(mag)
    ts.add(mag2)

    events = MouseEventHandler()
    events.AddEvent(Mouse(Mouse.left, Mouse.click_event,'cl'))
    
    while win(fps='max',base_color=(255,255,255)):
        ts.simulate(space)
        mag.draw(win)
        mag2.draw(win)
        
        space.tick()
        
        spawn._pos = Mouse.position()
        events.EventsUpdate()
        
        if events.GetEventById('cl'):
            space.add(p, spawn,10,1)
        

        space.render()
        space.update(lambda a, b:None)
    
    

    






    