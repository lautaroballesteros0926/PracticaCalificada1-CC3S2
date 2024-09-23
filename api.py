from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from game import Game  # Importamos tu código de la clase Game
from gamestats import Session,GameStats
import pygame
import uvicorn
from typing import List
import threading
# Inicializamos FastAPI y el juego  
app = FastAPI()
pygame.init()

# Modelo para mover las naves
class MoveRequest(BaseModel):
    player: int
    direction: str  # "left" o "right"

# Inicializa el objeto de bloqueo
lock = threading.Lock()

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
@app.post("/open_menu")
def open():
    # Correr el juego en un hilo separado
    thread = threading.Thread(target=run_game, args=(1,))   
    thread.start()  # Inicia el hilo que ejecuta el menú
    return {"message": "Menu Abierto"}  # Retorna la respuesta inmediatamente

@app.post("/open_stats")
def open(): 
    run_game(2)
    return  {"message": "Stats abierto"}
    
@app.post("/start_game")
def start_game():
    thread = threading.Thread(target=run_game, args=(3,))
    thread.start()  # Inicia el hilo para iniciar el juego
    return {"message": "Juego iniciado"}

@app.post("/move")
def move_ship(move_request: MoveRequest):
    global game  # Asegúrate de que estás accediendo a la instancia global del juego
    player = move_request.player
    direction = move_request.direction

    with lock:  # Usa el lock para evitar condiciones de carrera
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