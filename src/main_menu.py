import pygame

class MainMenu:
    def __init__(self):
        self.title_menu = pygame.image.load("sprites/boton_menu.png")
        self.buttom_start = pygame.image.load("sprites/boton_start.png")
        self.buttom_off = pygame.image.load("sprites/boton_off.png")
        self.buttom_stats = pygame.image.load("sprites/boton_stats.png")
        
        # Inicializar los rectángulos de los botones
        self.buttom_rect_start = self.buttom_start.get_rect()
        self.buttom_rect_stats = self.buttom_stats.get_rect()
        self.buttom_rect_off = self.buttom_off.get_rect()
        
        self.initialize_button_positions()

    def initialize_button_positions(self):
        self.buttom_rect_start.topleft = (330, 270)  # Posición del botón de inicio
        self.buttom_rect_stats.topleft = (330, 345)  # Posición del botón de estadísticas
        self.buttom_rect_off.topleft = (380, 420)    # Posición del botón de salida

    def draw(self, game):
        pygame.display.set_caption("Menú de Juego")
        
        # Cargar y dibujar la imagen de fondo
        background_image = pygame.image.load("sprites/fondo.png")
        game.screen.blit(background_image, (0, 0))

        # Dibujar el texto menú y botones en la pantalla
        game.screen.blit(self.title_menu, (280, 100))
        game.screen.blit(self.buttom_start, self.buttom_rect_start.topleft)
        game.screen.blit(self.buttom_stats, self.buttom_rect_stats.topleft)
        game.screen.blit(self.buttom_off, self.buttom_rect_off.topleft)
