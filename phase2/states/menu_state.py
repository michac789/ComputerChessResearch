import pygame


class BaseState:
    def __init__(self, *args, **kwargs):
        # self._font = 
        pass


class MenuState:
    def __init__(self, *args, **kwargs):
        self.font = pygame.font.Font(None, 48)
        self.t = 0
        self.options = ['Single Player', '2 Players', 'Quit Game']
        self.x = 1

    def exit(self):
        pass

    def get_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            self.x = 3
        pass

    def update(self, dt):
        mouse = pygame.mouse.get_pos()
        # left, _, _ = pygame.mouse.get_pressed()
        # if left == 1:
        #     self.x = 2
        self.t += dt

    def draw(self, screen):
        screen.fill(pygame.Color("green"))
        text_render = self.font.render(f'CHESS {self.t} {self.x}', True, pygame.Color('red'))
        screen.blit(text_render, (0, 0))
        pygame.draw.rect(screen, pygame.Color("blue"), pygame.Rect((50, 50), (100, 120)))
