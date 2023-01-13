import pygame


class BaseState:
    def __init__(self, **kwargs):
        self.small_font = pygame.font.Font(None, 24)
        self.medium_font = pygame.font.Font(None, 48)
        self.large_font = pygame.font.Font(None, 96)
        self.change_state = None
        self.mouse_pos = None
        self.time_elapsed = 0
        self.params = kwargs
    
    def exit(self) -> dict:
        return {
            'screen_width': self.params['screen_width'],
            'screen_height': self.params['screen_height'],
        }
    
    def get_event(self, event: pygame.event):
        self.mouse_pos = pygame.mouse.get_pos()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.change_state = 'quit'
    
    def update(self, dt: float):
        self.time_elapsed += dt
    
    def draw(self, screen: pygame.surface):
        screen.fill(pygame.Color('black'))
