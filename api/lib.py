# imports ---------------------------------------

import pygame_shaders
import subprocess
import threading
import pyperclip
import keyboard
import asyncio
import pygame
import socket
import random
import typing
import pickle
import mouse
import types
import tripy
import math
import time
import sys
import os



from dataclasses import dataclass
from colorama import Fore, Style
from io import TextIOWrapper
from ast import literal_eval
from threading import Thread
from typing import Callable, TypedDict, overload
from typing import Iterable
try:
    from libtypes import Color
except:
    from .libtypes import Color
try:
    from pygame import gfxdraw
    gfx = True
except:
    gfx = False
from typing import NewType
from typing import Tuple
from typing import Dict
from time import sleep
from typing import Any
from copy import copy,deepcopy

# imports ---------------------------------------

# init ------------------------------------------
__version__ = '1.22'
print(Fore.GREEN+'G-api ' +Fore.BLACK+ '[ '+Fore.MAGENTA+f'version: {__version__}'+Fore.BLACK+' ]'+Fore.RESET)
# init ------------------------------------------


# copying ---------------------------------------

def paste() -> str:
    return pyperclip.paste()

# copying ---------------------------------------

# asyncio ---------------------------------------

def create_task(func: Callable):
    return asyncio.create_task(func())

def add_tasks(tasks: asyncio.Task | Tuple[asyncio.Task, ...]) -> asyncio.Future:
    if isinstance(tasks, list):
        return asyncio.gather(*tasks)
    else:
        return asyncio.gather(tasks)
    
def run_file(file_name_: str , **kwargs):
    args = ""
    for name in kwargs:
        args += f"{name} {kwargs[name]} "
    # os.system("cmd")
    subprocess.Popen(["start", "cmd"], shell=True)
    time.sleep(0.1)
    keyboard.write(f"python {file_name_} {args}")
    keyboard.press("enter")
    
# asyncio ---------------------------------------

# math methods ----------------------------------

def out_min_max(value: float, min: float, max: float):
    if min<value<max:
        return False
    else:
        return True

def sign(num: int | float) -> bool | None:
    if num < 0:
        return -1
    elif num > 0:
        return 1
    elif num == 0:
        return 0

def posing(pos, dx=0, dy=0):
    death_pos = deepcopy(pos)
    return [death_pos[0] + dx, death_pos[1] + dy]

# math methods ----------------------------------

# vector ----------------------------------------

class Vector2:
    @staticmethod
    def Normal(pos1: Tuple[int, int] ,pos2: Tuple[int, int]) -> 'Vector2':
        return Vector2(pos1[0]-pos2[0], pos1[1]-pos2[1])
    
    @staticmethod
    def Random(start: float, stop: float):
        return Vector2(random.randint(start, stop), random.randint(start, stop))
    
    @overload
    def __init__(self, x_y: typing.Tuple[float, float]) -> "Vector2":
        ...

    @overload
    def __init__(self, x_: float, y_: float) -> "Vector2":
        ...

    def __init__(self, *_args) -> "Vector2":
        self.__args_manager__(*_args)

    def __args_manager__(self, *args):
        if len(args) == 1:
            self._x = args[0][0]
            self._y = args[0][1]
        elif len(args) == 2:
            self._x = args[0]
            self._y = args[1]

    def __str__(self) -> str:
        return f"Vector2 {self._x, self._y}"

    @property
    def lenght(self):
        l = vector_lenght(self._x, self._y)
        if l == 0:
            return 0.0000001
        return l

    @lenght.setter
    def lenght(self, _value: int):
        self._x *= _value / self.lenght
        self._y *= _value / self.lenght

    def rotate(self, angle: int):
        angle = math.radians(angle)
        _x = self._x * math.cos(angle) - self._y * math.sin(angle)
        _y = self._x * math.sin(angle) + self._y * math.cos(angle)
        self._x = _x
        self._y = _y

    def set_angle(self, angle: int):
        lenght = self.lenght
        angle = math.radians(angle)
        self._x = math.cos(angle) * lenght
        self._y = math.sin(angle) * lenght
        
    def scalar_angle(self, vector: 'Vector2') -> float:
        return (self.lenght*vector.lenght)*cos(math.radians(self.get_angle()-vector.get_angle()+90))

    def scalar_lenght(self, vector: 'Vector2') -> float:
        return (vector.x*self.x)+(vector.y*self.y)

    def get_angle(self) -> float:
        return angle_to_float([0, 0], [self._x, self._y])

    def normalyze(self):
        lenght = self.lenght
        self._x /= lenght
        self._y /= lenght

    @property
    def x(self) -> float:
        return self._x

    @property
    def y(self) -> float:
        return self._y

    @x.setter
    def x(self, value: float) -> None:
        self._x = value

    @y.setter
    def y(self, value: float) -> None:
        self._y = value
        
    @property
    def sw(self) -> float:
        return self._x
    
    @property
    def sh(self) -> float:
        return self._y

    @sw.setter
    def sw(self, value: float) -> None:
        self._x = value

    @sh.setter
    def sh(self, value: float) -> None:
        self._y = value
        
    @property
    def swh(self) -> typing.Tuple[int, int]:
        return [self._x, self._y]

    @swh.setter
    def swh(self, pos_: typing.Tuple[int, int]):
        self._x = pos_[0]
        self._y = pos_[1]

    @property
    def xy(self) -> typing.Tuple[int, int]:
        return [self._x, self._y]

    @xy.setter
    def xy(self, pos_: typing.Tuple[int, int]):
        self._x = pos_[0]
        self._y = pos_[1]

    def __iadd__(self, vector_: "Vector2") -> "Vector2":
        self.x += vector_.x
        self.y += vector_.y
        return self

    def __isub__(self, vector_: "Vector2") -> "Vector2":
        self.x -= vector_.x
        self.y -= vector_.y
        return self

    def __imul__(self, value_: float) -> "Vector2":
        self.x *= value_
        self.y *= value_
        return self

    def __add__(self, vector_: "Vector2") -> "Vector2":
        self.x += vector_.x
        self.y += vector_.y
        return self

    def __mul__(self, value_: float) -> "Vector2":
        self.x *= value_
        self.y *= value_

        return self

    def __sub__(self, vector_: float) -> "Vector2":
        self.x -= vector_.x
        self.y -= vector_.y

        return self

# vector ----------------------------------------

# timer -----------------------------------------

class Timer:
    def __init__(self, time_speed_: float = 1, time_f_: float = 0) -> None:
        self._timer_obj = 0
        self._ts = time_speed_
        self._tf = time_f_

        self._timer = 0

    def update(self):
        self._timer_obj += self._ts
        if self._timer_obj > self._tf:
            self._timer_obj = 0
            self._timer += 1

    def run(self, function_: callable, step_: int = 1, *args, **kvargs):
        if self._timer == step_:
            function_(*args, **kvargs)
            self._timer = 0

# timer -----------------------------------------

# shader ----------------------------------------

class Shader:
    def __init__(self, size, pos, vertex_file_, fragment_file_) -> None:
        self.shader_ = pygame_shaders.Shader(
            size, size, pos, vertex_file_, fragment_file_, 0
        )

    def clear(self, color=(0, 0, 0)):
        pygame_shaders.clear(color)

    def render(self, surf: pygame.Surface):
        self.shader_.render(surf)

    def send(self, name, data):
        self.shader_.send(name, data)

# shader ----------------------------------------


# base decorators -------------------------------

def NewProcess(name: str = None):
    if name is None:
        name = random.randint(0, 99999999999)

    def NewProcessInner(func: typing.Callable):
        def wrapper(*args, **kvargs):
            Thread(target=func, args=args, kwargs=kvargs, name=name).start()

        return wrapper

    return NewProcessInner

def TimeProcess(func: typing.Callable):
    def wrapper(*args, **kvargs):
        start = time.time()
        ret = func(*args, **kvargs)
        end = time.time()
        print(f"Time ({func.__name__}): {end - start}")
        return ret

    return wrapper

def get_thread_count():
    return threading.active_count()

def get_threads():
    return threading.enumerate()

# base decorators -------------------------------

# gradient --------------------------------------

class PrettyGradient:
    class TwoColors:
        def __init__(self, color_1: Color, color_2: Color, steps: int = 255, rgb_deltas = [1,1,1]) -> None:
            self._color_1 = color_1
            self._color_2 = color_2
            self._steps = steps
            self._rgb_deltas = rgb_deltas
            
            self.gradient_surf = pygame.Surface([self._steps,10])
        
        
        def generate(self):
            dr = self._color_2.r - self._color_1.r
            dg = self._color_2.g - self._color_1.g
            db = self._color_2.b - self._color_1.b
            
            delta_r = dr/self._steps
            delta_g = dg/self._steps
            delta_b = db/self._steps
            
            for i in range(self._steps):
                color = [
                    self._color_1.r+dr*sin(i/self._steps*self._rgb_deltas[0]),
                    self._color_1.g+dg*sin(i/self._steps*self._rgb_deltas[1]),
                    self._color_1.b+db*sin(i/self._steps*self._rgb_deltas[2]),
                ]
                Draw.draw_rect(self.gradient_surf, [i, 0], [2,10], color)
        
        def get_percent(self, percent: float):
            color = self.gradient_surf.get_at([int(self._steps*percent), 1])
            return [color.r, color.g, color.b]
    
    class ManyColors:
        def __init__(self, colors: Tuple[Color, ...], colors_steps: Tuple[int, ...], colors_rgb_deltas) -> None:
            self._colors = colors
            self._colors_steps = colors_steps
            self._colors_rgb_deltas = colors_rgb_deltas
            self._pos_x = 0
            
        def generate_gradient_surfs(self):
            self.all_step = 0
            for step in self._colors_steps:
                self.all_step+=step
                
            self.gradient_surf = pygame.Surface([self.all_step, 10])
            
            
        def generate(self):
            for i in range(len(self._colors)):
                color1 = self._colors[i-1]
                color2 = self._colors[i]
                step = self._colors_steps[i]
                delta = self._colors_rgb_deltas[i]
                cg = PrettyGradient.TwoColors(color1, color2, step, delta)
                cg.generate()
                self.gradient_surf.blit(cg.gradient_surf, [self._pos_x, 0])
                self._pos_x+=step
        
        def get_percent(self, percent: float):
            color = self.gradient_surf.get_at([int(self.all_step*percent), 1])
            return [color.r, color.g, color.b]

