import pygame, os
from states.base_state import BaseState
from chess.chess_board import ChessBoard
from chess.chess_constants import MAPPING


class PlayState(BaseState):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._initialize_board_sizes()
        self._initialize_buttons()
        self._generate_quads()
        self._cb = ChessBoard()
        self._cb.initialize_board()
        self._tiles = []
        self._hovered_tiles = [[False for _ in range(8)] for _ in range(8)]
        self._selected_tile = None
        self._allowed_tiles = [[False for _ in range(8)] for _ in range(8)]
    
    def _initialize_board_sizes(self):
        self._dim_height = 8
        self._dim_width = 8
        self._board_padding = self.params['screen_height'] / 30
        self._board_width = self.params['screen_width'] * (9 / 16) - (2 * self._board_padding)
        self._board_height = self.params['screen_height'] - (2 * self._board_padding)
        self._tile_size = int(min(self._board_width / self._dim_width, self._board_height / self._dim_height))
        self._board_start = (self._board_padding, self._board_padding)
    
    def _initialize_buttons(self):
        self._button_options = ['Reset Board', 'Main Menu']
        self._button_dict = {}
        self._button_hover = [False for _ in range(3)]
    
    def _generate_quads(self):
        self._sprite_sheet = {}
        SPRITE_SHEET_PATH = os.path.join('assets', 'chess_sprite_sheet.png')
        img = pygame.image.load(SPRITE_SHEET_PATH)
        self._img = pygame.transform.scale(img, (self._tile_size * 6, self._tile_size * 2))
        t = self._tile_size
        for i in range(2):
            for j in range(6):
                self._sprite_sheet[i * 6 + j + 1] = (t * j, t * i, t, t)
    
    def _get_event_board(self, event):
        self._hovered_tiles = [[False for _ in range(8)] for _ in range(8)]
        for i in range(self._dim_height):
            for j in range(self._dim_width):
                if self._tiles[i][j].collidepoint(self.mouse_pos):
                    self._hovered_tiles[i][j] = True
                    if event.type == pygame.MOUSEBUTTONDOWN and self._cb.allow_select_tile(i, j):
                        if self._selected_tile == (i, j):
                            self._selected_tile = None
                            self._allowed_tiles = [[False for _ in range(8)] for _ in range(8)]
                        else:
                            self._selected_tile = (i, j)
                            self._allowed_tiles = self._cb.get_valid_moves_list(i, j)
                    elif event.type == pygame.MOUSEBUTTONDOWN and self._allowed_tiles[i][j]:
                        self._cb.move_piece(*self._selected_tile, i, j)
                        self._selected_tile = None
                        self._allowed_tiles = [[False for _ in range(8)] for _ in range(8)]
    
    def _get_event_buttons(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self._button_dict[0].collidepoint(self.mouse_pos):
                self._cb.initialize_board()
            elif self._button_dict[1].collidepoint(self.mouse_pos):
                self.change_state = 'menu'
        for i in range(len(self._button_dict)):
            self._button_hover[i] = False
            if self._button_dict[i].collidepoint(self.mouse_pos):
                self._button_hover[i] = True

    def get_event(self, event):
        super().get_event(event)
        self._get_event_board(event)
        self._get_event_buttons(event)
    
    def _draw_chess_board(self, screen):
        self._tiles = []
        for i in range(self._dim_height):
            row_tiles = []
            for j in range(self._dim_width):
                start_x = self._board_start[0] + j * self._tile_size
                start_y = self._board_start[1] + i * self._tile_size
                rect = pygame.Rect(start_x, start_y, self._tile_size, self._tile_size)
                col = (
                    pygame.Color('green') if self._allowed_tiles[i][j] else
                    pygame.Color('yellow') if (i, j) == self._selected_tile else
                    pygame.Color('lightblue') if self._cb.allow_select_tile(i, j) and self._hovered_tiles[i][j] else
                    pygame.Color('white') if (i + j) % 2 == 0 else pygame.Color('grey')
                )
                pygame.draw.rect(screen, col, rect)
                pygame.draw.rect(screen, pygame.Color('black'), rect, 1)
                sprite_key = MAPPING[str(self._cb.board[i][j])]
                if sprite_key != -1:
                    screen.blit(self._img, (start_x, start_y), self._sprite_sheet[sprite_key])
                row_tiles.append(rect)
            self._tiles.append(row_tiles)
    
    def _display_buttons(self, screen):
        BUTTON_WIDTH = self.params['screen_width'] * (1 / 5)
        BUTTON_HEIGHT = self.params['screen_height'] * (1 / 8)
        START_X = (self.params['screen_width'] - BUTTON_WIDTH) * (11 / 16)
        START_Y = (self.params['screen_height'] - BUTTON_HEIGHT) * (9 / 10)
        for i, option in enumerate(self._button_options):
            START_X = START_X + i * BUTTON_WIDTH * 1.1
            button_rect = pygame.Rect(START_X, START_Y, BUTTON_WIDTH, BUTTON_HEIGHT)
            button_text = self.small_font.render(option, True,
                (pygame.Color('black') if not self._button_hover[i] else pygame.Color('magenta')))
            self._button_dict[i] = button_rect
            button_text_rect = button_text.get_rect()
            button_text_rect.center = button_rect.center
            pygame.draw.rect(screen, pygame.Color('yellow'), button_rect)
            screen.blit(button_text, button_text_rect)
        
    def draw(self, screen):
        screen.fill(pygame.Color((255, 153, 102)))
        self._draw_chess_board(screen)
        self._display_buttons(screen)
