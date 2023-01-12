import pygame
from states.base_state import BaseState


class PlayState(BaseState):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._dim_height = 8
        self._dim_width = 8
        self._board_padding = self.params['screen_height'] / 30
        self._board_width = self.params['screen_width'] * (9 / 16) - (2 * self._board_padding)
        self._board_height = self.params['screen_height'] - (2 * self._board_padding)
        self._tile_size = int(min(self._board_width / self._dim_width, self._board_height / self._dim_height))
        self._board_start = (self._board_padding, self._board_padding)
    
    def get_event(self, event):
        super().get_event(event)

    def draw(self, screen):
        screen.fill(pygame.Color((255, 153, 102)))
        tiles = []
        for i in range(self._dim_height):
            row_tiles = []
            for j in range(self._dim_width):
                rect = pygame.Rect(
                    self._board_start[0] + j * self._tile_size,
                    self._board_start[1] + i * self._tile_size,
                    self._tile_size, self._tile_size
                )
                col = pygame.Color('white') if (i + j) % 2 == 0 else pygame.Color('grey')
                pygame.draw.rect(screen, col, rect)
                pygame.draw.rect(screen, pygame.Color('black'), rect, 1)
                row_tiles.append(rect)
            tiles.append(row_tiles)
