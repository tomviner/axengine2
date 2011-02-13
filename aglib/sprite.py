from pygame import Surface
from pygame.sprite import DirtySprite
from aglib import util, State
from aglib.actions import *

class Sprite(DirtySprite):
    def __init__(self):
        DirtySprite.__init__(self)
        if not self.data['group'] == "text":
            self.image = Surface(self.data['size']).convert_alpha()
            self.image.fill(self.data['color'])
        self.rect = self.image.get_rect()
        self.stopped = True
        self.x, self.y = 0, 0
        self.alpha = None
        self.align()

    def align(self):
        size = self.data['size']
        pos = self.data['pos']
        offset = self.data['offset']
        w,h = State.window.get_size()
        if self.data['align'] == "relative":
            if pos == "topleft":
                self.rect.topleft = offset
            elif pos == "top":
                self.rect.centerx = (w/2) + offset[0]
                self.rect.top = offset[1]
            elif pos == "topright":
                self.rect.topright = [ w - offset[0], offset[1] ]
            elif pos == "left":
                self.rect.left = offset[0]
                self.rect.centery = (h/2) + offset[1]
            elif pos == "center":
                self.rect.center = [ (w/2) + offset[0], (h/2) + offset[1] ]
            elif pos == "right":
                self.rect.right = w - offset[0]
                self.rect.centery = (h/2) - offset[1]
            elif pos == "bottomleft":
                self.rect.bottomleft = [ offset[0], h - offset[1] ]
            elif pos == "bottom":
                self.rect.centerx = (w/2) + offset[0]
                self.rect.bottom = h - offset[1]
            elif pos == "bottomright":
                self.rect.bottomright = [ w - offset[0], h - offset[1] ]
        elif self.data['align'] == "tile":
            self.rect.topleft = (
                (pos[0] + offset[0]) * size[0],
                (pos[1] + offset[1]) * size[1])

    def do_actions(self):
        for action in self.data['actions']:
            eval(action)(self)

    def move(self):
        self.dirty = 1
        speed = self.data['speed']
        self.rect.move_ip([self.x * speed, self.y * speed])

    def update(self):
        self.do_actions()
        if not self.stopped:
            self.move()


class AnimatedSprite(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.file = State.images[self.data['image']]
        self.images = {}
        self.sheet = util.Spritesheet(self.file)
        self.count = 0
        self.frame = 0
        self.dir = 0
        self.get_images()

    def get_images(self):
        sw,sh = self.file.get_size()
        tw,th = self.data['size']
        for y in range(0, sh/th):
            self.images[y] = []
            for x in range(0, sw/tw):
                self.images[y].append((x*tw, y*th, tw, th))

    def animate(self):
        self.count = (self.count + 1) % 10
        if not self.count:
            self.frame = (self.frame + 1) % len(self.images[self.dir])
            self.switch_image(self.dir, self.frame)

    def switch_image(self, row, frame):
        self.image = self.sheet.images(self.images[row], self.alpha)[frame]

    def move(self):
        Sprite.move(self)
        self.animate()


class Map(Sprite):
    def __init__(self, obj):
        self.data = obj
        Sprite.__init__(self)
        if "map_tiles" in obj:
            self.create_tiles()

    def create_tiles(self):
        tiles = self.data['map_tiles']
        key = self.data['map_key']
        row, col = 0, 0
        for y in tiles:
            for x in tiles[row]:
                obj = State.objects[key[x]]
                offset = (col * obj['size'][0], row * obj['size'][1])
                tile = Terrain(obj)
                self.image.blit(tile.image, offset)
                col += 1
            col = 0
            row += 1


class Terrain(AnimatedSprite):
    def __init__(self, obj):
        self.data = obj
        AnimatedSprite.__init__(self)
        self.switch_image(0,0)


class Character(AnimatedSprite):
    def __init__(self, obj):
        self.data = obj
        AnimatedSprite.__init__(self)
        self.alpha = -1
        self.switch_image(self.dir, 1)


class Player(Character):
    def __init__(self, obj):
        Character.__init__(self, obj)

class Player2(Character):
    def __init__(self, obj):
        Character.__init__(self, obj)

class Monster(Character):
    def __init__(self, obj):
        Character.__init__(self, obj)


class Text(Sprite):
    def __init__(self, obj):
        self.data = obj
        font = util.load_font(obj)
        self.image = font.render(obj['text_content'], True, obj['color'])
        Sprite.__init__(self)
