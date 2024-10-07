  # language: es

  Característica: Movimiento del jugador

    Escenario: Movimiento a la izquierda 
      Dado que quiero moverme en direccion izquierda
      Cuando presiono el boton flecha izquierda
      Entonces debo mover a la izquierda 5 pixeles

    Escenario: Movimiento a la derecha 
      Dado que quiero moverme en direccion derecha
      Cuando presiono el boton flecha derecha
      Entonces debo mover a la derecha 5 pixeles


    Escenario: Movimiento no permitido
      Dado que quiero moverme en direccion arriba
      Cuando presiono el boton flecha arriba
      Entonces no debe suceder ningun movimiento

