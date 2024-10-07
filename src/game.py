import pygame
from fastapi import Depends
from background import Background
from players import Player
from coin import Coin
from meteorite import Meteorite
import prometheus_client
import requests 

# Nuevas clases 
from event_handler import EventHandler
from main_menu import MainMenu 
from carrera import Carrera
from end_screen import EndScreen

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.player1 = Player('sprites/cohete1.png',600)
        self.player2 = Player('sprites/cohete2.png',200)
        self.collision_count_p1 = 0  # Contador de colisiones para el jugador 1
        self.collision_count_p2 = 0  # Contador de colisiones para el jugador 2

        # Nuevos Objetos 
        self.event_handler = EventHandler()
        self.main_menu = MainMenu()
        self.start_carrera = Carrera()
        self.end_screen = EndScreen()

        # Creamos las variables para mandar las stats al puerto de prometheus
        self.p1_colision = prometheus_client.Counter(
            "colisions_p1",
            "colisiones del jugador 1"
        )
        self.p2_colision = prometheus_client.Counter(
            "colisions_p2",
            "colisiones del jugador 2"
        )
        self.p1_score = prometheus_client.Gauge(
            "score_p1",
            "score del jugador 1"
        )
        self.p2_score = prometheus_client.Gauge(
            "score_p2",
            "score del jugador 2"
        )

        # grupo de sprites
        self.controller = 1
        self.coins = pygame.sprite.Group()
        self.meteorites = pygame.sprite.Group()
        self.font = pygame.font.Font(None, 36)  # Fuente por defecto, tamaño 36
        self.start_time = pygame.time.get_ticks()  # Guardar el tiempo de inicio del juego
        # Crear meteoritos
        for _ in range(2):
            meteorite = Meteorite()
            self.meteorites.add(meteorite) #añadimos meteoritos en el grupo de sprites 
        # Crear monedas
        for _ in range(3):
            coin = Coin()
            self.coins.add(coin)  # añdimos las monedas al grupo de sprites 
        # Fondo 
        self.background = Background() 


    def loop(self):
        running = True
        while running:
            # Primero, procesamos los eventos
            for event in pygame.event.get():
                # Llama al manejador de eventos, pasando `self` (el objeto `Game`)
                running = self.event_handler.handle_event(self, event)
                if not running:
                    break
            # Después de manejar eventos, actualizamos el estado del juego y dibujamos
            if self.controller == 1:  # Menú principal
                self.main_menu.draw(self)
            elif self.controller == 2:  # Carrera
                keys = pygame.key.get_pressed()  # Obtiene las teclas presionadas
                if keys[pygame.K_LEFT]:
                    self.player1.move(-6, 0)  # Mueve el jugador 1 a la izquierda
                if keys[pygame.K_RIGHT]:
                    self.player1.move(6, 0)  # Mueve el jugador 1 a la derecha
                if keys[pygame.K_a]:
                    self.player2.move(-6, 0)  # Mueve el jugador 2 a la izquierda
                if keys[pygame.K_d]:
                    self.player2.move(6, 0) 
                self.start_carrera.draw(self)
                self.start_carrera.update(self)
                if (self.player1.score == 100 or self.player2.score == 100 or (self.collision_count_p1 == 3 and self.collision_count_p2 == 3)):
                    self.controller = 3
            elif self.controller == 3:  # Fin del juego
                self.end_game()  # Determina el ganador
                self.end_screen.draw(self)  # Pantalla final
                self.reset_game()   # Reseteamos
            # Finalmente, actualizamos la pantalla y el reloj
            pygame.display.flip()
            self.clock.tick(60)
    
    def reset_game(self):
        # Resetea el estado del juego cuando termina
        self.player1.rect.centerx = 600
        self.player2.rect.centerx = 200
        self.collision_count_p1 = 0
        self.collision_count_p2 = 0
        self.player1.score = 0
        self.player2.score = 0

    
    def game_over_1(self):
        player1_colision=int(self.collision_count_p1)
        player2_colision=int(self.collision_count_p2)
        winner=str(self.winner)
        score_player1=int(self.player1.score)
        score_player2=int(self.player2.score)
        
        url = "http://localhost:8000/stats"
        data = {
            "player1_collisions": player1_colision,
            "player2_collisions": player2_colision,
            "winner": winner,
            "score_player1": score_player1,
            "score_player2": score_player2
        }


        response = requests.post(url, json=data)
        try:
            response = requests.post(url, json=data)
            response.raise_for_status()  # Lanza una excepción para códigos de estado 4xx y 5xx
            print("Datos guardados con éxito:", response.json())
        except requests.exceptions.RequestException as e:
            print(f"Error al enviar los datos: {e}")

    def check_collisions(self, player, player_num):

        # Colisiones entre meteoritos y player
        collisions = pygame.sprite.spritecollide(player, self.meteorites, False)
        if collisions:
            for meteorite in collisions:
                meteorite.reset_position()
            if player_num == 1:
                self.collision_count_p1 += 1
                self.p1_colision.inc()
                print(f"Colisiones Jugador 1: {self.collision_count_p1}")
            else:
                self.collision_count_p2 += 1
                self.p2_colision.inc()
                print(f"Colisiones Jugador 2: {self.collision_count_p2}")
        
        #colisiones entre monedas y player
        collisions = pygame.sprite.spritecollide(player, self.coins, False)
        if collisions:
            for coin in collisions:
                coin.reset_position()
            if player_num == 1:
                self.player1.update_score()
                self.p1_score.inc(20)
            else:
                self.player2.update_score()
                self.p2_score.inc(20)

    def end_game(self):
        self.winner = "Jugador 1" if self.player1.score > self.player2.score else "Jugador 2"
        
    def display_time(self):
        # Restamos el tiempo actual menos el tiempo de inicio del juego 
        current_time = pygame.time.get_ticks() - self.start_time
        seconds = current_time // 1000
        time_text = self.font.render(f"Tiempo: {seconds} s", True, (255, 255, 255))
        self.screen.blit(time_text, (10, 70))                       
    
            
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

    def metrics(self):
        url = "http://localhost:8000/metrics"
        response = requests.get(url)

