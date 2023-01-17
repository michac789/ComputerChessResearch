from states.state_machine import Game
from states.menu_state import MenuState
from states.play2p_state import Play2PState
from states.playai_state import PlayAIState
import sys


states = {
    'menu': lambda **kw: MenuState(**kw),
    'play2p': lambda **kw: Play2PState(**kw),
    'playai': lambda **kw: PlayAIState(**kw),
    'quit': lambda **_: sys.exit(),
}
game = Game(states, 'menu')
game.run()
