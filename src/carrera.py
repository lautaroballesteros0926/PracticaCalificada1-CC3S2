import pygame

class Carrera:
    def __init__(self, max_score=100, max_collisions=3):
        self.max_score = max_score  # Puntaje máximo
        self.max_collisions = max_collisions  # Máximo de colisiones permitidas
    
    def draw(self, game):
        """Dibuja todos los elementos en pantalla durante la carrera."""
        # Dibuja el fondo
        game.background.draw(game.screen)

        # Dibuja los jugadores si tienen puntaje menor a max_score y colisiones menores a max_collisions
        if game.player1.score < self.max_score and game.collision_count_p1 < self.max_collisions: 
            game.screen.blit(game.player1.image, game.player1.rect)
        
        if game.player2.score < self.max_score and game.collision_count_p2 < self.max_collisions:
            game.screen.blit(game.player2.image, game.player2.rect)

        # Dibuja los grupos de meteoritos y monedas
        game.meteorites.draw(game.screen)
        game.coins.draw(game.screen)
        
        # Mostrar contadores de puntaje
        text_p1 = game.font.render(f"Score: {game.player1.score}", True, (255, 255, 255))
        text_p2 = game.font.render(f"Score: {game.player2.score}", True, (255, 255, 255))
        game.screen.blit(text_p1, (10, 10))
        game.screen.blit(text_p2, (10, 40))

        # Mostrar el tiempo restante o actual en la pantalla
        game.display_time()

    def update(self, game):
        """Actualiza los elementos de la carrera."""
        # Actualiza el fondo
        game.background.update()

        # Actualiza los meteoritos y monedas
        game.meteorites.update()
        game.coins.update()
        # Verificar colisiones y actualizaciones de puntaje si los jugadores no alcanzan el puntaje máximo y aún tienen vidas
        if game.player1.score < self.max_score and game.collision_count_p1 < self.max_collisions:
            game.check_collisions(game.player1, 1)

        if game.player2.score < self.max_score and game.collision_count_p2 < self.max_collisions:
            game.check_collisions(game.player2, 2)

