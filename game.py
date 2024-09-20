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

    # Creacion del menu

    def main_menu(self):
        runing = True
        while runing:
            self.draw_menu()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    runing = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # 1 es el botón izquierdo del ratón
                        # Obtener la posición del clic
                        mouse_pos = pygame.mouse.get_pos()
                        # Verificar si el clic ocurrió dentro del área del botón
                        if self.buttom_rect_start.collidepoint(mouse_pos):
                            # entra al juego directamente
                            self.loop()
                            # cerramos si cierras la ventana en loop
                            runing = False
                            print("¡Botón de inicio clicado!")
                        if self.buttom_rect_off.collidepoint(mouse_pos):
                            # cerramos la ventana
                            runing = False
                            print("¡Botón de salida clicado!")

    def draw_menu(self): 
        pygame.display.set_caption("Menú de Juego")
        # Colores
        BLACK = (0, 0, 0)
        # Fuentes
        font = pygame.font.Font(None, 74)
        font_small = pygame.font.Font(None, 36)

        # Cargar la imagen de fondo
        background_image = pygame.image.load("sprites/fondo.png")
        self.screen.blit(background_image, (0, 0))

        # Cargando las imágenes
        title_menu = pygame.image.load("sprites/boton_menu.png")
        buttom_start = pygame.image.load("sprites/boton_start.png")
        buttom_off = pygame.image.load("sprites/boton_off.png")

        # Crear un rectángulo a partir de la imagen del botón
        self.buttom_rect_start = buttom_start.get_rect()  # Hacemos self para acceder a este rectángulo desde main_menu
        self.buttom_rect_start.topleft = (330, 270)  # Posición del botón en la pantalla
        self.buttom_rect_off = buttom_off.get_rect()  # Igual para este botón
        self.buttom_rect_off.topleft = (380, 350)

        # Dibujar el texto menú y botones en la pantalla
        self.screen.blit(title_menu, (280, 100))
        self.screen.blit(buttom_start, self.buttom_rect_start.topleft)
        self.screen.blit(buttom_off, self.buttom_rect_off.topleft)

        pygame.display.flip()
