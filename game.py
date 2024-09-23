import pygame
from background import Background
from players import Player
from coin import Coin
from meteorite import Meteorite
#from gamestats import GameStats,Session
#from sqlalchemy import create_engine
#from sqlalchemy.ext.declarative import declarative_base
#from sqlalchemy.orm import sessionmaker
import requests 
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
                self.end_game() #Guarda estadisticas del juego
                self.send_game_data(self.player1.score, self.player2.score, self.winner)
                self.end_screen()
                # Al finalizar el juego
                # Al finalizar el juego               
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



    def end_game(self):
        self.winner = "Jugador 1" if self.player1.score > self.player2.score else "Jugador 2"
        

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
                            self.start_time = pygame.time.get_ticks()  # Guarda el tiempo de inicio del juego 
                            self.loop()
                            # cerramos si cierras la ventana en loop
                            runing = False
                        if self.buttom_rect_off.collidepoint(mouse_pos):
                            # cerramos la ventana
                            runing = False
                        if self.buttom_rect_stats.collidepoint(mouse_pos):
                            self.stats_screen()

                            
    def draw_menu(self): 
        pygame.display.set_caption("Menú de Juego")
        # Cargar la imagen de fondo
        background_image = pygame.image.load("sprites/fondo.png")
        self.screen.blit(background_image, (0, 0))

        # Cargando las imágenese
        title_menu = pygame.image.load("sprites/boton_menu.png")
        buttom_start = pygame.image.load("sprites/boton_start.png")
        buttom_off = pygame.image.load("sprites/boton_off.png")
        buttom_stats = pygame.image.load("sprites/boton_stats.png")

        # Crear un rectángulo a partir de la imagen del botón
        self.buttom_rect_start = buttom_start.get_rect()  # Hacemos self para acceder a este rectángulo desde main_menu
        self.buttom_rect_start.topleft = (330, 270)  # Posición del botón en la pantalla
        self.buttom_rect_stats = buttom_stats.get_rect()
        self.buttom_rect_stats.topleft = (330, 345)  # Posición del botón en la pantalla
        self.buttom_rect_off = buttom_off.get_rect()  # Igual para este botón
        self.buttom_rect_off.topleft = (380, 420)

        # Dibujar el texto menú y botones en la pantalla
        self.screen.blit(title_menu, (280, 100))
        self.screen.blit(buttom_start, self.buttom_rect_start.topleft)
        self.screen.blit(buttom_stats, self.buttom_rect_stats.topleft)
        self.screen.blit(buttom_off, self.buttom_rect_off.topleft)

        pygame.display.flip()

    
            
    def stats_screen(self):
        api_url = "http://localhost:8000/games"
        response = requests.get(api_url)
        games = response.json()

        running = True
        while running:
            self.draw_stats_screen(games)  # Pasar las partidas como argumento
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
            pygame.display.flip()

    def draw_stats_screen(self, games):
        pygame.display.set_caption("Estadísticas")
        
        # Cargar la imagen de fondo
        background_image = pygame.image.load("sprites/fondo_espacial.png")
        self.screen.blit(background_image, (0, 0))
        
        # Configurar la fuente para mostrar el texto en pantalla
        font = pygame.font.Font(None, 36)
        
        # Coordenadas iniciales para imprimir las partidas
        y_offset = 50  # Margen superior
        line_spacing = 40  # Espacio entre cada línea
        
        # Iterar sobre las partidas obtenidas de la API
        for game in games[-5:]:  # Muestra solo las últimas 5 partidas
            player1_score = game['player1_score']
            player2_score = game['player2_score']
            winner = game['winner']
            
            # Texto que se mostrará para cada partida
            game_text = f"Jugador 1: {player1_score} - Jugador 2: {player2_score} - Ganador: {winner}"
            
            # Renderizar el texto
            text_surface = font.render(game_text, True, (255, 255, 255))  # Texto en blanco
            self.screen.blit(text_surface, (50, y_offset))  # Dibujar en la pantalla
            
            # Actualizar el offset para la siguiente línea
            y_offset += line_spacing

        # Actualizar la pantalla de Pygame
        pygame.display.flip()


    
    def end_screen(self):
        print('Ingreso')
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                # Dibujar la pantalla de finalización
                self.draw_end_screen()
                pygame.display.flip()
    
    def draw_end_screen(self):
        # Fondo de la pantalla de finalización
        background_image = pygame.image.load("sprites/fondo.png")
        self.screen.blit(background_image, (0, 0))

        # Dibujar los botones de reiniciar y volver al menú
        button_restart = pygame.image.load("sprites/boton_off.png")
        button_menu = pygame.image.load("sprites/boton_menu.png")

        self.button_rect_restart = button_restart.get_rect()
        self.button_rect_restart.topleft = (300, 500)
        self.button_rect_menu = button_menu.get_rect()
        self.button_rect_menu.topleft = (300, 550)

        # Mostrar los botones en la pantalla
        self.screen.blit(button_restart, self.button_rect_restart.topleft)
        self.screen.blit(button_menu, self.button_rect_menu.topleft)

        # Título de "Game Over" o similar
        font = pygame.font.Font(None, 57)
        game_over_text = font.render("¡Juego Terminado!", True, (255, 255, 255))
        self.screen.blit(game_over_text, (200, 110))

        # Escribir ganador
        font = pygame.font.Font(None, 50)
        if self.player1.score > self.player2.score:
            game_over_text = font.render("Ganó el Jugador 1", True, (255, 255, 255))
            self.screen.blit(game_over_text, (200, 160))
        elif self.player2.score > self.player1.score:
            game_over_text = font.render("Ganó el Jugador 2", True, (255, 255, 255))
            self.screen.blit(game_over_text, (200, 160))

        #Estadisticas
        font = pygame.font.Font(None, 50)
        game_over_text = font.render("Resumen del Juego:", True, (255, 255, 255))
        self.screen.blit(game_over_text, (200, 200))

        #Jugador1
        font = pygame.font.Font(None, 35)
        game_over_text = font.render("Jugador1:", True, (255, 255, 255))
        self.screen.blit(game_over_text, (200, 260))



        #Score jugador 1
        font = pygame.font.Font(None, 28)
        game_over_text = font.render(
            f"Número de colisiones: {self.collision_count_p1}, Score del jugador: {self.player1.score}",
            True,
            (255, 255, 255)
        )
        self.screen.blit(game_over_text, (200, 300))

        #Jugador2
        font = pygame.font.Font(None, 35)
        game_over_text = font.render("Jugador2:", True, (255, 255, 255))
        self.screen.blit(game_over_text, (200, 340))



        #Score jugador 2
        font = pygame.font.Font(None, 28)
        game_over_text = font.render(
            f"Número de colisiones: {self.collision_count_p2}, Score del jugador: {self.player2.score}",
            True,
            (255, 255, 255)
        )
        self.screen.blit(game_over_text, (200, 380))

        pygame.display.flip()

    def send_game_data(self, player1_score, player2_score, winner):
        api_url = "http://localhost:8000/games"
        game_data = {
            "player1_score": player1_score,
            "player2_score": player2_score,
            "winner": winner
        }
        response = requests.post(api_url, json=game_data)
        print(response.json())