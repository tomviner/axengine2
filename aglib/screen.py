from random import randint
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
        """Add all the objects specified in the screen's configuration
            resource to their proper sprite groups for rendering."""

        for obj in State.screens[State.name]['objects']:
            self.add_object(obj)

    def add_object(self, name, amount=1, pos=None):
        """Add one or many of a single game object resource to the screen.

        name:   the name of the game object.
        amount: the amount of instances to add.
        pos:    if value is 'random', every object will start in a random
                location.
                if value is a (x,y) tuple, every object will start at that
                screen location."""

        obj = State.objects[name]
        new_pos = None
        for i in range(0, amount):
            if pos == 'random':
                scr = State.window.get_size()
                spr = obj['size']
                new_pos = (randint(0, scr[0]/spr[0]), randint(0, scr[1]/spr[1]))
            elif type(pos) == type(tuple()):
                new_pos = pos
            if new_pos:
                obj['pos'] = new_pos
            group = obj['group']
            if group not in State.groups:
                State.groups[group] = Group()
            sprite = eval(group.capitalize())(obj)
            State.groups[group].add(sprite)
        if obj['cursor']:
            State.cursor = sprite
        if obj['joystick']:
            State.joystick = sprite
        self.layers.add(State.groups[group])

    def draw(self):
        """Run the update method of every sprite, keeping track of which ones
            are dirty and need updating, and then finally updating only the
            dirty areas."""

        self.layers.update()
        State.dirty = self.layers.draw(State.window)
        display.update(State.dirty)

    def switch(self, name):
        """Switch to a new screen by saving the current state, and then
            restoring the specified state."""

        State.save(State.name)
        State.prev_name = State.name
        State.restore(name)

    def restore(self):
        """Called when a screen is restored from a saved state."""

        State.pressed = []
        for group in State.groups:
            for sprite in State.groups[group]:
                sprite.dirty = 1
                sprite.stopped = True

