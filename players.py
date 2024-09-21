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
        
        # Limitar el movimiento dentro de los bordes de la pantalla (800x600)
        if self.rect.left < 0:
            self.rect.left = 0  # No permitir que se salga por la izquierda
        if self.rect.right > 800:
            self.rect.right = 800  # No permitir que se salga por la derecha
        if self.rect.top < 0:
            self.rect.top = 0  # No permitir que se salga por arriba
        if self.rect.bottom > 600:
            self.rect.bottom = 600  # No permitir que se salga por abajo

    def update(self):
        # Puedes agregar lógica adicional para el jugador si es necesario
        pass
