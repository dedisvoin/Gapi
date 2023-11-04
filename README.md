# Gapi
Gapi - оболочка вокруг pygame позволяющая легко и быстро создавать графичексие приложения и игры под пк.
Моя библиотека в разы упращает процесс зоднаия игр.

Вот код для открытия простого окна.

```python
from api.lib import * # Импорт основного модуля из моей библиотеки

win = Window() # Создание обьекта окна

while win(): #Запуск основного цикла приложения
    ...
```
Как видите все намного прощще чем при использовании Pygame.

Теперь расмотрим по подробнее данный код.

```python
win = Window()
```
Окном создается благодаря экземпляру класса ```Window```, при его создании можно указать несколько полезных атрибутов:
```python
size: list[int] = [800, 650] # Размеры создаваемого окна, они не изменяемы.

win_name: str = "Main" # Название окна.

flag: Any = None # Дополнительные флаги, о них я расскажу позже.

cursor: Any = None # Курсор, без изменений - системный курсор.
```
В файле кода можно запустить лишь одно окно, при создании второго экземпляра просто изменится предыдущий, это сделанно во избежание ошибок.

Теперь рассмотрим создание цикла приложения. Он создается при помощи ```While win()```. win - это экземпляр класса окна.
Для создания цикла приложения необходимо вызывать каждую итерацию экземпляр класса окна.

При вызове можно также указать несколько полезных атрибутов.

```python
fps: int = 60 # максимальное количество fps, или же ограничитель фпс.

base_color: str = "white" # Цвет заливки фона. Можно передать любое значение которое можно имплементировать в цвет.

fps_view: bool = True # Счетчик фпс в углу окна.

exit_hot_key: str = "esc" # Горячая Клавиша для закрытия экрана.
```
## Отрисовка примитивов.

Библиотека содержит небольшое количество функций для рисования геометрических фигур любых типов.Все они хранятся в классе Draw. Осмотрим основные.

Для отрисовки фигур необходима поверхность отрисовки ее мы будем брать из экземпляра окна ```win.surf```.

```python
from api.lib import *

win = Window()

while win():
    # Рисование прямоугольника
    Draw.draw_rect(
        surface=win.surf,                         # Поверхность на которой будет происходить отрисовка
        pos=[100, 100],                           # Позиция левого верхнего угла
        size=[300, 200],                          # ширина и высота прямоугольника
        color=Color([200, 100, 130]).rgb,         # цвет прямоугольника
        width=0,                                  # ширина заливки прямоугольника
        radius=-1,                                # радиус закругления углов
        outline=None                              # настройки обводки
    )

    # Рисование окружности
    Draw.draw_circle(
        surface=win.surf,                         # Поверхность на которой будет происходить отрисовка
        pos=[300, 300],                           # Позиция центра
        radius=130,                               # радиус окружности
        color='orange',                           # цвет
        width=40,                                 # ширина заливки
        outline=None                              # настройки обводки
    )

    # Рисование линии
    Draw.draw_line(
        surface=win.surf,                         # Поверхность на которой будет происходить отрисовка
        point_1=[50, 50],                         # Первая точка
        point_2=[200, 400],                       # Вторая точка
        color='green',                            # цвет
        width=4                                   # ширина линии
    )
```

После запуска мы увидим это.

![Снимок экрана 2023-11-04 185710](https://github.com/dedisvoin/Gapi/assets/88434293/74f0134f-fc78-4d51-89c6-1ebb9ab9f418)

С остальными функциями этого класса вы можете познакомится сами.

## Считывание мыши и клавиатуры.

Для того чтобы проверить нажатие какой либо клавиши на клавиатуре необходимо вызвать метод ```key_pressed()``` класса ```Keyboard``` передав интересующую вас клавишу. Если она нажата то функция вернет ```True``` иначе ```False```.

```python
from api.lib import *

win = Window()

while win():
    if Keyboard.key_pressed('w'):
        print('Yes!')
```
Здесь мы проверяем нажатие клавиши ```w``` и при на жатии выводим в консоль Yes!.