# gradient --------------------------------------

# sound class -----------------------------------

class Sound:
    def __init__(self, file_name_: str) -> "Sound":
        self._sound = pygame.mixer.Sound(file_name_)

    def play(self):
        self._sound.play()

# sound class -----------------------------------

# base window class -----------------------------

class Window:
    def __init__(
        self,
        size: list[int, int] = [800, 650],
        win_name: str = "Main",
        flag: typing.Any = None,
        cursor: Any = None,
    ) -> None:
        self.__size = size
        self.__win_name = win_name
        self.__flag = flag
        self._win_opened = False
        self._delta = 0
        self.__delta_velosity = 60
        self.__timer = 0
        self.size = [0, 0]

        self.__create_win_with_params(self.__size, self.__win_name, self.__flag)
        if cursor is not None:
            pygame.mouse.set_cursor(cursor)

        self._win_opened = True
        self._fps_surf = Text("Arial", 12, bold=True)
        self._exit_hot_key = "esc"
        self.press_key = None

        self.key = None
        
        self.__update_methods = []
        
    def add_update_method(self, method: Callable):
        self.__update_methods.append(method)
        
    def __update_update_methods(self):
        for update_method in self.__update_methods:
            update_method(self.delta)

    def __call__(
        self, fps=60, base_color="white", fps_view=True, exit_hot_key="esc"
    ) -> Any:
        return self.update(fps, base_color, fps_view, exit_hot_key)

    def __any_full__(self, _flag: typing.Any) -> bool:
        if type(_flag) == list:
            if _flag[0] == "anyfull":
                return True
        return False

    # def __call__(self) -> pygame.Surface:
    #    return self._win
    
    def get_size(self):
        return [*pygame.display.get_window_size()]

    @property
    def surf(self):
        return self._win

    def __create_win_with_params(
        self, _p_size: list, _p_win_name: str, _p_flag: typing.Any
    ) -> None:
        pygame.init()
        if self.__any_full__(_p_flag):
            _flag = _p_flag[1]
            _p_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]
        else:
            _flag = 0 if _p_flag is None else _p_flag
        self._win = pygame.display.set_mode(_p_size, _flag)
        pygame.display.set_caption(_p_win_name)
        self._clock = pygame.time.Clock()

    def __mathing_delta(self):
        fps = self.fps
        try:
            self._delta = self.__delta_velosity / fps
        except Exception:
            ...

    @property
    def delta(self) -> float:
        return self._delta

    @property
    def gsize(self) -> typing.Tuple[int, int]:
        return self._win.get_size()
    
    @gsize.setter
    def gsize(self, size: Tuple[int, int]):
        pygame.display.set_mode(size=size)

    @property
    def center(self) -> typing.Tuple[int, int]:
        return [*self._win.get_rect().center]

    @property
    def fps(self):
        return self._clock.get_fps()

    @property
    def timer(self):
        return self.__timer

    @fps.setter
    def fps(self, _framerate: int):
        if _framerate == "max":
            _framerate = 5000
        elif _framerate == "min":
            _framerate = 30
        else:
            ...
        self._clock.tick(_framerate)

    def __events_handling(self):
        global mouse__wheel
        _events = pygame.event.get()
        mouse__wheel = [0, 0]
        self.press_key = None
        for event in _events:
            if event.type == pygame.QUIT:
                self._win_opened = False
                os._exit(0)
            elif event.type == pygame.MOUSEWHEEL:
                mouse__wheel = [event.x, event.y]
            if event.type == pygame.VIDEORESIZE:
                self.size = event.size  # or event.w, event.h

            if event.type == pygame.KEYDOWN:
                self.press_key = pygame.key.name(event.key)

        if keyboard.is_pressed(self._exit_hot_key):
            self._win_opened = False
            os._exit(0)

    def fps_view(self):
        self._win.blit(
            self._fps_surf.render(f"FPS: {int( self.fps )}",(100,100,200)), (10, 10)
        )

    def update(
        self,
        fps: int = 60,
        base_color: list | str = "white",
        fps_view: bool = True,
        exit_hot_key: str = "esc",
    ) -> None:
        self._exit_hot_key = exit_hot_key
        self.__events_handling()

        self.fps = fps
        self.__mathing_delta()
        
        self.__update_update_methods()
        try:
            self.__timer += 1 * self.delta
        except:
            ...

        pygame.display.flip()
        self._win.fill(base_color)

        if fps_view:
            self.fps_view()

        return self._win_opened
    

    def get_at(self, x: int, y: int) -> list:
        return self._win.get_at((x, y))

# base window class -----------------------------

# bin files -------------------------------------

def WirteBinaryFile(file_name_: str, data_: Any) -> Any:
    with open(file_name_, "wb") as file:
        pickle.dump(data_, file)

def LoadBinaryFile(file_name_: str) -> Any:
    file = open(file_name_, "rb")
    return pickle.load(file)

# bin files -------------------------------------

# collide ---------------------------------------

class Rect(Vector2):
    @overload
    def __init__(self, x: float, y: float, w: float, h: float) -> "Rect":
        ...

    @overload
    def __init__(self, pos: Tuple[float, float], size: Tuple[float, float]) -> "Rect":
        ...

    def __init__(self, *args):
        self.__args_wrapper(*args)
        self.colliding = True
        self.ids = random.randint(0, 99999999999999)
        self.end_size = [0,0]

    def UDT(self):
        self.end_size = copy(self.wh)

    def __args_wrapper(self, *args):
        if len(args) == 4:
            _x = args[0]
            _y = args[1]
            self._w = args[2]
            self._h = args[3]
        elif len(args) == 2:
            _x = args[0][0]
            _y = args[0][1]
            self._w = args[1][0]
            self._h = args[1][1]
        super().__init__(_x, _y)

    def draw(self, win: Window):

        Draw.draw_rect(win, [self.x, self.y], self.wh, "red", 1)

    def collide_point(self, point: Tuple[float, float] | Vector2) -> bool:
        px, py = 0, 0
        if isinstance(point, Vector2):
            px = point.x
            py = point.y
        if isinstance(point, (list, tuple)):
            px = point[0]
            py = point[1]

        if (
            self.x < px
            and px < self.x + self.w
            and self.y < py
            and py < self.y + self.h
        ):
            return True

        return False

    def collide_rect(self, rect: "Rect", win: None = None):
        if self.colliding:
            min_x = min(self._x, rect._x)
            min_y = min(self._y, rect._y)

            max_x = max(self._x + self._w, rect._x + rect._w)
            max_y = max(self._y + self._h, rect._y + rect._h)

            if win is not None:
                Draw.draw_rect(
                    win,
                    [min_x - 2, min_y - 2],
                    [max_x - min_x + 4, max_y - min_y + 4],
                    "Blue",
                    2,
                )

            dist_w = distance([min_x, min_y], [max_x, min_y])
            dist_h = distance([min_x, min_y], [min_x, max_y])
            if dist_w < self._w + rect._w and dist_h < self._h + rect._h:
                return True
        return False

    @property
    def wh(self) -> Tuple[float, float]:
        return [self._w, self._h]

    @wh.setter
    def wh(self, size_: Tuple[float, float]):
        self.end_size = [self._w, self._h]
        self._w = int(size_[0])
        self._h = int(size_[1])

    @property
    def w(self) -> float:
        return self._w

    @w.setter
    def w(self, w: float):
        self.end_size = [self._w, self._h]
        self._w = w

    @property
    def h(self) -> float:
        return self._h

    @h.setter
    def h(self, h: float):
        self.end_size = [self._w, self._h]
        self._h = h

    @property
    def y_up(self) -> float:
        return self._y

    @y_up.setter
    def y_up(self, y: float):
        self._y = y

    @property
    def y_down(self) -> float:
        return self._y + self._h

    @y_down.setter
    def y_down(self, y: float):
        self._y = y - self._h

    @property
    def x_left(self) -> float:
        return self._x

    @x_left.setter
    def x_left(self, x: float):
        self._x = x

    @property
    def x_right(self) -> float:
        return self._x + self._w

    @x_right.setter
    def x_right(self, x: float):
        self._x = x - self._w

    @property
    def center(self):
        return [self._x + self._w / 2, self._y + self._h / 2]

    @property
    def center_x(self):
        return self._x + self._w / 2

    @property
    def center_y(self):
        return self._y + self._h / 2

    @center_x.setter
    def center_x(self, _x: int):
        self._x = _x - self._w / 2

    @center_y.setter
    def center_y(self, _y: int):
        self._y = _y - self._h / 2

    @center.setter
    def center(self, pos):
        self._x = pos[0] - self._w / 2
        self._y = pos[1] - self._h / 2

class Circle(Vector2):
    def __init__(self, pos: Tuple[float, float], radius: float):
        self.x = pos[0]
        self.y = pos[1]
        self._radius = radius
        
    def draw(self, win: Window):
        Draw.draw_circle(win, self.xy, self.r, "red", 1)
        
    def collide_point(self, point: Tuple[float, float] | Vector2) -> bool:
        px, py = 0, 0
        if isinstance(point, Vector2):
            px = point.x
            py = point.y
        if isinstance(point, (list, tuple)):
            px = point[0]
            py = point[1]
            
        if distance([px, py],self.xy) < self.r:
            return True
        
        return False
    
    def collide_circle(self, circle: 'Circle') -> bool:
        if distance(self.xy, circle.xy) < self.r + circle.r:
            return True
        else:
            return False
    
    @property
    def r(self) -> float:
        return self._radius
    
    @r.setter
    def r(self, r):
        self._radius = r
    
    @property
    def y_up(self) -> float:
        return self._y - self.r

    @y_up.setter
    def y_up(self, y: float):
        self._y = y + self.r

    @property
    def y_down(self) -> float:
        return self._y + self.r

    @y_down.setter
    def y_down(self, y: float):
        self._y = y - self.r

    @property
    def x_right(self) -> float:
        return self._x + self.r

    @x_right.setter
    def x_right(self, x: float):
        self._x = x - self.r

    @property
    def x_left(self) -> float:
        return self._x - self.r

    @x_left.setter
    def x_left(self, x: float):
        self._x = x + self.r
    
# collide ---------------------------------------

# flags -----------------------------------------

