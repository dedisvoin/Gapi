from .lib import *
from libtypes import *


from typing import overload
from typing import Tuple







class Path:
    def __init__(self, points: Tuple[Tuple[int,int],...]=None, start_point_index: int = 0, speed: float = 1, looped: bool = True, normalize: bool = True, normilize_step: float = 10) -> "Path":
        self._points = points
        self._start_point_index = start_point_index
        self._speed = speed
        self._looped = looped
        self._normilize = normalize
        self._normilize_step = normilize_step
        
        if self._points is not None:
            self._pos = copy(points[self._start_point_index])
            if self._normilize: self.path_normilize()
        
        self._stooped = False
        self.normal_vector = None
        
    def path_normilize(self):
        for _ in range(1000):
            for i in range(len(self._points)):
                if distance(self._points[i],self._points[i-1])<self._normilize_step:
                    del self._points[i]
                    break

        
    
    def set_path(self, points:  Tuple[Tuple[int,int],...]):
        del self._points
        self._points = copy(points)
        self._pos = copy(points[self._start_point_index])
        if self._normilize: self.path_normilize()
        
    def pathing(self,delta):
        if not self._stooped:
            speed = Vector2(
                self._pos[0]-self._points[self._start_point_index+1][0],
                self._pos[1]-self._points[self._start_point_index+1][1]
            )
            speed.x+=0.000001
            speed.normalyze()
            speed*=self._speed
        
            self._pos[0] -= speed.x*delta
            self._pos[1] -= speed.y*delta
            
            if abs(self._pos[0]-self._points[self._start_point_index+1][0])<self._speed and abs(self._pos[1]-self._points[self._start_point_index+1][1])<self._speed:
                self._start_point_index+=1
                self._pos = copy(self._points[ self._start_point_index])
        
        self.normal_vector = Vector2(
            self._pos[0]-self._points[self._start_point_index][0],
            self._pos[1]-self._points[self._start_point_index][1],
        )
        if self.normal_vector.lenght != 0:
            self.normal_vector.x+=0.00001
            self.normal_vector.normalyze()
            self.normal_vector*=200
        else:
            self.normal_vector = Vector2(
                -(self._points[self._start_point_index-1][0]-self._points[self._start_point_index][0]),
                -(self._points[self._start_point_index-1][1]-self._points[self._start_point_index][1]),
            )
            self.normal_vector.x+=0.00001
            self.normal_vector.normalyze()
            self.normal_vector*=200

        
        if self._start_point_index+1 == len(self._points):
            if self._looped:
                self._start_point_index=-1
            else:
                self._stooped = True

            
    def view(self, win):
        if len(self._points)>1:
            Draw.draw_lines(win, self._points, (255,0,0),1,self._looped)
            