 # language: es

  Característica: Colisiones con meteorito

    Escenario: Colision de meteorito con nave
      Dado que la nave se encuentra en la posicion 600,600
      Cuando el meteorito se encuentra en la posicion 600,600
      Entonces se le resta una vida al jugador

    Escenario: Colision por tercera vez
      Dado la posicion del meteorito y de la nave coinciden y es 100,600
      Cuando el meteorito colisiona "3 veces" con la nave
      Entonces la nave debe ser destruida


