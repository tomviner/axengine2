#!/usr/bin/python2
import aglib

# Create the game engine using the 'demo' game configuration.
game = aglib.Engine('demo')

# The demo game contains a 'title' and 'world' screen. The default world screen
# has a map and a player object. Here, we will modify the world screen and add
# a few instances of a monster object, each starting in a random location.
game.add_object('world', 'char_monster', 20, 'random')

# Run the engine starting at the 'title' screen.
game.run('title')
