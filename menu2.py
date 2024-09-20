import pygame
import sys

pygame.init()

# Crear la pantalla
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Menú con botón")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Cargar la imagen del botón
button_image = pygame.image.load("sprites/boton_menu.png")
button_image = pygame.transform.scale(button_image, (300,100))  # Ajustar el tamaño del botón si es necesario

# Crear un rectángulo a partir de la imagen del botón
button_rect = button_image.get_rect()
button_rect.topleft = (250,100)  # Posición del botón en la pantalla

# Bucle principal del juego
running = True
while running:
    screen.fill(WHITE)  # Limpiar la pantalla con color blanco

    # Dibujar la imagen del botón en la pantalla
    screen.blit(button_image, button_rect.topleft)

    # Manejar eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Detectar si el botón del ratón ha sido presionado
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # 1 es el botón izquierdo del ratón
                # Obtener la posición del clic
                mouse_pos = pygame.mouse.get_pos()

                # Verificar si el clic ocurrió dentro del área del botón
                if button_rect.collidepoint(mouse_pos):
                    print("¡Botón clicado!")

    pygame.display.flip()  # Actualizar la pantalla

