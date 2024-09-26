import requests

# URL de tu API
API_URL = "http://localhost:8000"  # Cambia esto por el endpoint de tu API

# Función para mover jugadores
def mover_jugador(player_id, direction):
    data = {"player": player_id, "direction": direction}
    response = requests.post(f"{API_URL}/move", json=data)  # Llamada POST a la API para mover al jugador
    return response.json()

# Función para obtener las posiciones actuales de los jugadores
def obtener_posiciones():
    response = requests.get(f"{API_URL}/positions")  # Llamada GET a la API para obtener posiciones
    return response.json()

def open_game():
    # Lógica para abrir el juego mediante una solicitud a la API
    response = requests.post(API_URL)
    if response.status_code == 200:
        print("Juego abierto correctamente.")
    else:
        print("Error al abrir el juego.")

def start_game(option):
    # Lógica para iniciar el juego mediante una solicitud a la API
    data = {"option": option}
    response = requests.post(f"{API_URL}/option",json=data)
    if response.status_code == 200:
        print("Juego iniciado correctamente.")
    else:
        print("Error al iniciar el juego.")

# Función del menú interactivo
def mostrar_menu():
    print("\n--- Menú de Control del Juego ---")
    print("1. Mover a la izquierda jugador 1")
    print("2. Mover a la derecha jugador 1")
    print("3. Mover a la izquierda jugador 2")
    print("4. Mover a la derecha jugador 2")
    print("5. Mostrar coordenadas actuales de los jugadores")
    print("6. Salir")

# Función principal que maneja el ciclo
def main():
    controller=2
    while True:
        if controller == 2:
            inicio = input("Presione 2 para iniciar el juego o 0 para salir: ")
            if inicio == '2':
                start_game(2) 
            elif inicio == '0':
                print("Saliendo del juego...")
                break  # Salimos del ciclo principal

        while True:
            mostrar_menu()
            opcion = input("Selecciona una opción (1-6): ")

            if opcion == '1':
                            mover_jugador(1, 'left')  # Mover jugador 1 a la izquierda
            elif opcion == '2':
                            mover_jugador(1, 'right')  # Mover jugador 1 a la derecha
            elif opcion == '3':
                            mover_jugador(2, 'left')  # Mover jugador 2 a la izquierda
            elif opcion == '4':
                            mover_jugador(2, 'right')  # Mover jugador 2 a la derecha
            elif opcion == '5':
                            posiciones = obtener_posiciones()  # Obtener posiciones de los jugadores
                            print(f"Coordenadas actuales:\nJugador 1: {posiciones['player1']}\nJugador 2: {posiciones['player2']}")
            elif opcion == '6':
                            print("Volver al menu principal")
                            start_game(1)
                            controller=2
                            break
            else:
                            print("Opción inválida. Intenta de nuevo.")
            
        



if __name__ == "__main__":
    main()
