# language: es

  Característica: Menu Finalizacion

    Escenario: Ingreso a menu finalizacion cuando gana el jugador 1
      Dado que la nave del "jugador 1 tiene 2 vidas"
      Cuando llega a los "100 puntos"
      Entonces el jugador podrá visualizar los resultados de la partida

    Escenario: Ingreso a menu finalizacion cuando gana el jugador 2
      Dado que la nave del "jugador 2 tiene 3 vidas"
      Cuando llega a los "100 puntos"
      Entonces el jugador podrá visualizar los resultados de la partida

    Escenario: VISUALIZACION DE ESTADISTICAS CUANDO NO SE LLEGO A LOS 100 
      Dado que la nave del "jugador 1 tiene 0 vidas"
      Cuando la nave del "jugador 2 tiene 0 vidas" 
      Entonces el jugador podrá visualizar los resultados de la partida


