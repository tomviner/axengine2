from pygame import init, display, event, key
from pygame.locals import KEYDOWN, KEYUP, FULLSCREEN
from aglib import util, State, Clock, Screen, actions

class Engine(object):

    def __init__(self, name='demo'):
        init()
        State.game = util.load_cfg(name)
        State.clock = Clock(10, State.game['frame_rate'])
        State.window = display.set_mode(State.game['screen_size'])
        self.create_screens()

    def add(self, screen, object, amount=1, pos=None):
        State.restore(screen)
        State.screen.add_object(object, amount, pos)
        State.save(screen)

    def create_screen(self, name):
        State.screen = Screen(name)
        State.save(name)

    def create_screens(self):
        for s in State.game['screens']:
            self.create_screen(s)

    def show(self, screen):
        State.restore(screen)

    def check_events(self):
        cursor_keys = ("move_up", "move_down", "move_left", "move_right")
        screen_keys = ("quit", "new_game")
        for e in event.get():
            if e.type in (KEYDOWN, KEYUP):
                k = key.name(e.key)
                if k in State.controls:
                    control = getattr(actions, State.controls[k])
                    if e.type == KEYDOWN:
                        State.pressed.append(control)
                        ctrl = State.controls[k]
                        if ctrl in cursor_keys:
                            control(State.cursor)
                        else:
                            control(State.screen)
                    if e.type == KEYUP:
                        if control in State.pressed:
                            del State.pressed[State.pressed.index(control)]
                            actions.move_stop(State.cursor)
                            if State.pressed:
                                State.pressed[-1](State.cursor)

    def run(self, screen):
        State.running = True
        self.show(screen)
        while State.running:
            State.clock.tick()
            if State.clock.update_ready():
                self.check_events()
            if State.clock.frame_ready():
                State.screen.draw()
