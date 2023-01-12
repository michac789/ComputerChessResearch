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
    
    def get_event(self, event):
        self.mouse_pos = pygame.mouse.get_pos()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.change_state = 'quit'
    
    def update(self, dt):
        self.time_elapsed += dt
    
    def draw(self, screen):
        screen.fill(pygame.Color('black'))


class MenuState(BaseState):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._options = ['Single Player', '2 Players', 'Quit Game']
        self.button_dict = {}
    
    def get_event(self, event):
        super().get_event(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.button_dict[0].collidepoint(self.mouse_pos):
                self.change_state = 'play_ai'
            elif self.button_dict[1].collidepoint(self.mouse_pos):
                self.change_state = 'play_2p'
            elif self.button_dict[2].collidepoint(self.mouse_pos):
                self.change_state = 'quit'

    def draw(self, screen):
        screen.fill(pygame.Color('lightblue'))
        title_text = self.large_font.render('MY FIRST CHESS AI', True, pygame.Color('purple'))
        screen.blit(title_text, (80, 30))
        BUTTON_WIDTH = self.params['screen_width'] * (1 / 2)
        BUTTON_HEIGHT = self.params['screen_height'] * (1 / 5)
        START_X = (self.params['screen_width'] - BUTTON_WIDTH) // 2
        for i, option in enumerate(self._options):
            START_Y = 120 + i * (BUTTON_HEIGHT + 10)
            button_rect = pygame.Rect(START_X, START_Y, BUTTON_WIDTH, BUTTON_HEIGHT)
            button_text = self.medium_font.render(option, True, pygame.Color('black'))
            self.button_dict[i] = button_rect
            button_text_rect = button_text.get_rect()
            button_text_rect.center = button_rect.center
            pygame.draw.rect(screen, pygame.Color('yellow'), button_rect)
            screen.blit(button_text, button_text_rect)
