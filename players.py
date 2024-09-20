import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('sprites/cohete.png')
        self.rect = self.image.get_rect()
        self.rect.centerx = 400
        self.rect.bottom = 600

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def update(self):
        # Puedes agregar lógica adicional para el jugador si es necesario
        pass
