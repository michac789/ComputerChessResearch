import sys, pygame


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450

class Game:
    def __init__(self, states, start_state):
        pygame.init()
        self.screen = pygame.display.set_mode(
            (SCREEN_WIDTH, SCREEN_HEIGHT),
            pygame.RESIZABLE
        )
        self.clock = pygame.time.Clock()
        self.states = states
        self.state = self.states[start_state](**{
            'screen_width': SCREEN_WIDTH,
            'screen_height': SCREEN_HEIGHT
        })
    
    def run(self):
        while True:
            dt = self.clock.tick()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                self.state.get_event(event)
            self.state.update(dt)
            self.state.draw(self.screen)
            if self.state.change_state:
                self.change_state()
            pygame.display.update()
    
    def change_state(self):
        new_state = self.state.change_state
        if new_state not in self.states:
            raise Exception('invalid state!')
        self.state = self.states[new_state](**self.state.exit())
