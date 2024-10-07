import pygame
import requests

class StatsScreen:
    def draw(self, game):

        sessions = self.get_stats()
        pygame.display.set_caption("Estadísticas")
        
        # Cargar la imagen de fondo
        background_image = pygame.image.load("sprites/fondo_espacial.png")
        game.screen.blit(background_image, (0, 0))
        
        # Configurar la fuente para mostrar el texto en pantalla
        font = pygame.font.Font(None, 36)
        
        # Coordenadas iniciales para imprimir las partidas
        y_offset = 50  # Margen superior
        line_spacing = 40  # Espacio entre cada línea
        
        # Iterar sobre las partidas obtenidas de la API
        for session in sessions[-5:]:  # Muestra solo las últimas 5 partidas
            player1_score = session['player1_score']
            player2_score = session['player2_score']
            winner = session['winner']
            
            # Texto que se mostrará para cada partida
            game_text = f"Jugador 1: {player1_score} - Jugador 2: {player2_score} - Ganador: {winner}"
            
            # Renderizar el texto
            text_surface = font.render(game_text, True, (255, 255, 255))  # Texto en blanco
            game.screen.blit(text_surface, (50, y_offset))  # Dibujar en la pantalla
            
            # Actualizar el offset para la siguiente línea
            y_offset += line_spacing


    def get_stats(self):
        api_url = "http://localhost:8000/games"
        response = requests.get(api_url)
        sessions = response.json()
        return sessions