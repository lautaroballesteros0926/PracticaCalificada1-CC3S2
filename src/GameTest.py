import pygame
from game import Game  # Asegúrate de importar correctamente tu clase Game

class GameTest:
    def __init__(self):
        pygame.init()
        self.game = Game()

    def run(self):
        self.game.loop()
        pygame.quit()

if __name__ == "__main__":
    test = GameTest()
    test.run()
