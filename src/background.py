import pygame

class Background:
    def __init__(self):
        self.image = pygame.image.load('sprites/Imagen_fondo.png')
        self.rect1 = self.image.get_rect(topleft=(0, 0))  # Primera imagen
        self.rect2 = self.image.get_rect(topleft=(0, self.rect1.height))  # Segunda imagen

    def update(self):
        # Mueve ambos rectángulos hacia abajo
        self.rect1.y += 1
        self.rect2.y += 1

        # Reposiciona si sale de la pantalla
        if self.rect1.top >= pygame.display.get_surface().get_height():
            self.rect1.y = self.rect2.top - self.rect1.height  # Coloca encima de la segunda imagen
        if self.rect2.top >= pygame.display.get_surface().get_height():
            self.rect2.y = self.rect1.top - self.rect2.height  # Coloca encima de la primera imagen

    def draw(self, surface):
        # Dibuja ambas imágenes de fondo
        surface.blit(self.image, self.rect1)
        surface.blit(self.image, self.rect2)
