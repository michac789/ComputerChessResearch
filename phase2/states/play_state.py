import pygame


class MenuState:
    def __init__(self, *args, **kwargs):
        self.font = pygame.font.Font(None, 24)

    def exit(self):
        pass

    def update(self, dt):
        self.t += dt

    def draw(self, screen):
        screen.fill(pygame.Color("blue"))
        text_render = self.font.render('CHESS 2', True, pygame.Color('red'))
        screen.blit(text_render, (0, 0))
        pygame.draw.rect(screen, pygame.Color("blue"), pygame.Rect((50, 50), (100, 120)))
