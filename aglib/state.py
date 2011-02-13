from aglib import util

__doc__ = """An object store for convenient access to game objects."""

# These are the default attributes that will be saved/restored and persist
# across state changes.
default_attrs = [
    'name',
    'objects',
    'cursor',
    'joystick',
    'groups',
    'screen',
    'controls',
]

# A dictionary of state names and their attributes.
states = {}

class State(object):
    """A state gives global access to game objects. Any attribute can be
        manually modified after running restore() on the desired state. Running
        save() on the modified file will keep the changes when leaving and
        returning to the state later.

    attributes
    images:     a cache of image resources.
    objects:    a cache of game object resources.
    screens:    a cache of screen configuration resources.
    name:       the name of the state.
    prev_name:  the name of the previous state.
    cursor:     the sprite which has been marked as the cursor.
    joysick:    the sprite which can be controlled by a joystick
    screen:     the screen to draw to for the current state.
    groups:     a dictionary of the current sprite groups.
    controls:   the input controls for the current state, as specified in each
                screen's configuration resource.
    pressed:    a list of input keys currently being pressed down."""

    images = util.Cache('image')
    objects = util.Cache('object')
    screens = util.Cache('screen')
    name = None
    prev_name = None
    cursor = None
    joystick = None
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
