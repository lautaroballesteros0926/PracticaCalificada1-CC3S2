import pygame
import random

class Meteorite(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('sprites/meteorito.png')
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, 800)
        self.rect.y = random.randint(-100, -40)
        self.speed = random.randint(2, 6)

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 600:
            self.reset_position()

    def reset_position(self):
        self.rect.x = random.randint(0, 800)
        self.rect.y = random.randint(-100, -40)
