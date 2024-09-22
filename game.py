import pygame
from background import Background
from players import Player
from coin import Coin
from meteorite import Meteorite
class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.player1 = Player('sprites/cohete1.png',600)
        self.player2 = Player('sprites/cohete2.png',200)
        self.collision_count_p1 = 0  # Contador de colisiones para el jugador 1
        self.collision_count_p2 = 0  # Contador de colisiones para el jugador 2
        # grupo de sprites
        self.coins = pygame.sprite.Group()
        self.meteorites = pygame.sprite.Group()
        self.font = pygame.font.Font(None, 36)  # Fuente por defecto, tamaño 36
        self.start_time = pygame.time.get_ticks()  # Guardar el tiempo de inicio del juego

        # Crear meteoritos
        for _ in range(2):
            meteorite = Meteorite()
            self.meteorites.add(meteorite)
        # Crear monedas
        for _ in range(3):
            coin = Coin()
            self.coins.add(coin)
        # Fondo 
        self.background = Background() 

    # Loop principal 
    def loop(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.handle_input()
            self.update()
            self.draw()
            # Se detendrá el juego si uno de los jugadores llega a 100 o si ambos pierden todas sus vidas
            if (self.player1.score == 100 or self.player2.score == 100 or (self.collision_count_p1 == 3 and self.collision_count_p2 == 3)):
                print('Ingresando al menú de finalización')
                self.end_screen()
                running = False  # detiene el bucle del juego


            self.clock.tick(60)
    
    # Controla las teclas para players 
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

    #Actualiza todos los sprites 
    def update(self):
        
        self.background.update()  # Actualiza el fondo
        self.player1.update()
        self.player2.update()
        # Actualizamos posiciones de los sprites 
        
        self.meteorites.update()
        self.coins.update()

        # Verificar colisiones si es que no llegan a 100 y aun no se le acaba las vida (maximo 3 choques)
        if self.player1.score <100 and self.collision_count_p1<3:
            self.check_collisions(self.player1, 1)

        if self.player2.score <100 and self.collision_count_p2<3:
            self.check_collisions(self.player2, 2)

    def check_collisions(self, player, player_num):

        # Colisiones entre meteoritos y player
        collisions = pygame.sprite.spritecollide(player, self.meteorites, False)
        if collisions:
            for meteorite in collisions:
                meteorite.reset_position()
            if player_num == 1:
                self.collision_count_p1 += 1
                print(f"Colisiones Jugador 1: {self.collision_count_p1}")
            else:
                self.collision_count_p2 += 1
                print(f"Colisiones Jugador 2: {self.collision_count_p2}")
        
        #colisiones entre monedas y player
        collisions = pygame.sprite.spritecollide(player, self.coins, False)
        if collisions:
            for coin in collisions:
                coin.reset_position()
            if player_num == 1:
                self.player1.update_score()
            else:
                self.player2.update_score()

    def draw(self):
        # Dibuja el fondo
        self.background.draw(self.screen)

        #Dibuja los sprites si tienen puntaje menor a 100 y si aun tienen vidas 
        if(self.player1.score < 100 and self.collision_count_p1<3): 
            self.screen.blit(self.player1.image, self.player1.rect)
        if(self.player2.score < 100 and self.collision_count_p2<3):
            self.screen.blit(self.player2.image, self.player2.rect)

        self.meteorites.draw(self.screen) # distinto porque es un grupo de sprites 
        self.coins.draw(self.screen)
        
        # Mostrar contadores de colisiones
        text_p1 = self.font.render(f"Score: {self.player1.score}", True, (255, 255, 255))
        text_p2 = self.font.render(f"Score: {self.player2.score}", True, (255, 255, 255))
        self.screen.blit(text_p1, (10, 10))
        self.screen.blit(text_p2, (10, 40))

        self.display_time()
        pygame.display.flip()

    def display_time(self):
        # Restamos el tiempo actual menos el tiempo de inicio del juego 
        current_time = pygame.time.get_ticks() - self.start_time
        seconds = current_time // 1000
        time_text = self.font.render(f"Tiempo: {seconds} s", True, (255, 255, 255))
        self.screen.blit(time_text, (10, 70))


    # Creacion del menu

    def main_menu(self):
        runing = True
        while runing:
            self.draw_menu()
                            
    def draw_menu(self): 
        pygame.display.set_caption("Menú de Juego")
        # Cargar la imagen de fondo
        background_image = pygame.image.load("sprites/fondo.png")
        self.screen.blit(background_image, (0, 0))

        # Cargando las imágenese
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

    def end_screen(self):
        print('Ingreso')
        running = True
        while running:
            # Dibujar la pantalla de finalización
            self.draw_end_screen()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Botón izquierdo del ratón
                        mouse_pos = pygame.mouse.get_pos()
                        if self.button_rect_restart.collidepoint(mouse_pos):
                            running = False  # Salir de la pantalla de finalización y reiniciar el juego
                        if self.button_rect_menu.collidepoint(mouse_pos):
                            running = False  # Salir de la pantalla de finalización y regresar al menú

            pygame.display.flip()

    
    def draw_end_screen(self):
        # Fondo de la pantalla de finalización
        background_image = pygame.image.load("sprites/fondo.png")
        self.screen.blit(background_image, (0, 0))

        # Dibujar los botones de reiniciar y volver al menú
        button_restart = pygame.image.load("sprites/boton_off.png")
        button_menu = pygame.image.load("sprites/boton_menu.png")

        self.button_rect_restart = button_restart.get_rect()
        self.button_rect_restart.topleft = (300, 250)
        self.button_rect_menu = button_menu.get_rect()
        self.button_rect_menu.topleft = (300, 350)

        # Mostrar los botones en la pantalla
        self.screen.blit(button_restart, self.button_rect_restart.topleft)
        self.screen.blit(button_menu, self.button_rect_menu.topleft)

        # Título de "Game Over" o similar
        font = pygame.font.Font(None, 74)
        game_over_text = font.render("¡Juego Terminado!", True, (255, 255, 255))
        self.screen.blit(game_over_text, (200, 150))

        pygame.display.flip()
