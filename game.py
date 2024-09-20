import pygame
from background import Background
from meteorite import Meteorite
from players import Player

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.background = Background()
        self.player = Player()
        self.meteorites = pygame.sprite.Group()
	# Crear meteoritos
        for _ in range(10):  # Generar 10 meteoritos
            meteorite = Meteorite()
            self.meteorites.add(meteorite)


    def loop(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.handle_input()
            self.update()
            self.draw()

            self.clock.tick(60)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player.move(-5, 0)
        if keys[pygame.K_RIGHT]:
            self.player.move(5, 0)

    def update(self):
        self.meteorites.update()
        self.player.update()

    def draw(self):
        self.screen.blit(self.background.image, self.background.rect)
        self.screen.blit(self.player.image, self.player.rect)
        self.meteorites.draw(self.screen)
        pygame.display.flip()
