from pygame import init, display
from pygame.sprite import Group, LayeredDirty
from aglib import State
from aglib.sprite import *

class Screen(object):
    def __init__(self, name):
        State.name = name
        State.screen = self
        State.controls = State.screens[State.name]['controls']
        State.groups = {}
        self.layers = LayeredDirty()
        self.add_all()
        State.save(State.name)

    def add_all(self):
        for name in State.screens[State.name]['objects']:
            self.add_object(name, None)

    def add_object(self, name, pos):
        obj = State.objects[name]
        if pos:
            obj['pos'] = pos
        group = obj['group']
        if group not in State.groups:
            State.groups[group] = Group()
        sprite = eval(group.capitalize())(obj)
        State.groups[group].add(sprite)
        if obj['cursor']:
            State.cursor = sprite
        self.layers.add(State.groups[group])

    def draw(self):
        self.layers.update()
        State.dirty = self.layers.draw(State.window)
        display.update(State.dirty)

    def switch(self, name):
        State.save(State.name)
        State.prev_name = State.name
        State.restore(name)

    def restore(self):
        State.pressed = []
        for group in State.groups:
            for sprite in State.groups[group]:
                sprite.dirty = 1
                sprite.stopped = True
