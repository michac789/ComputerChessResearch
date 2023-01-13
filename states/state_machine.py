import sys, pygame


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450

class Game:
    '''
    Initialize pygame screen, states, and current starting state.
    States are stored in dictionary 'states', keys represent the
    name of the state, values are callback to the state object.
    It is done so like this to preserve memory and load seperate
    state objects depending on current state.
    '''
    def __init__(self, states: dict[str: callable], start_state: str):
        pygame.init()
        self.screen = pygame.display.set_mode(
            (SCREEN_WIDTH, SCREEN_HEIGHT),
            # pygame.RESIZABLE
        )
        self.clock = pygame.time.Clock()
        self.states = states
        self.state = self.states[start_state](**{
            'screen_width': SCREEN_WIDTH,
            'screen_height': SCREEN_HEIGHT
        })
    
    '''
    Main game loop, for every frame (dt), call these methods
    in this order from current game state object:
    - 'get_event': check for inputs for every pygame event per frame
    - 'update': pass in dt, make relevant changes to game state
    - 'draw': pass screen surface, update changes visually
    - change state to 'change_state' attribute if not None
    '''
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
    
    '''
    Called when 'change_state' attribute is not None.
    Change current state to 'change_state', pass a dictionary
    (return value from 'exit' method) to the next state as kwargs.
    '''
    def change_state(self):
        new_state = self.state.change_state
        if new_state not in self.states:
            raise Exception('invalid state!')
        self.state = self.states[new_state](**self.state.exit())
