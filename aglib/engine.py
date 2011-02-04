from pygame import init, display, event, key, joystick
from pygame.locals import *
from aglib import util, State, Clock, Screen, actions

#
# TJG: Pretty much everything in this game engine is
# done via JSON-serialised objects. It's not entirely
# clear why this should be but it will at least make
# it easier for us to interoperate with Dojos from
# other languages.
#

class Engine(object):
    """An engine provides a top-level game object that can be used to
        initialize a game from the specified game configuration resource"""

    def __init__(self, name='demo'):
        """Initialise pygame and load the parameters for the game indicated
        by the `name` param. Start the clock for the screen's frame rate and
        create a window surface for the game's screen size.

        Create each of the screen objects referenced by the game and store
        their state, ready to show.
        """
        init()
        joystick.init()
        for i in range(joystick.get_count()):
            joystick.Joystick(i).init()

        State.game = util.load_cfg(name)
        State.clock = Clock(10, State.game['frame_rate'])
        State.window = display.set_mode(State.game['screen_size'])

        self._last_joystick_action = None
        self.create_screens()

    def add_object(self, screen, object, amount=1, pos=None):
        """Add one or more instances of an object to a screen."""

        State.restore(screen)
        State.screen.add_object(object, amount, pos)
        State.save(screen)

    def create_screen(self, name):
        """Create a new screen and save it to a state of the same name for
            retrieval."""

        State.screen = Screen(name)
        State.save(name)

    def create_screens(self):
        """Create all of the game screens specified in the game configuration.

        Called when the engine is first initialized."""

        for name in State.game['screens']:
            self.create_screen(name)

    def check_events(self):
        """Input checking."""

        cursor_keys = ("move_up", "move_down", "move_left", "move_right")
        screen_keys = ("quit", "new_game")
        for e in event.get():
            k = ""
            if e.type == JOYAXISMOTION:
                if e.axis == 1:
                    if -1 == round(e.value):
                        _type = "keydown"
                        self._last_joystick_action = k = "up"
                    if 1 == round(e.value):
                        _type = "keydown"
                        self._last_joystick_action = k = "down"
                    if 0 == round(e.value):
                        _type = "keyup"
                        k = self._last_joystick_action
                if e.axis == 0:
                    if -1 == round(e.value):
                        _type = "keydown"
                        self._last_joystick_action = k = "left"
                    if 1 == round(e.value):
                        _type = "keydown"
                        self._last_joystick_action = k = "right"
                    if 0 == round(e.value):
                        _type = "keyup"
                        k = self._last_joystick_action
            elif e.type in (KEYDOWN, KEYUP):
                k = key.name(e.key)
                if e.type == KEYDOWN:
                    _type = "keydown"
                elif e.type == KEYUP:
                    _type = "keyup"


                if k in State.controls:
                if self._last_joystick_action:
                    sprite = State.joystick
                    if _type == "keyup":
                      self._last_joystick_action = None
                else:
                    sprite = State.cursor
                    control = getattr(actions, State.controls[k])
                if _type == "keydown":
                        State.pressed.append(control)
                        ctrl = State.controls[k]
                        if ctrl in cursor_keys:
                        control (sprite)
                        else:
                            control(State.screen)
                if _type == "keyup":
                        if control in State.pressed:
                            del State.pressed[State.pressed.index(control)]
                        actions.move_stop(sprite)
                            if State.pressed:
                            State.pressed[-1](sprite)




    def update(self):
        """Called whenever the game clock determines that game mechanics are
            ready to be updated."""

        self.check_events()

    def draw(self):
        """Called whenever the game clock determines that a frame is ready to
            be drawn."""

        State.screen.draw()

    def run(self, screen):
        """Main game loop."""

        State.running = True
        State.restore(screen)
        while State.running:
            State.clock.tick()
            if State.clock.update_ready():
                self.update()
            if State.clock.frame_ready():
                self.draw()
