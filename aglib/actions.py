from random import choice
from pygame import Rect
from aglib import State

def new_game(screen):
    screen.switch('world')

def quit(screen):
    if State.name == 'title': exit()
    else: screen.switch(State.prev_name)

def help_menu(screen):
    if State.name == 'help_screen':
        screen.switch(State.prev_name)
    else:
        # blank the screen. how?
        screen.switch('help_screen')
    
def setup(screen):
    pass
        
def quit_menu(screen):
    pass

def collide_edge(obj):
    w,h = State.window.get_size()
    obj.rect.clamp_ip(Rect(0, 0, w, h))

def collide_player(obj):
    player_rects = [s.rect for s in State.groups['player']]
    for rect in player_rects:
        if rect.colliderect(obj.rect):
            move_stop(obj)

def move_up(obj):
    obj.stopped = False
    obj.dir = 3
    obj.y = -1

def move_down(obj):
    obj.stopped = False
    obj.dir = 0
    obj.y = 1

def move_left(obj):
    obj.stopped = False
    obj.dir = 1
    obj.x = -1

def move_right(obj):
    obj.stopped = False
    obj.dir = 2
    obj.x = 1

def move_stop(obj):
    obj.dirty = 1
    obj.stopped = True
    obj.x, obj.y = 0, 0

def move_random(obj):
    choices = [ 'stop', 'up', 'down', 'left', 'right' ]
    eval('move_' + choice(choices))(obj)

def menu_up(obj):
    pass

def menu_down(obj):
    pass
