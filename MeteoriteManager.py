import pygame
from meteorite import Meteorite

class MeteoriteManager:
    def __init__(self, count):
        self.meteorites = pygame.sprite.Group()
        self.load_meteorites(count)

    def load_meteorites(self, count):
        """Cargar meteoritos en el grupo."""
        for _ in range(count):
            meteorite = Meteorite()
            self.meteorites.add(meteorite)

    def update(self):
        """Actualizar todos los meteoritos."""
        self.meteorites.update()

    def draw(self,screen):
        self.meteorites.draw(screen)
        