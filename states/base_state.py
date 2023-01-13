import pygame


class BaseState:
    '''
    Initialize basic fonts and view instance variables.
    For every dt, if 'change_state' is not None, exit current
    state and change to 'change_state' state.
    'self.mouse_pos' store mouse position, to be updated every dt.
    'self.time_elapsed' store time (in sec) since this state started.
    'self.params' store dictionary passed from previous state.
    '''
    def __init__(self, **kwargs):
        self.small_font = pygame.font.Font(None, 24)
        self.medium_font = pygame.font.Font(None, 48)
        self.large_font = pygame.font.Font(None, 96)
        self.change_state = None
        self.mouse_pos = None
        self.time_elapsed = 0
        self.params = kwargs
    
    '''
    Return a dictionary to be passed on to the next state.
    Called when exiting current state.
    '''
    def exit(self) -> dict:
        return {
            'screen_width': self.params['screen_width'],
            'screen_height': self.params['screen_height'],
        }
    
    '''
    Called every dt for every event (inputs) in the game.
    Write logic regarding getting inputs and what variables to change.
    '''
    def get_event(self, event: pygame.event):
        self.mouse_pos = pygame.mouse.get_pos()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.change_state = 'quit'
    
    '''
    Called every dt, update any changes for every dt here.
    '''
    def update(self, dt: float):
        self.time_elapsed += dt
    
    '''
    Called every dt, render stuff on screen here.
    '''
    def draw(self, screen: pygame.surface):
        screen.fill(pygame.Color('black'))
