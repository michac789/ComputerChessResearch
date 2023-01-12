import sys
import pygame
from states.menu_state import MenuState


class Game:
    def __init__(self, screen, states, start_state):
        pygame.init()
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.states = states
        self.state = self.states[start_state]()
    
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                dt = self.clock.tick()
                self.state.update(dt)
                self.state.draw(self.screen)
                pygame.display.update()


if __name__ == '__main__':
    screen = pygame.display.set_mode((500, 500))
    states = {
        'menu': lambda: MenuState(),
    }
    game = Game(screen, states, 'menu')
    game.run()
