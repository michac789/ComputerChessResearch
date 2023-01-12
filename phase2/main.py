from states.state_machine import Game
from states.menu_state import MenuState
from states.play_state import PlayState
import sys


states = {
    'menu': lambda **kw: MenuState(**kw),
    'play': lambda **kw: PlayState(**kw),
    'quit': lambda **_: sys.exit(),
}
game = Game(states, 'menu')
game.run()
