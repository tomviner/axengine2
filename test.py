#!/usr/bin/python2
import aglib

# Load the 'demo' game.
game = aglib.Engine('demo')

# The demo game already adds a map and a player character to the world screen.
# Here we add a bunch of monsters to the world screen.
game.add('world', 'char_monster', 20, 'random')

# Actually run the game starting at the title screen.
game.run('title')
