import pygame

class EventHandler:
    def handle_event(self, game, event):
        if event.type == pygame.QUIT:
            return False  # Sale del bucle principal
        
        # Delegar el manejo de eventos según el controlador del juego
        if game.controller == 1:  # Menu principal 
            return self.handle_menu_event(game, event)
        elif game.controller == 2:  # Carrera
            pass
        elif game.controller == 3:  # reinicia el juego 
            return self.handle_end_event(game,event)
        
        return True  

    def handle_menu_event(self, game, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 1 es el botón izquierdo del ratón
                    # Obtener la posición del clic
                    mouse_pos = pygame.mouse.get_pos()
                    # Verificar si el clic ocurrió dentro del área del botón
                    if game.main_menu.buttom_rect_start.collidepoint(mouse_pos):
                        # entra al juego directamente
                        game.start_time = pygame.time.get_ticks()  # Guarda el tiempo de inicio del juego 
                        game.controller = 2 
                    if game.main_menu.buttom_rect_stats.collidepoint(mouse_pos):
                        game.controller = 4  # pantalla de estadistica 
        return True              
    
    def handle_end_event(self, game, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # 1 es el botón izquierdo del ratón
                # Obtener la posición del clic
                mouse_pos = pygame.mouse.get_pos()
                # Verificar si el clic ocurrió dentro del área del botón
                if game.end_screen.button_rect_restart.collidepoint(mouse_pos):
                    game.controller=1
        return True