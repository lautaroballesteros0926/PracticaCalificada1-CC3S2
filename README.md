# Documentacion


# API REST - Juego de Naves Espaciales

Esta API está diseñada para gestionar un juego de naves espaciales, donde los jugadores compiten para llegar a la meta evitando obstáculos. Se pueden realizar movimientos de las naves, consultar el estado del juego, y almacenar estadísticas y resultados de las partidas. Además, la API está instrumentada con Prometheus para monitorear métricas, como la velocidad de las naves y las colisiones.

## Base URL
```
http://127.0.0.1:8000
```

---

## Endpoints

### 1. Abrir el menú principal

**Descripción**: Inicia el menú principal del juego.

- **URL**: `/open_menu`
- **Método**: `POST`
- **Respuesta**:
  - `200 OK`: `{"message": "Menu Abierto"}`

---

### 2. Abrir pantalla de estadísticas

**Descripción**: Abre la pantalla de estadísticas del juego.

- **URL**: `/open_stats`
- **Método**: `POST`
- **Respuesta**:
  - `200 OK`: `{"message": "Stats abierto"}`

---

### 3. Iniciar el juego

**Descripción**: Inicia una nueva partida del juego.

- **URL**: `/start_game`
- **Método**: `POST`
- **Respuesta**:
  - `200 OK`: `{"message": "Juego iniciado"}`

---

### 4. Mover la nave

**Descripción**: Mueve la nave del jugador en la dirección especificada.

- **URL**: `/move`
- **Método**: `POST`
- **Cuerpo**:
  ```json
  {
    "player": 1, 
    "direction": "left"  // o "right"
  }
  ```
- **Respuesta**:
  - `200 OK`: `{"message": "Movimiento realizado"}`
  - `400 Bad Request`: `"Jugador inválido"`

---

### 5. Consultar estado del jugador

**Descripción**: Obtiene la posición y el número de colisiones del jugador.

- **URL**: `/status`
- **Método**: `GET`
- **Parámetro de consulta**: `player` (número de jugador)
- **Respuesta**:
  - `200 OK`: 
    ```json
    {
      "player": 1,
      "position": 150,
      "collisions": 3
    }
    ```
  - `400 Bad Request`: `"Jugador inválido"`

---

### 6. Cerrar el juego

**Descripción**: Cierra el juego y libera los recursos de `pygame`.

- **URL**: `/close`
- **Método**: `POST`
- **Respuesta**:
  - `200 OK`: `{"message": "Juego cerrado exitosamente"}`
  - `400 Bad Request`: `"El juego no está iniciado"`

---

### 7. Crear y almacenar una partida

**Descripción**: Guarda las estadísticas de una partida finalizada.

- **URL**: `/games`
- **Método**: `POST`
- **Cuerpo**:
  ```json
  {
    "player1_score": 300,
    "player2_score": 250,
    "winner": "player1"
  }
  ```
- **Respuesta**:
  - `200 OK`: 
    ```json
    {
      "message": "Partida almacenada exitosamente",
      "game": {
        "player1_score": 300,
        "player2_score": 250,
        "winner": "player1"
      }
    }
    ```

---

### 8. Obtener todas las partidas almacenadas

**Descripción**: Devuelve la lista de todas las partidas almacenadas.

- **URL**: `/games`
- **Método**: `GET`
- **Respuesta**:
  - `200 OK`: 
    ```json
    [
      {
        "player1_score": 300,
        "player2_score": 250,
        "winner": "player1"
      },
      {
        "player1_score": 180,
        "player2_score": 220,
        "winner": "player2"
      }
    ]
    ```

---

## Prometheus Metrics

La API está instrumentada con `prometheus_fastapi_instrumentator` para recopilar métricas de la aplicación, como el número de peticiones y la latencia. Estas métricas están disponibles en `/metrics`.
