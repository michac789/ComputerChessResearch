import sys, pygame


class Game:
    def __init__(self, screen, states, start_state):
        pygame.init()
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.states = states
        self.state = self.states[start_state]()
    
    def run(self):
        while True:
            dt = self.clock.tick()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                self.state.get_event(event)
            self.state.update(dt)
            self.state.draw(self.screen)
            
            pygame.display.update()
