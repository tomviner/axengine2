from os import path
from json import JSONDecoder
from pygame import font, image, Rect, Surface
from pygame.locals import RLEACCEL

__doc__ = """Various utility functions."""

aglib_dir = path.abspath(path.dirname(__file__))
aglib_data = path.normpath(path.join(aglib_dir, 'data'))

def get_path(type, name):
    """Get the path to a resource file, given its type and name."""

    if type in ('cfg', 'screen', 'object'): ext = '.json'
    if type == 'image': ext = '.png'
    elif type == 'font': ext = '.ttf'
    return path.join(aglib_data, type, name + ext)

def decode_data(data):
    """Decode the data of a JSON object into a Python dictionary."""

    file = open(data).read()
    return JSONDecoder().decode(file)

def load_object(name):
    """Load a game object and recursively set its inherited attributes.

    If a game object has a 'template' attribute set, it automatically inherits
    the attributes of this parent object. Those attributes can be redefined in
    the child object to override them.

    This process is recursive, which leads to minimize redundant metadata.

    Returns a new dictionary of the modified game object."""

    data = decode_data(name)
    if 'template' in data:
        tmp = get_path('object', data['template'])
        obj = load_object(tmp)
        for x in obj:
            if x not in data:
                data[x] = obj[x]
    return data

def load_cfg(name):
    """Load a game configuration resource."""

    file = get_path('cfg', name)
    return load_object(file)

def load_screen(name):
    """Load a screen configuration resource."""

    return load_object(name)

def load_text(name):
    """Load a text game object."""

    return load_object(name)

def load_font(data):
    """Load a text game object's specified font file and return the rendered
        surface."""

    file = get_path('font', data['text_font'])
    return font.Font(file, data['text_size'])

def load_image(file):
    """Load an image resource and return its surface."""

    return image.load(file)


class Cache(dict):
    """A cache is a collection of game resources with special tricks to aid in
        resource loading.

    A cache is actually a modified Python dictionary. Accessing a game object
    is as simple as:
    objects = Cache('objects')
    player = objects['char_player']

    The cache does a couple of things to help us:
    * It allows us to access metadata of any type of game object easily with
        builtin Python dictionary methods.
    * It ensures each object is read from disk and loaded only once."""

    def __init__(self, type):
        self.type = type
    def __getitem__(self, name):
        item = get_path(self.type, name)
        if name not in self:
            self[name] = eval('load_' + self.type)(item)
        return super(Cache, self).__getitem__(name)


class Spritesheet(object):
    """A spitesheet manages a sprite image, which contain multiple
        sub-images."""

    def __init__(self, file):
        self.sheet = file
    def image(self, rect, colorkey=None, alpha=False):
        rect = Rect(rect)
        if alpha: image = Surface(rect.size).convert_alpha()
        else: image = Surface(rect.size).convert()
        image.blit(self.sheet, (0,0), rect)
        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, RLEACCEL)
        return image
    def images(self, rects, colorkey=None):
        imgs = []
        for rect in rects:
            imgs.append(self.image(rect, colorkey))
        return imgs
