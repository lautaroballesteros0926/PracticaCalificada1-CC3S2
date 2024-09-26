from fastapi import Depends,FastAPI, HTTPException
from pydantic import BaseModel
from game import Game  # Importamos tu código de la clase Game
import pygame
import uvicorn
from typing import List

from prometheus_fastapi_instrumentator import Instrumentator
from database import engine,get_db
from sqlalchemy.orm import Session
from models import Base,GameStats
# Inicializamos FastAPI y el juego
app = FastAPI() 

Base.metadata.create_all(bind=engine)


pygame.init()

Instrumentator().instrument(app).expose(app)
# Modelo para mover las naves
class MoveRequest(BaseModel):
    player: int
    direction: str  # "left" o "right"


class GameController(BaseModel):
    option: int

class GameStatsCreate(BaseModel):
    player1_collisions: int
    player2_collisions: int
    winner: str
    score_player1: int
    score_player2: int


# Endpoint para iniciar el juego
@app.post("/option")
def optionMenu( game_controller : GameController):
    option = game_controller.option
    game.controller = option
    return {"message": "Menu Abierto"}


    
@app.post("/open_menu")
def openjuego():
    global game
    game=Game()
    game.loop()
    return{"message":"Interfaz Abierta"}
# Endpoint para mover la nave

@app.post("/move")
def move_ship(move_request: MoveRequest):
    global game  # Asegúrate de que estás accediendo a la instancia global del juego
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


@app.get("/stats")
def get_stats(db: Session = Depends (get_db)):
    return db.query(GameStats).all()



# Endpoint para guardar estadísticas del juego
@app.post("/stats")
def save_stats(
    stats: GameStatsCreate,  # Cambiar a usar el modelo
    db: Session = Depends(get_db)
):
    new_stat = GameStats(
        player1_collisions=stats.player1_collisions,
        player2_collisions=stats.player2_collisions,
        winner=stats.winner,
        score_player1=stats.score_player1,
        score_player2=stats.score_player2
    )
    db.add(new_stat)
    db.commit()
    db.refresh(new_stat)
    return new_stat

# Ejecutar el servidor usando uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