@dataclass
class Flags:
    win_full = pygame.FULLSCREEN
    win_resize = pygame.RESIZABLE
    win_scales = pygame.SCALED
    win_noframe = pygame.NOFRAME
    opengl = pygame.OPENGL
    win_anyfull = ["anyfull", pygame.FULLSCREEN]

    cursor_diamond = pygame.cursors.diamond
    cursor_ball = pygame.cursors.ball
    cursor_arrow = pygame.cursors.arrow
    cursor_broken = pygame.cursors.broken_x

# flags -----------------------------------------

# base text class -------------------------------

class Text:
    def __init__(
        self,
        font: pygame.font.Font,
        font_size: int,
        text: str = None,
        color: list | str = "white",
        bold: bool = False,
    ) -> None:
        pygame.font.init()

        self.__font = font
        self.__font_size = font_size
        self.__bold = bold
        self.__font_object = pygame.font.SysFont(
            self.__font, self.__font_size, self.__bold
        )
        if text is not None:
            self.__text = text
            self.__font_surf = self.__font_object.render(self.__text, True, color)

    def draw(
        self,
        surface: pygame.Surface,
        pos: list[int, int] = [0, 0],
        centering: bool = False,
        text: str = "",
        color: list | str = "white",
    ) -> None:
        self.__font_surf = self.__font_object.render(text, True, color)
        if centering:
            pos = [
                pos[0] - self.__font_surf.get_width() // 2,
                pos[1] - self.__font_surf.get_height() // 2,
            ]

        surface.blit(self.__font_surf, pos)
        return self.__font_surf.get_size()

    def render(self, text: str, color: list | str = "white", max_size=None) -> pygame.Surface:
        self.__text = text
        self.__font_surf = self.__font_object.render(self.__text, True, color)
        try:
            if max_size:
                self.__font_surf = self.__font_surf.subsurface([0,0,max_size,self.__font_surf.get_height()])
        except: ...
        return self.__font_surf

# base text class -------------------------------

# sprites ---------------------------------------

__image_color_key__ = (0,0,0)
def load_pg_image(file_name_: str) -> pygame.Surface:
    surf = pygame.image.load(file_name_).convert()
    surf.set_colorkey(__image_color_key__)
    return surf

class Sprite:
    def __init__(self, file_name_: str | None = None, tranfrom_and_rotate: bool = True, rotate_buffering: bool = False) -> None:
        self._file_name = file_name_
        if file_name_ is not None:
            self._start_sprite = self._load_sprite(self._file_name)
        self._transform_and_rotate = tranfrom_and_rotate
        self._rotate_buffering = rotate_buffering
        
        self._angle = 0
        self._scale = 1
        self._center_pos = [0, 0]
        self._r_buffer = []
        
        if self._rotate_buffering:
            self.buffering_rotate()
        
    def buffering_rotate(self):
        for i in range(360):
            self._r_buffer.append(pygame.transform.rotate(self._start_sprite, i).convert_alpha())
        print('buffering...')
    
    def start_sprite(self, surf_: pygame.Surface):
        self._start_sprite = surf_
        return self
        
    def _convert_center_pos(self, _pos: Tuple[float, float], _surf: pygame.Surface) -> Tuple[float, float]:
        _surf_size = _surf.get_size()
        return [_pos[0]-_surf_size[0]/2, _pos[1]-_surf_size[1]/2]
        
    def _load_sprite(self, _file_name: str) -> pygame.Surface:
        return load_pg_image(_file_name)
    
    def _set_transform_propertys(self) -> pygame.Surface:
        if not self._rotate_buffering:
            if self._transform_and_rotate:
                return pygame.transform.rotate(
                    pygame.transform.scale(self._start_sprite, [self._start_sprite.get_width()*self.scale, self._start_sprite.get_height()*self.scale]),
                    self.angle
                )
            else:
                
                surf = pygame.transform.rotate(self._start_sprite, self.angle)
                surf = pygame.transform.scale(
                    surf,  [surf.get_width()*self.scale, surf.get_height()*self.scale]
                )
                return surf
        else:
            surf = self._r_buffer[int(self.angle)%360]
            surf = pygame.transform.scale(
                surf, [surf.get_width()*self.scale, surf.get_height()*self.scale]
            )
            return surf
    
    @property
    def center(self) -> Tuple[float, float]:
        return self._center_pos
    
    @center.setter
    def center(self, center: Tuple[float, float]):
        self._center_pos = center
    
    @property
    def angle(self) -> float:
        return self._angle
    
    @angle.setter
    def angle(self, angle: float):
        # Set angle property from Sprite
        self._angle = angle
    
    @property
    def scale(self) -> float:
        return self._scale
    
    @scale.setter
    def scale(self, scale: float):
        # Set scale property from Sprite
        self._scale = scale
        
    @property
    def size(self):
        surf = self._set_transform_propertys()
        return [*surf.get_size()]
    
    def transform(self, _angle: None | float = None, _scale: None | float = None) -> None:
        # Set transform propertis from Sprite
        self.scale = _scale
        self.angle = _angle
        
    def render(self, _surf: pygame.Surface):
        _rendered_surf = self._set_transform_propertys()
        _rendered_pos = self._convert_center_pos(self.center, _rendered_surf)
        _surf.blit(_rendered_surf, _rendered_pos)
    
class AnimatedSprite:
    '''  
    # -------------Colors---------------                                            
    # Line color              -> (255,   0, 255)        
    # Colom color             -> (255, 255,   0)        
    # Size color              -> (  0,   0, 255)        
    '''
    
    @classmethod
    def load_sprites(self, file_name_: str) -> Tuple[pygame.Surface, ...]:
        canvas_ = load_pg_image(file_name_)

        width_ = canvas_.get_size()[0]
        height_ = canvas_.get_size()[1]


        spritets_coloms = []
        sizes_poses = []

        for i in range(height_):
            c = canvas_.get_at([0, i])
            color = (c[0], c[1], c[2])
            if color == (255, 0, 255):
                spritets_coloms.append(i)

        for col in spritets_coloms:
            for line in range(width_):
                c = canvas_.get_at([line, col])
                color = (c[0], c[1], c[2])
                if color == (255, 255, 0):
                    pos = [line + 1, col]
                    spw = 0
                    sph = 0
                    for sw in range(width_ - line):
                        c = canvas_.get_at([line + sw, col])
                        color = (c[0], c[1], c[2])
                        if color == (0, 0, 255):
                            spw = sw
                            break
                    for sh in range(height_ - col):
                        c = canvas_.get_at([line, col + sh])
                        color = (c[0], c[1], c[2])
                        if color == (0, 0, 255):
                            sph = sh
                            break
                    sizes_poses.append([[pos[0], pos[1] + 1], [spw, sph]])
        textures = []
        
        for sp in sizes_poses:
            canvas_.set_clip(sp[0], sp[1])
            texture = canvas_.get_clip()
            surft = canvas_.subsurface(texture)
            textures.append(surft)
        return textures

    def _create_sprites(self, file_name: str) -> Tuple[Sprite, ...]:
        _sprites = self.load_sprites(file_name)
        _new_sprites = [Sprite().start_sprite(_image) for _image in _sprites]
        return _new_sprites

    def __init__(self, file_name_: str, speed_: int = 10) -> None:
        self._sprites: Tuple[Sprite, ...] = self._create_sprites(file_name_)
        
        self._time = 0
        self._speed = speed_
        self._index = 0
        
        self._center_pos = [0, 0]
        self._scale = 0
        self._angle = 0
    
    def _set_transform_propertys(self):
        for sprite in self._sprites:
            sprite.transform(self.angle, self.scale)
            sprite.center = self._center_pos
        
    @property
    def angle(self) -> float:
        return self._angle
    
    @angle.setter
    def angle(self, angle):
        self._angle = angle
        self._set_transform_propertys()
        
    @property
    def center(self) -> Tuple[float, float]:
        return self._center_pos
    
    @center.setter
    def center(self, center) -> Tuple[float, float]:
        self._center_pos = center
        self._set_transform_propertys()
        
    @property
    def scale(self) -> float:
        return self._scale
    
    @scale.setter
    def scale(self, scale):
        self._scale = scale
        self._set_transform_propertys()
        
    def transform(self, _angle: None | float = None, _scale: None | float = None) -> None:
        # Set transform propertis from Sprite
        self.scale = _scale
        self.angle = _angle
        self._set_transform_propertys()
        
    def update(self):
        self._time += 1
        if self._time>=self._speed:
            self._index += 1
            self._time = 0
        if self._index >= len(self._sprites):
            self._index = 0 
        
    def render(self, surf_: pygame.Surface):
        self._sprites[self._index].render(surf_)

class Tiles(TypedDict):
    up: Sprite
    up_left: Sprite
    up_right: Sprite
    down: Sprite
    down_left: Sprite
    down_right: Sprite
    left: Sprite
    right: Sprite
    center: Sprite
    
    vertical_up: Sprite
    vertical_middle: Sprite
    vertical_down: Sprite
    
    horisontal_left: Sprite
    horisontal_middle: Sprite
    horisontal_right: Sprite
    
    one: Sprite
    
    center_left: Sprite
    center_right: Sprite

class TileSheat:
    def __init__(self, tiles_file: str, tile_size: Tuple[int, int], tiles_count: int) -> None:
        self._tile_size = tile_size
        self._tiles_count = tiles_count
        self._tiles_file = load_pg_image(tiles_file)
        self._cutting_sprites: Tuple[pygame.Surface, ...] = []
        self._converting_sprites: Tuple[Sprite, ...] = []
        
        self.tiles = Tiles()
        
    def cutting(self):
        x = 0
        y = 0
        for i in range(self._tiles_count):
            sprite = self._tiles_file.subsurface([x,y, self._tile_size[0], self._tile_size[1]])
            self._cutting_sprites.append(sprite)
            x+=self._tile_size[0]
            if x==self._tiles_file.get_width():
                x = 0
                y += self._tile_size[1]
                
        self.converting()
                
    def converting(self):
        for spr in self._cutting_sprites:
            sprite = Sprite().start_sprite(spr)
            self._converting_sprites.append(sprite)
            
    def create(self):
        self.cutting()
        
        self.tiles['up_left'] = self._converting_sprites[0]
        self.tiles["up"] = self._converting_sprites[1]
        self.tiles['up_right'] = self._converting_sprites[2]
        
        self.tiles["left"] = self._converting_sprites[4]
        self.tiles['center'] = self._converting_sprites[5]
        self.tiles["right"] = self._converting_sprites[6]
        
        self.tiles['down_left'] = self._converting_sprites[8]
        self.tiles["down"] = self._converting_sprites[9]
        self.tiles['down_right'] = self._converting_sprites[10]
                
        self.tiles['vertical_up'] = self._converting_sprites[3]
        self.tiles['vertical_middle'] = self._converting_sprites[7]
        self.tiles['vertical_down'] = self._converting_sprites[11]
        
        self.tiles["horisontal_left"] = self._converting_sprites[12]
        self.tiles["horisontal_middle"] = self._converting_sprites[13]
        self.tiles["horisontal_right"] = self._converting_sprites[14]
        
        self.tiles["one"] = self._converting_sprites[15] 
        
        self.tiles['center_left'] = self._converting_sprites[16]
        self.tiles['center_right'] = self._converting_sprites[17]
        