""""
    # Loop principal 
    def loop(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if self.controller==1:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:  # 1 es el botón izquierdo del ratón
                            # Obtener la posición del clic
                            mouse_pos = pygame.mouse.get_pos()
                            # Verificar si el clic ocurrió dentro del área del botón
                            if self.buttom_rect_start.collidepoint(mouse_pos):
                                # entra al juego directamente
                                self.start_time = pygame.time.get_ticks()  # Guarda el tiempo de inicio del juego 
                                self.controller=2
                                # cerramos si cierras la ventana en loop
                            if self.buttom_rect_stats.collidepoint(mouse_pos):
                                self.stats_screen()
                            if self.buttom_rect_off.collidepoint(mouse_pos):
                                self.controller=1
                else:
                    if self.controller==3:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if event.button == 1:  # 1 es el botón izquierdo del ratón
                                # Obtener la posición del clic
                                mouse_pos = pygame.mouse.get_pos()
                                # Verificar si el clic ocurrió dentro del área del botón
                                if self.button_rect_restart.collidepoint(mouse_pos):
                                    self.controller=1
                                    self.player1.rect.centerx=600
                                    self.player2.rect.centerx=200
            if self.controller == 1:
                self.player1.score=0
                self.player2.score=0
                self.collision_count_p1=0
                self.collision_count_p2=0
                self.start_time = pygame.time.get_ticks()  # Guarda el tiempo de inicio del juego 
                self.draw_menu()
            else:
                if self.controller == 2:
                    self.handle_input()
                    self.update()
                    self.draw()
                
                if (self.player1.score == 100 or self.player2.score == 100 or (self.collision_count_p1 == 3 and self.collision_count_p2 == 3)):
                    self.controller=3
                    print('Ingresando al menú de finalización')
                    self.end_game() #Determina el ganador
                    self.game_over() # Termina el juego #x y manda los datos a la base de datos
                    self.metrics()
                    self.end_screen() # pantalla final 
                    self.player1.rect.centerx=600
                    self.player2.rect.centerx=200
                    self.collision_count_p1=0
                    self.collision_count_p2=0
                    self.player1.score=0
                    self.player2.score=0
                    # Al finalizar el juego             
            self.clock.tick(60)
            
"""     