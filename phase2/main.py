from states.state_machine import Game
from states.menu_state import MenuState


states = {
    'menu': lambda **kw: MenuState(**kw),
}
game = Game(states, 'menu')
game.run()
