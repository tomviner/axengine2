from os import path
from json import JSONDecoder
from pygame import font, image, Rect, Surface
from pygame.locals import RLEACCEL

aglib_dir = path.abspath(path.dirname(__file__))
aglib_data = path.normpath(path.join(aglib_dir, 'data'))

def get_path(type, name):
    '''Returns the path to a data resource, given its type and name.'''
    if type in ('game', 'screen', 'object'):
        ext = '.json'
    elif type == 'image': ext = '.png'
    elif type == 'font': ext = '.ttf'
    file = path.join(aglib_data, type, name + ext)
    return file

def decode_data(data):
    '''Open a data resource and decode its JSON into Python.'''
    file = open(data)
    return JSONDecoder().decode(file.read())

def load_game(game):
    file = get_path('game', game)
    return load_object(file)

def load_screen(screen):
    return load_object(screen)

def load_text(text):
    return load_object(text)

def load_font(data):
    file = get_path('font', data['text_font'])
    return font.Font(file, data['text_size'])

def load_image(file):
    return image.load(file)

def load_object(obj):
    '''Load a data resource and recursively set the attributes of its
        children templates.
    Returns a dictionary of object's attributes.'''
    data = decode_data(obj)
    if 'template' in data:
        tmp = get_path('object', data['template'])
        obj = load_object(tmp)
        for x in obj:
            if x not in data:
                data[x] = obj[x]
    return data


class Cache(dict):
    def __init__(self, type):
        self.type = type
    def __getitem__(self, name):
        item = get_path(self.type, name)
        if name not in self:
            self[name] = eval('load_' + self.type)(item)
        return super(Cache, self).__getitem__(name)


class Spritesheet(object):
    def __init__(self, file):
        self.sheet = file
    def image(self, rect, colorkey=None, alpha=False):
        rect = Rect(rect)
        if alpha:
            image = Surface(rect.size).convert_alpha()
        else:
            image = Surface(rect.size).convert()
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
