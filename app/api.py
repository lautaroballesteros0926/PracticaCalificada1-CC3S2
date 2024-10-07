from fastapi import Depends,FastAPI, HTTPException, Response
from pydantic import BaseModel
from src.game import Game  # Importamos tu código de la clase Game
import pygame
import uvicorn
import prometheus_client
from app.database import engine,get_db
from sqlalchemy.orm import Session
from app.models import Base,GameStats
# Inicializamos FastAPI y el juego
app = FastAPI() 

Base.metadata.create_all(bind=engine)


pygame.init()

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

@app.get("/games")
def get_stats(db: Session = Depends (get_db)):
    return db.query(GameStats).all()

# Endpoint para guardar estadísticas del juego
@app.post("/stats")
def save_stats(stats: GameStatsCreate,db: Session = Depends(get_db)):
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

@app.get("/metrics")
def get_metrics():
    return Response(
        content=prometheus_client.generate_latest(),
        media_type="text/plain",
    )


@app.get("/positions")
def get_status():
    position1 = game.player1.rect.x
    position2 = game.player2.rect.x
    return {
        "player1 position": position1,
        "player2 position": position2
    }

# Ejecutar el servidor usando uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
