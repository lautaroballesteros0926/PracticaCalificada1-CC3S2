import pygame
from background import Background
from meteorite import Meteorite
from players import Player

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.background = Background()
        self.player1 = Player()
        self.player2 = Player()
        self.meteorites = pygame.sprite.Group()
        self.font = pygame.font.Font(None, 36)  # Fuente por defecto, tamaño 36
        self.start_time = pygame.time.get_ticks()  # Guardar el tiempo de inicio del juego
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
            self.player1.move(-5, 0)
        if keys[pygame.K_RIGHT]:
            self.player1.move(5, 0)
        if keys[pygame.K_a]:
            self.player2.move(-5, 0)
        if keys[pygame.K_d]:
            self.player2.move(5, 0)

    def update(self):
        self.meteorites.update()
        self.player1.update()
        self.player2.update()

    def draw(self):
        self.screen.blit(self.background.image, self.background.rect)
        self.screen.blit(self.player1.image, self.player1.rect)
        self.screen.blit(self.player2.image, self.player2.rect)
        self.meteorites.draw(self.screen)
        self.display_time()
        pygame.display.flip()
    
    def display_time(self):
        # Calcular el tiempo en segundos desde que comenzó el juego
        current_time = pygame.time.get_ticks() - self.start_time
        seconds = current_time // 1000  # Convertir a segundos

        # Renderizar el texto con la fuente
        time_text = self.font.render(f"Tiempo: {seconds} s", True, (255, 255, 255))  # Texto en blanco

        # Dibujar el texto en la esquina superior izquierda
        self.screen.blit(time_text, (10, 10))