# sprites ---------------------------------------



# map generators --------------------------------

def tiles_scale(TileSheat, scale):
    for tilename in TileSheat.tiles:
        TileSheat.tiles[tilename].scale = scale

def get_pos_with_xy_and_size(x, y, size):
    return [x*size[0], y*size[1]]

def get_pos_with_xy_and_size_no_center(x, y, size):
    return [x*size[0]+size[0]/2, y*size[1]+size[1]/2]

def create_map_surf_by_tilesheats_and_array(tile_sheats_dict, map_array):
    
    #map_array = copy(map_array)
    
    tile_size = tile_sheats_dict[1].tiles['one'].size
    map_surf_size = [(len(map_array[0]))*tile_size[0],(len(map_array))*tile_size[1]]
    
    map_surf = pygame.Surface(map_surf_size, flags=pygame.SRCALPHA, depth=32)
    

    tiles_keys = tile_sheats_dict.keys()
    
    
    for x in range(len(map_array)):
        for y in range(len(map_array[x])+1):
            try:
                find = True
                pos = get_pos_with_xy_and_size_no_center(x, y, tile_size)
                tsh = tile_sheats_dict[map_array[y][x]]
            except:
                find = False
                    

                
            if find:
                tile_name = 'one'
                
                x_right = x+1
                y_down = y+1
                x_left = x-1
                y_up = y-1
                if x_right == len(map_array[0]):    x_right = 0
                if y_down == len(map_array):        y_down  = 0
                
                if map_array[y_up][x] not in tiles_keys and map_array[y_down][x] not in tiles_keys:
                    if (
                        map_array[y][x_left] in tiles_keys and
                        map_array[y][x_right] in tiles_keys
                        ):
                        tile_name = 'horisontal_middle'
                    elif (
                        map_array[y][x_left] not in tiles_keys and
                        map_array[y][x_right] in tiles_keys
                        ):
                        tile_name = 'horisontal_left'
                    elif (
                        map_array[y][x_left] in tiles_keys and
                        map_array[y][x_right] not in tiles_keys
                        ):
                        tile_name = 'horisontal_right'
                
                elif map_array[y_up][x] in tiles_keys and map_array[y_down][x] not in tiles_keys:
                    
                    if (
                        map_array[y][x_left] not in tiles_keys and
                        map_array[y][x_right] not in tiles_keys
                        ):
                        tile_name = 'vertical_down'
                    elif (
                        map_array[y][x_left] in tiles_keys and
                        map_array[y][x_right] in tiles_keys
                        ):
                        tile_name = 'down'
                    elif (
                        map_array[y][x_left] not in tiles_keys and
                        map_array[y][x_right] in tiles_keys
                        ):
                        tile_name = 'down_left'
                    elif (
                        map_array[y][x_left] in tiles_keys and
                        map_array[y][x_right] not in tiles_keys
                        ):
                        tile_name = 'down_right'
                
                elif map_array[y_up][x] not in tiles_keys:
                    if (
                        map_array[y][x_left] not in tiles_keys and
                        map_array[y][x_right] not in tiles_keys
                        ):
                        tile_name = 'vertical_up'
                    elif (
                        map_array[y][x_left] in tiles_keys and
                        map_array[y][x_right] in tiles_keys
                        ):
                        tile_name = 'up'
                    elif (
                        map_array[y][x_left] not in tiles_keys and
                        map_array[y][x_right] in tiles_keys
                        ):
                        tile_name = 'up_left'
                    elif (
                        map_array[y][x_left] in tiles_keys and
                        map_array[y][x_right] not in tiles_keys
                        ):
                        tile_name = 'up_right'
                
                elif map_array[y_up][x] in tiles_keys:
            
                    if (
                        map_array[y][x_left] not in tiles_keys and
                        map_array[y][x_right] not in tiles_keys
                        ):
                        tile_name = 'vertical_middle'
                    elif (
                        map_array[y][x_left] in tiles_keys and
                        map_array[y][x_right] in tiles_keys
                        ):
                        if (
                            map_array[y_up][x_left] in tiles_keys and
                            map_array[y_up][x_right] in tiles_keys
                            ):
                            tile_name = 'center'
                        elif (
                            map_array[y_up][x_left] not in tiles_keys and
                            map_array[y_up][x_right] in tiles_keys
                            ):
                            tile_name = 'center_right'
                        elif (
                            map_array[y_up][x_left] in tiles_keys and
                            map_array[y_up][x_right] not in tiles_keys
                            ):
                            tile_name = 'center_left'
                        
                    elif (
                        map_array[y][x_left] not in tiles_keys and
                        map_array[y][x_right] in tiles_keys
                        ):
                        tile_name = 'left'
                    elif (
                        map_array[y][x_left] in tiles_keys and
                        map_array[y][x_right] not in tiles_keys
                        ):
                        tile_name = 'right'
                        
                
                
                
                
                
                tsh.tiles[tile_name].center = pos
                tsh.tiles[tile_name].render(map_surf)
                
    return map_surf

def create_map_surf_by_tilesheats_and_array_no_connect(tile_sheats_dict, map_array_all):
    
    tile_size = tile_sheats_dict[1].tiles['one'].size
    map_surf_size = [(len(map_array_all[0]))*tile_size[0],(len(map_array_all))*tile_size[1]]

    g_map_surf = pygame.Surface(map_surf_size, flags=pygame.SRCALPHA, depth=32)
    
    mass = []
    for i in map_array_all:
        mass.extend(i)
    mass = set(mass)
    mass.remove(0)
    lists_count = list(mass)
    
    new_generated_maps = []
    new_generated_maps_size = [len(map_array_all[0]), len(map_array_all)]
    
    for k in lists_count:
        nm = []
        for y in range(new_generated_maps_size[1]):
            mapp = []
            for x in range(new_generated_maps_size[0]):
                if map_array_all[y][x] == k:
                    mapp.append(k)
                else:
                    mapp.append(0)
            nm.append(mapp)
        
        new_generated_maps.append(nm)
    
    
    
    tiles_keys = list(tile_sheats_dict.keys())

    for i, map_array  in enumerate( new_generated_maps ):
        map_surf = pygame.Surface(map_surf_size, flags=pygame.SRCALPHA, depth=32)
        
        
        
        for x in range(len(map_array)):
            for y in range(len(map_array[x])+1):
                try:
                    find = True
                    pos = get_pos_with_xy_and_size_no_center(x, y, tile_size)
                    tsh = tile_sheats_dict[map_array[y][x]]
                except:
                    find = False
                        

                    
                if find:
                    tile_name = 'one'
                    
                    x_right = x+1
                    y_down = y+1
                    x_left = x-1
                    y_up = y-1
                    if x_right == len(map_array[0]):    x_right = 0
                    if y_down == len(map_array):        y_down  = 0
                    
                    if map_array[y_up][x] not in tiles_keys and map_array[y_down][x] not in tiles_keys:
                        if (
                            map_array[y][x_left] in tiles_keys and
                            map_array[y][x_right] in tiles_keys
                            ):
                            tile_name = 'horisontal_middle'
                        elif (
                            map_array[y][x_left] not in tiles_keys and
                            map_array[y][x_right] in tiles_keys
                            ):
                            tile_name = 'horisontal_left'
                        elif (
                            map_array[y][x_left] in tiles_keys and
                            map_array[y][x_right] not in tiles_keys
                            ):
                            tile_name = 'horisontal_right'
                    
                    elif map_array[y_up][x] in tiles_keys and map_array[y_down][x] not in tiles_keys:
                        
                        if (
                            map_array[y][x_left] not in tiles_keys and
                            map_array[y][x_right] not in tiles_keys
                            ):
                            tile_name = 'vertical_down'
                        elif (
                            map_array[y][x_left] in tiles_keys and
                            map_array[y][x_right] in tiles_keys
                            ):
                            tile_name = 'down'
                        elif (
                            map_array[y][x_left] not in tiles_keys and
                            map_array[y][x_right] in tiles_keys
                            ):
                            tile_name = 'down_left'
                        elif (
                            map_array[y][x_left] in tiles_keys and
                            map_array[y][x_right] not in tiles_keys
                            ):
                            tile_name = 'down_right'
                    
                    elif map_array[y_up][x] not in tiles_keys:
                        if (
                            map_array[y][x_left] not in tiles_keys and
                            map_array[y][x_right] not in tiles_keys
                            ):
                            tile_name = 'vertical_up'
                        elif (
                            map_array[y][x_left] in tiles_keys and
                            map_array[y][x_right] in tiles_keys
                            ):
                            tile_name = 'up'
                        elif (
                            map_array[y][x_left] not in tiles_keys and
                            map_array[y][x_right] in tiles_keys
                            ):
                            tile_name = 'up_left'
                        elif (
                            map_array[y][x_left] in tiles_keys and
                            map_array[y][x_right] not in tiles_keys
                            ):
                            tile_name = 'up_right'
                    
                    elif map_array[y_up][x] in tiles_keys:
                
                        if (
                            map_array[y][x_left] not in tiles_keys and
                            map_array[y][x_right] not in tiles_keys
                            ):
                            tile_name = 'vertical_middle'
                        elif (
                            map_array[y][x_left] in tiles_keys and
                            map_array[y][x_right] in tiles_keys
                            ):
                            if (
                                map_array[y_up][x_left] in tiles_keys and
                                map_array[y_up][x_right] in tiles_keys
                                ):
                                tile_name = 'center'
                            elif (
                                map_array[y_up][x_left] not in tiles_keys and
                                map_array[y_up][x_right] in tiles_keys
                                ):
                                tile_name = 'center_right'
                            elif (
                                map_array[y_up][x_left] in tiles_keys and
                                map_array[y_up][x_right] not in tiles_keys
                                ):
                                tile_name = 'center_left'
                            
                        elif (
                            map_array[y][x_left] not in tiles_keys and
                            map_array[y][x_right] in tiles_keys
                            ):
                            tile_name = 'left'
                        elif (
                            map_array[y][x_left] in tiles_keys and
                            map_array[y][x_right] not in tiles_keys
                            ):
                            tile_name = 'right'
                            
                    
                    
                    
                    
                    
                    tsh.tiles[tile_name].center = pos
                    tsh.tiles[tile_name].render(map_surf)

        
        g_map_surf.blit(map_surf, [0,0])
        
    return g_map_surf
        
