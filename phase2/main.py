import pygame
from states.state_machine import Game
from states.menu_state import MenuState


screen = pygame.display.set_mode((500, 500))
states = {
    'menu': lambda: MenuState(),
}
game = Game(screen, states, 'menu')
game.run()
