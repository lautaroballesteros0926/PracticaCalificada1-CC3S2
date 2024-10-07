import pygame

class EndScreen:
    def __init__(self):
        # Cargar imágenes, fuentes y otros elementos solo una vez durante la inicialización
        self.background_image = pygame.image.load("sprites/fondo.png")
        self.button_restart = pygame.image.load("sprites/boton_off.png")
        self.font_large = pygame.font.Font(None, 57)
        self.font_medium = pygame.font.Font(None, 50)
        self.font_small = pygame.font.Font(None, 35)
        self.font_stats = pygame.font.Font(None, 28)

        # Guardar las posiciones de los botones
        self.button_rect_restart = self.button_restart.get_rect(topleft=(300, 500))
    
    def draw(self, game):
        # Usar los atributos de la clase para dibujar en la pantalla
        self._draw_background(game)
        self._draw_buttons(game)
        self._draw_game_over_text(game)
        self._draw_winner_text(game)
        self._draw_stats(game)
    
    def _draw_background(self, game):
        """Dibuja el fondo en la pantalla final."""
        game.screen.blit(self.background_image, (0, 0))

    def _draw_buttons(self, game):
        """Dibuja los botones de reiniciar y volver al menú."""
        game.screen.blit(self.button_restart, self.button_rect_restart.topleft)

    def _draw_game_over_text(self, game):
        """Dibuja el texto principal de 'Game Over'."""
        game_over_text = self.font_large.render("¡Juego Terminado!", True, (255, 255, 255))
        game.screen.blit(game_over_text, (200, 110))

    def _draw_winner_text(self, game):
        """Muestra el ganador del juego."""
        if game.player1.score > game.player2.score:
            winner_text = self.font_medium.render("Ganó el Jugador 1", True, (255, 255, 255))
        elif game.player2.score > game.player1.score:
            winner_text = self.font_medium.render("Ganó el Jugador 2", True, (255, 255, 255))
        else:
            winner_text = self.font_medium.render("Empate", True, (255, 255, 255))
        game.screen.blit(winner_text, (200, 160))

    def _draw_stats(self, game):
        """Muestra las estadísticas de los jugadores."""
        stats_text = self.font_medium.render("Resumen del Juego:", True, (255, 255, 255))
        game.screen.blit(stats_text, (200, 200))

        # Estadísticas del Jugador 1
        self._draw_player_stats(game, 1, game.collision_count_p1, game.player1.score, 260)

        # Estadísticas del Jugador 2
        self._draw_player_stats(game, 2, game.collision_count_p2, game.player2.score, 340)

    def _draw_player_stats(self, game, player_num, collisions, score, y_offset):
        """Dibuja las estadísticas de un jugador específico."""
        player_text = self.font_small.render(f"Jugador {player_num}:", True, (255, 255, 255))
        game.screen.blit(player_text, (200, y_offset))

        player_stats = self.font_stats.render(f"Número de colisiones: {collisions}, Score: {score}", True, (255, 255, 255))
        game.screen.blit(player_stats, (200, y_offset + 40))