# map generators --------------------------------

# base math class -------------------------------

def two_element_typing_xy(iterable_: list | tuple | Vector2):
    if isinstance(iterable_, (list, tuple)):
        return iterable_[0], iterable_[1]
    elif isinstance(iterable_, Vector2):
        return iterable_.x, iterable_.y

def two_element_typing_x_y(iterable_: list | tuple | Vector2):
    if isinstance(iterable_, (list, tuple)):
        return [iterable_[0], iterable_[1]]
    elif isinstance(iterable_, Vector2):
        return [iterable_.x, iterable_.y]

def distance(
    point_1: Any | typing.Tuple[int, int], point_2: Any | typing.Tuple[int, int]
):
    dx = point_1[0] - point_2[0]
    dy = point_1[1] - point_2[1]
    _distance = math.sqrt(dx**2 + dy**2)
    return _distance

def distance_to_line(
    l_point_1: Any | typing.Tuple[int,int], l_point_2: Any | typing.Tuple[int,int], point: Any | typing.Tuple[int,int]
):
    d1 = distance(l_point_2, point)
    d2 = distance(l_point_1, point)
    l = distance(l_point_2, l_point_1)
    p = (d1 + d2 + l) /2
    h = (2*math.sqrt(p*(p-l)*(p-d1)*(p-d2)))/l
    return h
    
def distance_to_line_stop(
    l_point_1: Any | typing.Tuple[int,int], l_point_2: Any | typing.Tuple[int,int], point: Any | typing.Tuple[int,int]
):
    d1 = distance(l_point_2, point)
    d2 = distance(l_point_1, point)
    l = distance(l_point_2, l_point_1)
    p = (d1 + d2 + l) /2
    h = (2*math.sqrt(p*(p-l)*(p-d1)*(p-d2)))/l
    
    l_angle = angle_to(l_point_1, l_point_2)
    p1_angle = angle_to(l_point_1, point) - l_angle
    p2_angle = angle_to(l_point_2, point) - l_angle
    #print(p1_angle, p2_angle)
    if (p1_angle<90 or p1_angle>270) and (p2_angle>90 and p2_angle<270):
        return h
    else:
        return None

def rotate_angle(origin, point, angle):
    """
    Rotate a point counterclockwise by a given angle around a given origin.
    The angle should be given in radians.
    """
    angle = math.radians(angle)
    ox, oy = origin
    px, py = point

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy

# create method get center position with two point type list ot type vector2 ->

def center_pos(
    point_1: Vector2 | typing.Tuple[int, int], point_2: Vector2 | typing.Tuple[int, int]
):
    x1, y1 = two_element_typing_xy(point_1)
    x2, y2 = two_element_typing_xy(point_2)
    dx = (x1 - x2) / 2
    dy = (y1 - y2) / 2
    return [x2 + dx, y2 + dy]

def vector_lenght(lenght_x: int, lenght_y: int):
    _distance = math.sqrt(lenght_x**2 + lenght_y**2)
    if distance==0:
        return 1
    return _distance

def rect_center(rect_pos: typing.Tuple[int, int], rect_size: typing.Tuple[int, int]):
    return [rect_pos[0] + rect_size[0] / 2, rect_pos[1] + rect_size[1] / 2]

def angle_to(
    point_1: typing.Tuple[int, int] | "Vector2",
    point_2: typing.Tuple[int, int] | "Vector2",
) -> float:
    pos1 = two_element_typing_x_y(point_1)
    pos2 = two_element_typing_x_y(point_2)

    atan = math.atan2(pos1[0] - pos2[0], pos1[1] - pos2[1])
    return int(atan / math.pi * 180 + 180)

def center_rect(
    pos: typing.Tuple[int, int], size: typing.Tuple[int, int], _reverse: bool = False
) -> Tuple[int, int]:
    if not _reverse:
        return [pos[0] + size[0] / 2, pos[1] + size[1] / 2]
    else:
        return [pos[0] - size[0] / 2, pos[1] - size[1] / 2]

def angle_to_float(
    point_1: typing.Tuple[int, int] | "Vector2",
    point_2: typing.Tuple[int, int] | "Vector2",
) -> float:
    if isinstance(point_1, Vector2):
        pos1 = point_1.xy
    elif isinstance(point_1, (list, tuple)):
        pos1 = point_1

    if isinstance(point_2, Vector2):
        pos2 = point_2.xy
    elif isinstance(point_2, (list, tuple)):
        pos2 = point_2

    atan = math.atan2(pos1[0] - pos2[0], pos1[1] - pos2[1])
    return (atan / math.pi * 180 + 180) % 360

def triangulate(polygone_points_: Tuple[Tuple[int,int], ...]):
    return tripy.earclip(polygone_points_)

def in_rect(
    rect_pos_: typing.Tuple[float, float] | Vector2,
    rect_size_: typing.Tuple[float, float] | Vector2,
    point_: typing.Tuple[float, float] | Vector2,
):
    if isinstance(rect_pos_, Vector2):
        rect_pos = rect_pos_.xy
    elif isinstance(rect_pos_, (list, tuple)):
        rect_pos = rect_pos_

    if isinstance(rect_size_, Vector2):
        rect_size = rect_size_.xy
    elif isinstance(rect_size_, (list, tuple)):
        rect_size = rect_size_

    if isinstance(point_, Vector2):
        point = point_.xy
    elif isinstance(point_, (list, tuple)):
        point = point_

    if (
        point[0] > rect_pos[0]
        and point[0] < rect_pos[0] + rect_size[0]
        and point[1] > rect_pos[1]
        and point[1] < rect_pos[1] + rect_size[1]
    ):
        return True
    else:
        return False

def in_circle(
    circle_pos_: typing.Tuple[float, float] | Vector2,
    circle_rad_: float,
    point_: typing.Tuple[float, float] | Vector2
):
    if isinstance(circle_pos_, Vector2):
        circle_pos = circle_pos_.xy
    elif isinstance(circle_pos_, (list, tuple)):
        circle_pos = circle_pos_
        
    if isinstance(point_, Vector2):
        point = point_.xy
    elif isinstance(point_, (list, tuple)):
        point = point_
    if distance(circle_pos, point)<circle_rad_:
        return True
    return False

def in_polygone(
    triangles: Tuple[Tuple[int,int,int], ...],
    point_: typing.Tuple[float, float] | Vector2
):
    if isinstance(point_, Vector2):
        point = point_.xy
    elif isinstance(point_, (list, tuple)):
        point = point_
        
    
    
    for k, t in enumerate( triangles):
        Ttrue = 0
        for i in range(3):

            vec = Vector2.Normal(copy(triangles[k][i]),copy(triangles[k][i-1]))
            p_vec = Vector2.Normal(copy(triangles[k][i-1]), point)
            n = vec.scalar(p_vec)
            if n<0:
                Ttrue+=1
    

        if Ttrue==0:
            return True
        
        
        
        
        
        
    return False

def sin(value: float) -> float:
    return math.sin(value)

def cos(value: float) -> float:
    return math.cos(value)

# base math class -------------------------------

# base draw class -------------------------------

