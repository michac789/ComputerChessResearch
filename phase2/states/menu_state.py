import pygame
from states.base_state import BaseState


class MenuState(BaseState):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._button_options = ['Single Player', '2 Players', 'Quit Game']
        self._button_dict = {}
        self._button_hover = [False for _ in range(3)]
    
    def get_event(self, event):
        super().get_event(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self._button_dict[0].collidepoint(self.mouse_pos):
                self.change_state = 'play'
            elif self._button_dict[1].collidepoint(self.mouse_pos):
                self.change_state = 'play'
            elif self._button_dict[2].collidepoint(self.mouse_pos):
                self.change_state = 'quit'
        for i in range(len(self._button_dict)):
            self._button_hover[i] = False
            if self._button_dict[i].collidepoint(self.mouse_pos):
                self._button_hover[i] = True

    def draw(self, screen):
        screen.fill(pygame.Color('lightblue'))
        title_text = self.large_font.render('MY FIRST CHESS AI', True, pygame.Color('purple'))
        screen.blit(title_text, (80, 30))
        
        BUTTON_WIDTH = self.params['screen_width'] * (1 / 2)
        BUTTON_HEIGHT = self.params['screen_height'] * (1 / 5)
        START_X = (self.params['screen_width'] - BUTTON_WIDTH) // 2
        for i, option in enumerate(self._button_options):
            START_Y = 120 + i * (BUTTON_HEIGHT + 10)
            button_rect = pygame.Rect(START_X, START_Y, BUTTON_WIDTH, BUTTON_HEIGHT)
            button_text = self.medium_font.render(option, True,
                (pygame.Color('black') if not self._button_hover[i] else pygame.Color('magenta')))
            self._button_dict[i] = button_rect
            button_text_rect = button_text.get_rect()
            button_text_rect.center = button_rect.center
            pygame.draw.rect(screen, pygame.Color('yellow'), button_rect)
            screen.blit(button_text, button_text_rect)
