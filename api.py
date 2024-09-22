from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from game import Game  # Importamos tu código de la clase Game
import pygame
import uvicorn
# Inicializamos FastAPI y el juego
app = FastAPI()
pygame.init()


# Modelo para mover las naves
class MoveRequest(BaseModel):
    player: int
    direction: str  # "left" o "right"

def run_game(a):
    global game
    game=Game()

    if a==1:
        game.main_menu()  # Inicia el menú principal del juego
    else: 
        game.loop()  



# Endpoint para iniciar el juego
@app.post("/open")
def open():
    run_game(1)
    return {"message": "Menu Abierto"}


@app.post("/start_game")
def open():
    run_game(2)
    return {"message": "Juego iniciado"}

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

# Ejecutar el servidor usando uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)