from src.game import Game

def before_scenario(context, scenario):
    context.game = Game()