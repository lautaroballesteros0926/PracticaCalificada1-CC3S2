from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from game import Game  # Importamos tu código de la clase Game
from gamestats import Session,GameStats
import pygame
import uvicorn
from typing import List
from prometheus_fastapi_instrumentator import Instrumentator
# Inicializamos FastAPI y el juego
app = FastAPI()
pygame.init()

Instrumentator().instrument(app).expose(app)

# Modelo para mover las naves
class MoveRequest(BaseModel):
    player: int
    direction: str  # "left" o "right"

class GameController(BaseModel):
    option: int


def run_game(a):
    global game
    game=Game()
    if a==1:
        game.main_menu()  # Inicia el menú principal del juego
    elif a==2: 
        game.stats_screen()
    else: 
        game.loop()



# Endpoint para iniciar el juego
@app.post("/option")
def optionMenu( game_controller : GameController):
    option = game_controller.option
    game.controller = option
    return {"message": "Menu Abierto"}

@app.post("/open_stats")
def open(): 
    run_game(2)
    return  {"message": "Stats abierto"}
    
@app.post("/start_game")
def openjuego():
    global game
    game=Game()
    game.loop()
    return{"message":"Interfaz Abierta"}
# Endpoint para mover la nave
@app.post("/move")
def move_ship(move_request: MoveRequest):
    player = move_request.player
    direction = move_request.direction

    if player == 1:
        if direction == 'left':
            game.player1.move(-5, 0)
        elif direction == 'right':
            game.player1.move(5, 0)
    elif player == 2:
        if direction == 'left':
            game.player2.move(-5, 0)
        elif direction == 'right':
            game.player2.move(5, 0)
    else:
        raise HTTPException(status_code=400, detail="Jugador inválido")

    return {"message": "Movimiento realizado"}

# Endpoint para consultar la posición y estado del jugador
@app.get("/status")
def get_status(player: int):
    if player == 1:
        position = game.player1.rect.x
        collisions = game.collision_count_p1
    elif player == 2:
        position = game.player2.rect.x
        collisions = game.collision_count_p2
    else:
        raise HTTPException(status_code=400, detail="Jugador inválido")

    return {
        "player": player,
        "position": position,
        "collisions": collisions
    }

""""
@app.get("/stats")
def get_stats():
    session = Session()
    stats = session.query(GameStats).all()
    session.close()
    
    return [{"game_id": stat.id,  # Añadir el número de juego (ID)
             "player1_collisions": stat.player1_collisions, 
             "player2_collisions": stat.player2_collisions, 
             "winner": stat.winner, 
             "score_player1": stat.score_player1, 
             "score_player2": stat.score_player2} for stat in stats]
"""



# Endpoint para cerrar el juego
@app.post("/close")
def close_game():
    global game
    if not game:
        raise HTTPException(status_code=400, detail="El juego no está iniciado")

    pygame.quit()
    game = None  # Reiniciar el estado del juego
    return {"message": "Juego cerrado exitosamente"}



# Guardar los datos del juego 

class GameData(BaseModel):
    player1_score: int
    player2_score: int
    winner: str

# Base de datos simulada para almacenar las partidas
games = []

@app.post("/games")
def create_game(game: GameData):
    """
    Crea una nueva partida y la almacena.
    """
    games.append(game)
    return {"message": "Partida almacenada exitosamente", "game": game}

@app.get("/games", response_model=List[GameData])
def get_games():
    """
    Retorna todas las partidas anteriores.
    """
    return games

# Ejecutar el servidor usando uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)