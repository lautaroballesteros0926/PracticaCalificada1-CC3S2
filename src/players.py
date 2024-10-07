import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self,image_path,position):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.centerx = position         #coordenada del eje x del centro de la imagen 
        self.rect.bottom = 600
        self.score = 0

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
        
        # Limitar el movimiento dentro de los bordes de la pantalla (800x600)
        if self.rect.left < 0:
            self.rect.left = 0  # No permitir que se salga por la izquierda
        if self.rect.right > 800:
            self.rect.right = 800  # No permitir que se salga por la derecha
            
    def update_score(self): 
        self.score=self.score+20 