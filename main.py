from states.state_machine import Game
from states.menu_state import MenuState
from states.play_state import PlayState, PlayAIState
import sys


states = {
    'menu': lambda **kw: MenuState(**kw),
    'play': lambda **kw: PlayState(**kw),
    'playai': lambda **kw: PlayAIState(**kw),
    'quit': lambda **_: sys.exit(),
}
game = Game(states, 'menu')
game.run()
