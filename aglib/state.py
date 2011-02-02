from aglib import util

default_attrs = [
    'name',
    'objects',
    'cursor',
    'groups',
    'screen',
    'controls',
]
states = {}

#
# TJG: This is an very simple in-memory singleton object store:
# only one object at a time can be "active"; the rest are stored
# in state dictionaries keyed by name. Then the whole state is
# stored in the module-global states dictionary.
#

class State(object):
    '''A container for various game objects and data that can be easily
        accessed without unnecessarily passing them around in constructors.'''

    # data resources
    images = util.Cache('image')
    objects = util.Cache('object')
    screens = util.Cache('screen')

    # state attributes that are saved and restored when switching states.
    name = None
    prev_name = None
    cursor = None
    screen = None
    groups = {}
    controls = {}
    pressed = []

    @staticmethod
    def save(name, attrs=default_attrs):
        state_dict = {}
        for attr in attrs:
            if hasattr(State, attr):
                state_dict[attr] = getattr(State, attr)
        states[name] = state_dict

    @staticmethod
    def restore(name, attrs=default_attrs):
        for attr in attrs:
            setattr(State, attr, states[name][attr])
        for attr in attrs:
            obj = getattr(State, attr)
            if hasattr(obj, 'restore'):
                obj.restore()
        State.name = name
