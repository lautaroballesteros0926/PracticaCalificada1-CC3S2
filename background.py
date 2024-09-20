import pygame

class Background(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('sprites/Imagen_fondo.png')
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)
