import pygame


'''
    TextsMixin provide method to easily add multiple texts on different coordinates.
'''
class TextsMixin:
    def _display_texts(self, surf: pygame.surface, texts: list[tuple[str, type, type, int, int]]):
        for text in texts:
            new_text = text[1].render(text[0], True, text[2])
            surf.blit(new_text, (text[3], text[4]))


'''
    ButtonsMixin provides several methods to efficiently create buttons,
    with hover effects and clicking functionality.
'''
class ButtonsMixin:
    def _initialize_buttons(self, options: list=[]):
        self._button_options = options
        self._button_dict = {}
        self._button_hover = [False for _ in range(len(self._button_options))]
    
    def _change_state_callback(self, state: str):
        self.change_state = state

    def _get_event_buttons(self, event: pygame.event, callbacks: dict[callable] = {}):
        for i in range(len(self._button_dict)):
            self._button_hover[i] = False
            if self._button_dict[i].collidepoint(self.mouse_pos):
                self._button_hover[i] = True
            if event.type == pygame.MOUSEBUTTONDOWN and self._button_dict[i].collidepoint(self.mouse_pos):
                if i in callbacks: callbacks[i]()
    
    def _create_button_util(self, i: int, text: str, surf: pygame.surface,
            s_x: float, s_y: float, w: float, h: float, font: pygame.font,
            antialias: bool=True,
            col_text_hover: pygame.color=pygame.Color('magenta'),
            col_text: pygame.color=pygame.Color('black'),
            col_rect: pygame.color=pygame.Color('yellow')):
        button_rect = pygame.Rect(s_x, s_y, w, h)
        button_text = font.render(text, antialias,
            (col_text if not self._button_hover[i] else col_text_hover))
        self._button_dict[i] = button_rect
        button_text_rect = button_text.get_rect()
        button_text_rect.center = button_rect.center
        pygame.draw.rect(surf, col_rect, button_rect)
        surf.blit(button_text, button_text_rect)