class Draw:
    @classmethod
    def __outline(self, _color, _width, _type, _surf, **kvargs):
        if _type == "rect":
            radius = kvargs["radius"]
            pos = kvargs["pos"]
            size = kvargs["size"]
            Draw.draw_rect(_surf, pos, size, _color, _width, radius=radius)
        elif _type == "circle":
            radius = kvargs["radius"]
            pos = kvargs["pos"]
            Draw.draw_circle(_surf, pos, radius, _color, _width)
        elif _type == "polygone":
            points = kvargs["points"]
            Draw.draw_alines(_surf, points, _color, _width, True)
            
    @staticmethod
    def draw_rect(
        surface: pygame.Surface,
        pos: list[int],
        size: list[int],
        color: list | str | Color = "gray",
        width: int = 0,
        radius: int = -1,
        outline: typing.Tuple[list | str | Color, int] = None,
    ) -> None:
        if len(size) == 1:
            size = [size[0], size[0]]
        if isinstance(radius, (list, tuple)):
            lt_rad = radius[0]
            rt_rad = radius[1]
            rb_rad = radius[2]
            lb_rad = radius[3]
            radius = -1
        else:
            lt_rad = radius
            rt_rad = radius
            rb_rad = radius
            lb_rad = radius
        if isinstance(color, Color):
            color = color.rgb
        pygame.draw.rect(
            surface, color, (pos, size), width, radius, lt_rad, rt_rad, lb_rad, rb_rad
        )

        if outline is not None:
            Draw.__outline(
                outline[0],
                outline[1],
                "rect",
                surface,
                radius=(lt_rad, rt_rad, rb_rad, lb_rad),
                pos=pos,
                size=size,
            )

    @staticmethod
    def draw_rc_rect(
        surf: pygame.Surface,
        center: list[int],
        size: list[int],
        angle: float = 0,
        color: list | str | Color = "gray",
        width: int = 0,
        outline: typing.Tuple[list | str | Color, int] = None,
    ):
        normal_vector = Vector2(0,20)
        normal_vector.set_angle(angle)
        normal_vector.normalyze()
        
        left_rigth_vector = copy(normal_vector)
        left_rigth_vector.rotate(90)
        
        center_vector = Vector2(center)
        
        normal_vector*=size[0]/2
        left_rigth_vector*=size[1]/2
        pos1 = [
            center_vector.x+normal_vector.x+left_rigth_vector.x,
            center_vector.y+normal_vector.y+left_rigth_vector.y,
        ]
        pos2 = [
            center_vector.x+normal_vector.x-left_rigth_vector.x,
            center_vector.y+normal_vector.y-left_rigth_vector.y,
        ]
        pos3 = [
            center_vector.x-normal_vector.x+left_rigth_vector.x,
            center_vector.y-normal_vector.y+left_rigth_vector.y,
        ]
        pos4 = [
            center_vector.x-normal_vector.x-left_rigth_vector.x,
            center_vector.y-normal_vector.y-left_rigth_vector.y,
        ]
        
        
        Draw.draw_polygone(surf, [pos1,pos2, pos4,pos3], color, width, outline)

    @staticmethod
    def draw_rc_triangle(
        surf: pygame.Surface,
        center: list[int],
        size: list[int],
        angle: float = 0,
        color: list | str | Color = "gray",
        width: int = 0,
        outline: typing.Tuple[list | str | Color, int] = None,
    ):
        normal_vector = Vector2(0,20)
        normal_vector.set_angle(angle)
        normal_vector.normalyze()
        
        left_rigth_vector = copy(normal_vector)
        left_rigth_vector.rotate(90)
        
        center_vector = Vector2(center)
        
        normal_vector*=size[0]/2
        left_rigth_vector*=size[1]/2
        pos1 = [
            center_vector.x-normal_vector.x+left_rigth_vector.x,
            center_vector.y-normal_vector.y+left_rigth_vector.y,
        ]
        pos2 = [
            center_vector.x-normal_vector.x-left_rigth_vector.x,
            center_vector.y-normal_vector.y-left_rigth_vector.y,
        ]
        pos4 = [
            center_vector.x+normal_vector.x,
            center_vector.y+normal_vector.y,
        ]
        
        
        Draw.draw_polygone(surf, [pos1, pos2, pos4], color, width, outline)

    @staticmethod
    def draw_rp_line(
        surf: pygame.Surface,
        pos: list[int],
        lenght: int = 100,
        angle: float = 0,
        color: list | str | Color = "gray",
        width: int = 1,
        circled: bool = True
    ):
        normal_vector = Vector2(0,100)
        normal_vector.normalyze()
        
        normal_vector*=lenght
        normal_vector.set_angle(angle)
        
        Draw.draw_aline(surf, pos, [pos[0]+normal_vector.x,pos[1]+normal_vector.y], color, width, circled)
    
    @staticmethod
    def draw_rc_line(
        surf: pygame.Surface,
        center: list[int],
        lenght: int = 100,
        angle: float = 0,
        color: list | str | Color = "gray",
        width: int = 1
    ):
        normal_vector = Vector2(0,100)
        normal_vector.normalyze()
        
        normal_vector*=lenght/2
        normal_vector.set_angle(angle)
        
        Draw.draw_aline(surf, [center[0]-normal_vector.x,center[1]-normal_vector.y], [center[0]+normal_vector.x,center[1]+normal_vector.y], color, width)
        
    @staticmethod
    def draw_circle(

        surface: pygame.Surface,
        pos: list[int],
        radius: int,
        color: list | str | Color = "gray",
        width: int = 0,
        outline: typing.Tuple[list | str | Color, int] = None,
        centering: bool = False,
    ) -> None:
        if isinstance(color, Color):
            color = color.rgb
        pygame.draw.circle(surface, color, pos, radius, width)
        if centering:
            pos = [pos[0] + radius, pos[1] + radius]

        if outline is not None:
            Draw.__outline(
                outline[0], outline[1], "circle", surface, pos=pos, radius=radius
            )

    @staticmethod
    def draw_polygone(

        surface: pygame.Surface,
        points: list[list[int]],
        color: list | str | Color = "gray",
        width: int = 0,
        outline: typing.Tuple[list | str | Color, int] = None,
    ) -> None:
        if isinstance(color, Color):
            color = color.rgb
        pygame.draw.polygon(surface, color, points, width)

        if outline is not None:
            Draw.__outline(outline[0], outline[1], "polygone", surface, points=points)

    @staticmethod
    def draw_line(

        surface: pygame.Surface,
        point_1: list | tuple | Vector2,
        point_2: list | tuple | Vector2,
        color: list | str | Color = "gray",
        width: int = 1,
    ) -> None:
        if isinstance(color, Color):
            color = color.rgb
        if isinstance(point_1, Vector2):
            pos1 = point_1.xy
        elif isinstance(point_1, (list, tuple)):
            pos1 = point_1
        if isinstance(point_2, Vector2):
            pos2 = point_2.xy
        elif isinstance(point_2, (list, tuple)):
            pos2 = point_2
        pygame.draw.line(surface, color, pos1, pos2, width)

    @staticmethod
    def draw_vector_line(
        surface: pygame.Surface,
        pos: list | tuple | Vector2,
        vector: Vector2,
        color: list | str | Color = 'gray',
        width: int = 1
    ):
        start_pos = pos
        end_pos = posing(start_pos, vector.x, vector.y)
        
        left_vector = copy(vector)
        right_vector = copy(vector)
        left_vector.normalyze()
        right_vector.normalyze()
        left_vector*=(18+width)
        right_vector*=(18+width)
        left_vector.rotate(150)
        right_vector.rotate(-150)
        Draw.draw_aline(surface, start_pos, end_pos, color, width)
        Draw.draw_aline(surface, end_pos, [end_pos[0]+right_vector.x, end_pos[1]+right_vector.y], color, width)
        Draw.draw_aline(surface, end_pos, [end_pos[0]+left_vector.x, end_pos[1]+left_vector.y], color, width)
        
    @staticmethod
    def draw_aline(

        surface: pygame.Surface,
        point_1: list | tuple | Vector2,
        point_2: list | tuple | Vector2,
        color: list | str | Color = 'gray',
        width = 2,
        circled: bool = True

    ) -> None:
        if isinstance(color, Color):
            color = color.rgb
        if isinstance(point_1, Vector2):
            pos1 = point_1.xy
        elif isinstance(point_1, (list, tuple)):
            pos1 = point_1
        if isinstance(point_2, Vector2):
            pos2 = point_2.xy
        elif isinstance(point_2, (list, tuple)):
            pos2 = point_2
            
        vector_normal = Vector2([pos1[0]-pos2[0]+0.00001,pos1[1]-pos2[1]])
        vector_normal.normalyze()
        poses = []
        
        vector_left = copy(vector_normal)
        vector_left.rotate(90)
        vector_left*=width/2
        poses.append([pos1[0]+vector_left.x, pos1[1]+vector_left.y])
        poses.append([pos2[0]+vector_left.x, pos2[1]+vector_left.y])
        
        vector_right = copy(vector_normal)
        vector_right.rotate(-90)
        vector_right*=width/2
        poses.append([pos2[0]+vector_right.x, pos2[1]+vector_right.y])
        poses.append([pos1[0]+vector_right.x, pos1[1]+vector_right.y])
        
        
        
        
        
        
        
        Draw.draw_polygone(surface, poses, color)
        if circled:
            Draw.draw_circle(surface, pos1, width/2, color)
            Draw.draw_circle(surface, pos2, width/2, color)
    
    @staticmethod
    def draw_dashed_line(

        surface: pygame.Surface,
        point_1: list | tuple | Vector2,
        point_2: list | tuple | Vector2,
        color: list | str | Color = "gray",
        width: int = 1,
        dash_size: int = 10,
    ) -> None:
        if isinstance(color, Color):
            color = color.rgb
        if isinstance(point_1, Vector2):
            pos1 = point_1.xy
        elif isinstance(point_1, (list, tuple)):
            pos1 = point_1
        if isinstance(point_2, Vector2):
            pos2 = point_2.xy
        elif isinstance(point_2, (list, tuple)):
            pos2 = point_2
        vector = Vector2(pos1[0] - pos2[0], pos1[1] - pos2[1])
        lenght = vector.lenght
        vector.normalyze()
        vector *= dash_size
        delta_pos = pos1
        for i in range(int(lenght // dash_size)):
            delta_pos = [pos1[0] - vector.x, pos1[1] - vector.y]
            if i % 2 == 0:
                Draw.draw_line(surface, pos1, delta_pos, color, width)
            pos1 = delta_pos

    @staticmethod
    def draw_dashed_hline(

        surface: pygame.Surface,
        point_1: list | tuple | Vector2,
        point_2: list | tuple | Vector2,
        color: list | str | Color = "gray",
        width: int = 1,
        dash_size: int = 10,
    ) -> None:
        if isinstance(color, Color):
            color = color.rgb
        if isinstance(point_1, Vector2):
            pos1 = point_1.xy
        elif isinstance(point_1, (list, tuple)):
            pos1 = point_1
        if isinstance(point_2, Vector2):
            pos2 = point_2.xy
        elif isinstance(point_2, (list, tuple)):
            pos2 = point_2
        vector = Vector2(pos1[0] - pos2[0], pos1[1] - pos2[1])
        lenght = vector.lenght
        vector.normalyze()
        vector *= dash_size
        delta_pos = pos1
        for i in range(int(lenght // dash_size)):
            delta_pos = [pos1[0] - vector.x, pos1[1] - vector.y]
            if i % 2 == 0:
                Draw.draw_hline(surface, pos1[1], pos1[0], delta_pos[0], width, color)
            pos1 = delta_pos

    @staticmethod
    def draw_dashed_vline(

        surface: pygame.Surface,
        point_1: list | tuple | Vector2,
        point_2: list | tuple | Vector2,
        color: list | str | Color = "gray",
        width: int = 1,
        dash_size: int = 10,
    ) -> None:
        if isinstance(color, Color):
            color = color.rgb
        if isinstance(point_1, Vector2):
            pos1 = point_1.xy
        elif isinstance(point_1, (list, tuple)):
            pos1 = point_1
        if isinstance(point_2, Vector2):
            pos2 = point_2.xy
        elif isinstance(point_2, (list, tuple)):
            pos2 = point_2
        vector = Vector2(pos1[0] - pos2[0], pos1[1] - pos2[1])
        lenght = vector.lenght
        vector.normalyze()
        vector *= dash_size
        delta_pos = pos1
        for i in range(int(lenght // dash_size)):
            delta_pos = [pos1[0] - vector.x, pos1[1] - vector.y]
            if i % 2 == 0:
                Draw.draw_vline(surface, pos1[0], pos1[1], delta_pos[1], width, color)
            pos1 = delta_pos

    @staticmethod
    def draw_lines(

        surface: pygame.Surface,
        points: Tuple[Tuple[float, float], ...],
        color: Tuple[int, int, int] | str | Color,
        width: int,
        closed: bool = False,
        blend: int = 1,
    ):
        if isinstance(color, Color):
            color = color.rgb
        for i in range(width):
            for j in range(width):
                points_ = list(
                    map(
                        lambda elem: [
                            elem[0] + i - width // 2,
                            elem[1] + j - width // 2,
                        ],
                        points,
                    )
                )
                pygame.draw.aalines(surface, color, closed, points_, blend)

    @staticmethod
    def draw_alines(
        surface: pygame.Surface,
        points: Tuple[Tuple[float, float], ...],
        color: Tuple[int, int, int] | str | Color,
        width: int,
        closed: bool = False,
    ):
        if isinstance(color, Color):
            color = color.rgb
        
        
        for i in range(len(points)):
                if closed:
                    Draw.draw_aline(surface, points[i-1], points[i], color, width)
                else:
                    if i-1>=0:
                        Draw.draw_aline(surface, points[i-1], points[i], color, width)

    @staticmethod
    def draw_join_line(
        surface: pygame.Surface, 
        point_1: list | tuple | Vector2,
        point_2: list | tuple | Vector2,
        color: list | str | Color = "gray",
        join_width: int = 10,
        join_steps: int = 10,
        width: int = 1,
    ):
        if isinstance(color, Color):
            color = color.rgb
        if isinstance(point_1, Vector2):
            pos1 = point_1.xy
        elif isinstance(point_1, (list, tuple)):
            pos1 = point_1
        if isinstance(point_2, Vector2):
            pos2 = point_2.xy
        elif isinstance(point_2, (list, tuple)):
            pos2 = point_2
        
        lenght = distance(point_1, point_2)
        
        vector_speed = Vector2(
            pos1[0]-pos2[0],
            pos1[1]-pos2[1]
        )
        vector_speed.normalyze()
        vector_speed*=(lenght/ join_steps)
        
        
        vector_joining = copy(vector_speed)
        vector_joining.normalyze()
        vector_joining*=join_width
        vector_joining.rotate(90)
        points = []
        
        for i in range(join_steps):
            points.append(copy(pos2))
            pos2[0]+=vector_speed.x
            pos2[1]+=vector_speed.y
            
            pos2[0]+=vector_joining.x
            pos2[1]+=vector_joining.y
            if i%2==0:
                vector_joining*=-1
        points.append(pos2)
            
            
        
        
            
        Draw.draw_lines(surface, points, color, width)
            
    @staticmethod
    def draw_vline(

        surface: pygame.Surface,
        x: int,
        y1: int,
        y2: int,
        width: int = 1,
        color: list | str | Color = (100, 100, 100),
    ) -> None:
        if isinstance(color, Color):
            color = color.rgb
        for i in range(width):
            gfxdraw.vline(surface, int(x - int(width / 2) + i), int(y1), int(y2), color)

    @staticmethod
    def draw_hline(

        surface: pygame.Surface,
        y: int,
        x1: int,
        x2: int,
        width: int = 1,
        color: list | str | Color = (100, 100, 100),
    ) -> None:
        if isinstance(color, Color):
            color = color.rgb
        for i in range(width):
            gfxdraw.hline(surface, int(x1), int(x2), int(y - int(width / 2) + i), color)

    @staticmethod
    def draw_bezier(

        surface: pygame.Surface,
        points: Tuple[Tuple[float, float], ...],
        steps: int = 2,
        color: Tuple[int, int, int] | str | Color = (100, 100, 100),
        width: int = 1,
    ):
        if isinstance(color, Color):
            color = color.rgb
        for i in range(width):
            for j in range(width):
                points_ = list(
                    map(
                        lambda elem: [
                            elem[0] + i - width // 2,
                            elem[1] + j - width // 2,
                        ],
                        points,
                    )
                )
                gfxdraw.bezier(surface, points_, steps, color)

    @staticmethod
    def draw_rect_fast(

        surface: pygame.Surface,
        pos: list[int],
        size: list[int],
        color: list | str | Color = "gray",
    ):
        if len(size) == 1:
            size = [size[0], size[0]]
        if isinstance(color, Color):
            color = color.rgb
        rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
        gfxdraw.rectangle(surface, rect, color)

    @staticmethod
    def draw_dashed_lines(
        surface: pygame.Surface,
        points: list,
        color: list | str | Color = "gray",
        width: int = 1,
        dash_size: int = 10,
    ):
        for i in range(len(points)):
            if i + 1 < len(points):
                Draw.draw_dashed_line(
                    surface, points[i], points[i + 1], color, width, dash_size
                )

    @staticmethod
    def draw_arc(
        surface: pygame.Surface,
        center_pos: list,
        color: list | str | Color = "gray",
        start_angle: int = 0,
        stop_angle: int = 175,
        radius: int = 100,
        width: int = 50,
        step: int = 20,
        outline_width: int = 0,
    ):
        if isinstance(color, Color):
            color = color.rgb
        if width != 1:
            stop_angle = stop_angle % 361
            toch = step
            ang_step = (start_angle - stop_angle) / toch
            width = min(radius, width)

            start_pos = [
                center_pos[0] + sin(math.radians(start_angle)) * (radius - width),
                center_pos[1] + cos(math.radians(start_angle)) * (radius - width),
            ]
            poses = []
            poses.append(start_pos)

            for i in range(toch + 1):
                x = center_pos[0] + sin(math.radians(start_angle)) * radius
                y = center_pos[1] + cos(math.radians(start_angle)) * radius
                start_angle += ang_step

                poses.append([x, y])
            start_angle -= ang_step
            for i in range(toch):
                x = center_pos[0] + sin(math.radians(start_angle)) * (radius - width)
                y = center_pos[1] + cos(math.radians(start_angle)) * (radius - width)
                start_angle -= ang_step

                poses.append([x, y])

            Draw.draw_polygone(surface, poses, color, outline_width)
        else:
            pygame.draw.arc(
                surface,
                color,
                [
                    center_pos[0] - radius,
                    center_pos[1] - radius,
                    radius * 2,
                    radius * 2,
                ],
                math.radians(start_angle + 90),
                math.radians(stop_angle + 90),
            )

    @classmethod
    def draw_shapes(
        self, 
        surface: pygame.Surface,
        shapes: Tuple[callable, ...],
        pos: list | Vector2
    ):
        shapes_functions = [shape[0].__name__ for shape in shapes]
        shapes_kvargs = [shape[1] for shape in shapes]
        
        for i in range(len(shapes_functions)):
            shapes_kvargs[i]['pos'][0]+=pos[0]
            shapes_kvargs[i]['pos'][1]+=pos[1]
            Draw.__dict__[shapes_functions[i]].__call__(surface=surface, **shapes_kvargs[i])

    
# base draw class -------------------------------

# base input class ------------------------------

mouse__wheel = 0

class Mouse:
    left = "_left"
    right = "_right"
    middle = "_middle"
    press_event = '_press'
    click_event = '_click'

    end_pos = [0, 0]
    pressed = False
    def __init__(self, bt, type, id = None) -> None:
        self.bt = bt
        self.type = type
        if id is None:
            self.id = random.randint(0,999999999999)
        else:
            self.id = id
        self.pressed = False

    @classmethod
    @property
    def whell(self):
        global mouse__wheel
        return mouse__wheel

    @classmethod
    @property
    def pos(self) -> list[int, int]:
        return [*pygame.mouse.get_pos()]

    @classmethod
    def position(self) -> list[int, int]:
        return [*pygame.mouse.get_pos()]

    def set_position(self, pos: typing.Tuple[int, int]) -> None:
        pygame.mouse.set_pos(pos)

    @classmethod
    def set_hide(self):
        pygame.mouse.set_visible(False)

    @classmethod
    def set_show(self):
        pygame.mouse.set_visible(True)

    def press(self, button: str = left):
        if button == Mouse.left:
            return pygame.mouse.get_pressed()[0]
        if button == Mouse.middle:
            return pygame.mouse.get_pressed()[1]
        if button == Mouse.right:
            return pygame.mouse.get_pressed()[2]

    def click(self, button: str = left):
        p = self.press(button)
        if p:
            if not self.pressed:
                self.pressed = True
                return True
            else:
                return False
        if not self.press(button):
            self.pressed = False
            return False

    @classmethod
    @property
    def speed(self) -> typing.Tuple[int, int]:
        return pygame.mouse.get_rel()

    @classmethod
    def set_cursor(self, cursor: Any) -> None:
        pygame.mouse.set_cursor(cursor)

class MouseEventHandler:
    def __init__(self) -> None:
        self.events: Tuple[Mouse, ...] = []
        self.events_outputs = []
    
    def AddEvent(self, mouse_event: Mouse):
        self.events.append(mouse_event)
        
    def GetEventById(self, id) -> Tuple[bool, ...]:
        for event in self.events_outputs:
            if event[1] == id:
                return event[0]
        
    def EventsUpdate(self):
        self.events_outputs = []
        for event in self.events:
            if event.type == Mouse.click_event:
                self.events_outputs.append([event.click(event.bt), event.id])
            if event.type == Mouse.press_event:
                self.events_outputs.append([event.press(event.bt), event.id])
            
class Keyboard:
    def key_pressed(key):
        return keyboard.is_pressed(key)

    def key_pressed_win(key):
        akt = pygame.mouse.get_focused()
        if akt:
            return keyboard.is_pressed(key)
        else:
            return False

# base input class ------------------------------

# physicks --------------------------------------

IDS = 0

class Colliders:
    CTYPE_RECT = 'Rect'
    CTYPE_CIRCLE = 'circle'
    GRAVITY = Vector2(0,0.5)
    
    class CRect(Rect):
        def __init__(self, start_pos_: Tuple[float, float],
                    start_size_: Tuple[float, float],
                    start_speed_: Vector2 = Vector2(0,0),
                    statick: bool = True,
                    bounsing: Vector2 = Vector2(0,0),
                    trenie: Vector2 = Vector2(0.9,0.9),
                    colliding_down: bool = True,
                    colliding_up: bool = True) -> None:
            global IDS
            super().__init__(start_pos_[0],start_pos_[1], start_size_[0], start_size_[1])
            self._speed = start_speed_
            self._statick = statick
            self._trenie = trenie
            self._colliding_down = colliding_down
            self._colliding_up = colliding_up
            
            
            
            
            self._bounsing = bounsing
            self._type = Colliders.CTYPE_RECT
            
            self._collide = {
                'up':False,
                'down':False,
                'left':False,
                'right':False
            }
            self._id = IDS
            IDS+=1
            
        @property
        def statick(self) -> bool: return self._statick
        
        @property
        def id(self) -> int: return self._id
        
        @property
        def type(self) -> str: return self._type
        
        def set_defauld_collides(self):
            self._collide = {
                'up':False,
                'down':False,
                'left':False,
                'right':False
            }
        
        def get_collides(self):
            return self._collide
        
    class CCircle(Circle):
        def __init__(self, start_pos_: Tuple[float, float], start_radius_: Tuple[float, float], start_speed_: Vector2 = Vector2(0,0), statick: bool = True, bounsing: float = 0.9) -> None:
            global IDS
            super().__init__(start_pos_, start_radius_)
            self.xy = start_pos_
            self._radius = start_radius_
            self._speed = start_speed_
            self._statick = statick
            
            self._bounsing = bounsing
            self._type = Colliders.CTYPE_CIRCLE
            self._id = IDS
            IDS+=1
            
        @property
        def statick(self) -> bool: return self._statick
        
        @property
        def id(self) -> int: return self._id
        
        @property
        def type(self) -> str: return self._type
        
    def __init__(self, surf):
        self._space:Tuple[Colliders.CRect, ...] = []
        self._surf = surf
        self.render_all_colliders = False
        self.render_all_speeds = False
        self.render_all_staticks = False
        self.text = Text('arial',20,'None','red',True)
        

        
    def add(self, collider: [CRect, CCircle]):
        self._space.append(collider)
        
    def __simulate_gravity__(self, collider):
        collider._speed += Colliders.GRAVITY
        
    def __simulate_collider_pos_x__(self, collider):
        collider.x += collider._speed.x
        
    def __simulate_collider_pos_y__(self, collider):
        
        collider.y += collider._speed.y
        
    def __collide_all_objects__(self, collider):
        collide_objs = []
        for j, collider2 in enumerate( self._space ):
            if collider.id != collider2.id:
                if collider2.type == Colliders.CTYPE_RECT:
                    if collider.collide_rect(collider2):
                        collide_objs.append(collider2)
        
        return collide_objs
    
    def __simulate_attach_y__(self, collider: CRect , collide_objects: Tuple[CRect, ...]) -> None:
        for collider_a in collide_objects:
            if collider_a.statick:
                collider._speed.x*=collider_a._trenie.x
                if collider_a._colliding_down:
                    if collider._speed.y>0:
                        collider.y_down = collider_a.y_up
                        collider._speed.y*=-collider._bounsing.y
                        collider._collide['down'] = True
                        break
                        
                    elif collider._speed.y<=0 :
                        collider.y_up = collider_a.y_down
                        collider._speed.y*=-collider._bounsing.y  
                        collider._collide['up'] = True
                        break
                    
                else:
                    
                    if collider._speed.y > 0:
                        
                        collider.y_down = collider_a.y_up
                        collider._speed.y*=-collider._bounsing.y
                        collider._collide['down'] = True
                        break
            
            
                
    def __simulate_attach_x__(self, collider: CRect , collide_objects: Tuple[CRect, ...]) -> None:
        for collider_a in collide_objects:
            if collider_a.statick and collider.wh == collider.end_size:
                
                if collider_a._colliding_down:
                    collider._speed.y*=collider_a._trenie.y
                    if collider._speed.x>0:
                        collider.x_right = collider_a.x_left
                        collider._speed.x*=-collider._bounsing.x
                        collider._collide['right'] = True
                        break
                        
                    elif collider._speed.x<=0:
                        collider.x_left = collider_a.x_right
                        collider._speed.x*=-collider._bounsing.x 
                        collider._collide['left'] = True
                        break
                
            
            
            
                    
    @NewProcess()
    def printing(self):
        while True:
            sleep(0.5)
            print('-'*20)
            for c in self._space:
                print(c.id, c._speed)
        
    def update(self):
        for i, collider in enumerate(self._space):
            collider.set_defauld_collides()

            if self.render_all_colliders:
                collider.draw(self._surf)
                #self.text.draw(self._surf, collider.center, True, 'id: '+str(collider.id), 'gray')
            if self.render_all_staticks:
                if collider.statick:
                    collider.draw(self._surf)
            
            if self.render_all_speeds:
                Draw.draw_line(self._surf, collider.xy, [collider.x+collider._speed.x, collider.y+collider._speed.y], 'blue', 3)
            
            #collider._speed.x = round(collider._speed.x, 4)
            #collider._speed.y = round(collider._speed.y, 4)
            if abs(collider._speed.y)<0.01:
                collider._speed.y = 0
            
            
                
            if not collider.statick:
                self.__simulate_collider_pos_y__(collider)
                
                collider._speed.y+=Colliders.GRAVITY.y
                
                collide_objects = self.__collide_all_objects__(collider)
            
                self.__simulate_attach_y__(collider, collide_objects)
            
            if not collider.statick:
                self.__simulate_collider_pos_x__(collider)
                
                collider._speed.x+=Colliders.GRAVITY.x
                
                collide_objects = self.__collide_all_objects__(collider)
            
                self.__simulate_attach_x__(collider, collide_objects)
            
            collider.UDT()
                
        self._space = list(filter(lambda elem: elem.w>1 and elem.h>1, self._space))
        
class Camera:
    def __init__(self) -> None:
        self.sx = 0
        self.sy = 0
        
    def simulate(self, target_pos, player_pos, delta = 0.5):
        self.sx = (target_pos[0]-player_pos[0])*delta
        self.sy = (target_pos[1]-player_pos[1])*delta
                

# physicks --------------------------------------

class DataLoader:
    def __file_test__(self, file_name_: str) -> bool:
        if file_name_.split('.')[1] == 'data':
            return True
        return False
    
    def strokes_with_file(self, file_name_: str) -> list[str]:
        file = open(file_name_)
        strokes = file.readlines()
        return strokes
    
    def get_stroke_block_type(self, stroke_: str):
        open_index = stroke_.index('[')
        close_index = stroke_.index(']')
        return stroke_[open_index+2:close_index-1]
    
    def finde_with_stroke_var_name_and_file(self, stroke_: str):
        equal_index = stroke_.index('=')
        var_name = stroke_[:equal_index-1]
        file_name = stroke_[equal_index+2:-1]
        
        return var_name, file_name
        
    def replace_new_lines(self, strokes_: list[str]) -> list[str]:
        new_strings = []
        for stroke in strokes_:
            new_strings.append(stroke.replace('\n',' '))
        return new_strings
    
    def generate_data_tree(self, strokes_: list[str]) -> list:
        data_types = [
            'tilesheats',
            'sprites',
            'animations'
        ]
        
        datas = {
            'tilesheats':[],
            'sprites':[],
            'animations':[]
        }
        
        data_write_opened = False
        data_block_type = None
        
        strokes_ = self.replace_new_lines(strokes_)
        
        strokes = []
        for stroke in strokes_:
            if stroke!=' ':
                strokes.append(stroke)
                
        
        for i, stroke in enumerate( strokes ):
            if stroke[0] == '>':
                data_write_opened = False
            
            if data_write_opened:
                if stroke != '' and stroke != ' ' and stroke != '\n':
                    if data_block_type == data_types[0]:
                        var_name, d = self.finde_with_stroke_var_name_and_file(stroke)
                        
                        strings = d.split(' ')
                        file = strings[0][1:-1]
                        tile_size = int(strings[1])
                        tiles_count = int(strings[2])
                        data = [file, tile_size, tiles_count]
                        
                        print(f'Tileshet {var_name} loaded!')
                        datas[data_block_type].append([var_name, data])
                        
                    if data_block_type == data_types[1]:
                        var_name, d = self.finde_with_stroke_var_name_and_file(stroke)
                        
                        strings = d.split(' ')
                        file = strings[0][1:-1]
                        tr = int(strings[1])
                        rb = int(strings[2])
                        data = [file, tr, rb]
                        
                        print(f'Sprite {var_name} loaded!')
                        datas[data_block_type].append([var_name, data])
                
            if stroke[0] == '<':
                data_block_type = self.get_stroke_block_type(stroke)
                if data_block_type in data_types:
                    data_write_opened = True
                
        return datas
        
    def generate_objects_for_data_tree(self, data_tree_: dict):
        data_types = [
            'tilesheats',
            'sprites',
            'animations'
        ]
        
        datas = {}
        
        for object_type in data_tree_:
            objects = data_tree_[object_type]
            
            for obj in objects:
                if object_type == data_types[0]:
                    data = TileSheat(obj[1][0], [obj[1][1],obj[1][1]], obj[1][2])
                    data.create()
                    datas[obj[0]] = data
                if object_type == data_types[1]:
                    data = Sprite(obj[1][0], obj[1][1], obj[1][2])
                    datas[obj[0]] = data
                    
        return datas
    
    def generate_objects_for_data_tree_tile_sheats(self, data_tree_: dict):
        data_types = [
            'tilesheats',
        ]
        
        datas = {}
        
        for object_type in data_tree_:
            objects = data_tree_[object_type]
            
            for obj in objects:
                if object_type == data_types[0]:
                    data = TileSheat(obj[1][0], [obj[1][1],obj[1][1]], obj[1][2])
                    data.create()
                    datas[obj[0]] = data
                    
        return datas
                
    def Load_from_file(self, file_name_: str):
        '''
        {name}.data file config
        
        <[ sprites ]
        
        {sprite_name} = '{file_name}' {rotate_buffer} {0}
        
        >[ sprites ]
        
        <[ tilesheats ]
        
        {tilesheat_name} = '{file_name}' {tile_size} {tiles_count}
        
        >[ tilesheats ]
        
        '''
        
        if self.__file_test__(file_name_):
            
            file = self.strokes_with_file(file_name_)
            data_tree = self.generate_data_tree(file)
            return self.generate_objects_for_data_tree(data_tree)
            
    def Load_from_file_tilesheats(self, file_name_: str):
        '''
        {name}.data file config
        
        <[ tilesheats ]
        
        {tilesheat_name} = '{file_name}' {tile_size} {tiles_count}
        
        >[ tilesheats ]
        
        '''
        
        if self.__file_test__(file_name_):
            
            file = self.strokes_with_file(file_name_)
            data_tree = self.generate_data_tree(file)
            return self.generate_objects_for_data_tree_tile_sheats(data_tree)
            
#DataLoader().Load_from_file(r'api\test.data')
            
            



