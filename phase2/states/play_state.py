import pygame
from states.base_state import BaseState


class PlayState(BaseState):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def get_event(self, event):
        super().get_event(event)

    def draw(self, screen):
        screen.fill(pygame.Color('red'))
