import pygame, os
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
        self._generate_quads()
    
    def _generate_quads(self):
        self.sprite_sheet = {}
        SPRITE_SHEET_PATH = os.path.join('assets', 'chess_sprite_sheet.png')
        img = pygame.image.load(SPRITE_SHEET_PATH)
        img = pygame.transform.scale(img, (self._tile_size * 6, self._tile_size * 2))
        t = self._tile_size
        for i in range(2):
            for j in range(6):
                self.sprite_sheet[i * 6 + j] = (t * j, t * i, t, t)
                # surf = pygame.Surface((self._tile_size, self._tile_size))
                # surf.blit(img, (0, 0), (0, 0, self._tile_size, self._tile_size))
                

    
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
        

        PIC = os.path.join('assets', 'chess_sprite_sheet.png')
        PIC = pygame.image.load(PIC)
        img = pygame.transform.scale(PIC, (self._tile_size * 6, self._tile_size * 2))

        surf = pygame.Surface((100, 100))
        surf.blit(img, (0, 0), self.sprite_sheet[2])

        screen.blit(surf, (500, 100))



        # sprites = {}
        # for i in range(2):
        #     for j in range(6):
        #         x = x
