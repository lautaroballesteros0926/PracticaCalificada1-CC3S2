import pygame

class carrera:
    def __init__(self):
        pass
    def draw(self, game):
        # Dibuja el fondo
        game.background.draw(self.screen)

        #Dibuja los sprites si tienen puntaje menor a 100 y si aun tienen vidas 
        if(game.player1.score < 100 and game.collision_count_p1<3): 
            game.screen.blit(game.player1.image, game.player1.rect)
        if(game.player2.score < 100 and self.collision_count_p2<3):
            game.screen.blit(game.player2.image, game.player2.rect)

        game.meteorites.draw(game.screen) # distinto porque es un grupo de sprites 
        game.coins.draw(game.screen)
        
        # Mostrar contadores de colisiones
        text_p1 = game.font.render(f"Score: {game.player1.score}", True, (255, 255, 255))
        text_p2 = game.font.render(f"Score: {game.player2.score}", True, (255, 255, 255))
        game.screen.blit(text_p1, (10, 10))
        game.screen.blit(text_p2, (10, 40))

        game.display_time()

    #Actualiza todos los sprites 
    def update(self,game):
        
        game.background.update()  # Actualiza el fondo
        
        # Actualizamos posiciones de los sprites 
        
        game.meteorites.update()
        game.coins.update()

        # Verificar colisiones si es que no llegan a 100 y aun no se le acaba las vida (maximo 3 choques)
        if game.player1.score <100 and game.collision_count_p1<3:
            game.check_collisions(game.player1, 1)

        if game.player2.score <100 and game.collision_count_p2<3:
            game.check_collisions(game.player2, 2)
    
    def draw(self,game):
        # Dibuja el fondo
        game.background.draw(game.screen)

        #Dibuja los sprites si tienen puntaje menor a 100 y si aun tienen vidas 
        if(game.player1.score < 100 and game.collision_count_p1<3): 
            game.screen.blit(game.player1.image, game.player1.rect)
        if(game.player2.score < 100 and game.collision_count_p2<3):
            game.screen.blit(game.player2.image, game.player2.rect)

        game.meteorites.draw(game.screen) # distinto porque es un grupo de sprites 
        game.coins.draw(game.screen)
        
        # Mostrar contadores de colisiones
        text_p1 = game.font.render(f"Score: {game.player1.score}", True, (255, 255, 255))
        text_p2 = game.font.render(f"Score: {game.player2.score}", True, (255, 255, 255))
        game.screen.blit(text_p1, (10, 10))
        game.screen.blit(text_p2, (10, 40))

        game.display_time()