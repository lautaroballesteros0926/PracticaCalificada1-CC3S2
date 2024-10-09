Feature: Colisiones con monedas

    Scenario: Colision de moneda con nave
        Given la moneda se ubica en la posicion 100,600
        When la nave se ubica en la posicion 100,600
        Then colisionan y se le suma 20 puntos al jugador

    Scenario: Quinta colision de moneda con la nave
        Given la moneda y la nave coinciden su posicion en 100,600
        When la moneda colisiona 5 veces con la nave
        Then la nave colisionada gana la partida
    
    Scenario: reinicio de posicion de la moneda luego de colisicion
        Given la moneda se ubica en la posicion 100,600
        When la nave se ubica en la posicion 100,600
        Then la posicion de la moneda cambia a su posicion en el eje y inicial

