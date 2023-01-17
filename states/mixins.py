import pygame


'''
    AtlasMixin provide method to generate quads given an atlas sprite sheet.
'''
class AtlasMixin:
    '''
    From 'path', generate 'n_y' times 'n_x' quads, each of size 'size_y' and 'size_x'.
    Store all the quads in 'self._sprite_sheet' dictionary numbered from 1 to 'n_y' times 'n_x'.
    '''
    def _generate_quads(self, path: str, n_y: int, n_x: int, size_y: int, size_x: int):
        self._sprite_sheet = {}
        img = pygame.image.load(path)
        self._img = pygame.transform.scale(img, (size_x * n_x, size_y * n_y))
        for i in range(n_y):
            for j in range(n_x):
                self._sprite_sheet[i * n_x + j + 1] = (size_x * j, size_y * i, size_x, size_y)


'''
    TextsMixin provide method to easily add multiple texts on different coordinates.
'''
class TextsMixin:
    '''
    Display a list of texts, where each text consist of:
    <text, pygame font, pygame color, x_coordinate, y_coordinate>
    '''
    def _display_texts(self, surf: pygame.surface, texts: list[tuple[str, type, type, int, int]]):
        for text in texts:
            new_text = text[1].render(text[0], True, text[2])
            surf.blit(new_text, (text[3], text[4]))


'''
    ButtonsMixin provides several methods to efficiently create buttons,
    with hover effects and clicking functionality.
'''
class ButtonsMixin:
    '''
    Call this when initializing your state object.
    '_button_options' store list of texts to be displayed.
    '_button_dict' store dict of button to check for collision.
    '_button_hover' keep track of which button is currently hovered.
    '''
    def _initialize_buttons(self, options: list=[]):
        self._button_options = options
        self._button_dict = {}
        self._button_hover = [False for _ in range(len(self._button_options))]
    
    '''
    Utility function to update 'change_state' instance variable.
    '''
    def _change_state_callback(self, state: str):
        self.change_state = state

    '''
    Call this in 'get_event' method, check that for each button:
    When hovered, make change to 'self._button_hover'.
    When clicked, call the callback function from 'callbacks' dict.
    '''
    def _get_event_buttons(self, event: pygame.event, callbacks: dict[callable] = {}):
        for i in range(len(self._button_dict)):
            self._button_hover[i] = False
            if self._button_dict[i].collidepoint(self.mouse_pos):
                self._button_hover[i] = True
            if event.type == pygame.MOUSEBUTTONDOWN and self._button_dict[i].collidepoint(self.mouse_pos):
                if i in callbacks: callbacks[i]()
    
    '''
    Call this in 'draw' method for every button needed.
    Creates rectangle and blit the text on the center of it.
    '''
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
