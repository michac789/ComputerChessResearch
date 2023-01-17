import pygame
from states.base_state import BaseState
from states.play2p_state import Play2PState
from chess.chess_ai import get_computer_move


class PlayAIState(Play2PState, BaseState):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._computer_turn = False
        def next_ai_move():
            self._computer_turn = True
            self._marked_tile1 = None
            self._marked_tile2 = None
        self.extra_func = lambda: next_ai_move()

    def _get_event_board(self, event: pygame.event, extra_func: callable=lambda: None):
        if self._computer_turn:
            move = get_computer_move(self._cb)
            self._cb.move_piece(*move)
            self._computer_turn = False
            self._marked_tile1 = (move[0], move[1])
            self._marked_tile2 = (move[2], move[3])
        super()._get_event_board(event, extra_func)

    def get_event(self, event: pygame.event):
        BaseState.get_event(self, event)
        self._get_event_board(event, self.extra_func)
        self._get_event_buttons(event, callbacks={
            0: lambda: self._change_state_callback('playai'),
            1: lambda: self._change_state_callback('menu'),
        })
