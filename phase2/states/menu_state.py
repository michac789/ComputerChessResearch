import pygame
from states.base_state import BaseState
from states.mixins import ButtonsMixin


class MenuState(ButtonsMixin, BaseState):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._initialize_buttons(['Single Player', '2 Players', 'Quit Game'])
    
    def get_event(self, event):
        super().get_event(event)
        self._get_event_buttons(event, callbacks={
            0: lambda: self._change_state_callback('play'),
            1: lambda: self._change_state_callback('play'),
            2: lambda: self._change_state_callback('quit'),
        })
    
    def _display_buttons(self, screen):
        BUTTON_WIDTH = self.params['screen_width'] * (1 / 2)
        BUTTON_HEIGHT = self.params['screen_height'] * (1 / 5)
        START_X = (self.params['screen_width'] - BUTTON_WIDTH) // 2
        for i, option in enumerate(self._button_options):
            START_Y = 120 + i * (BUTTON_HEIGHT + 10)
            self._create_button_util(i, option, screen, START_X, START_Y,
                BUTTON_WIDTH, BUTTON_HEIGHT, self.medium_font)

    def draw(self, screen):
        screen.fill(pygame.Color('lightblue'))
        title_text = self.large_font.render('MY FIRST CHESS AI', True, pygame.Color('purple'))
        screen.blit(title_text, (80, 30))
        self._display_buttons(screen)
