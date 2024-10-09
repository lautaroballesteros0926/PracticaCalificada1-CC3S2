
Feature: LIMITES DE LA PANTALLA DE JUEGO

    Scenario: Limite izquierdo de la pantalla
        Given la nave llega al limite izquierda de la pantalla
        When presiono la tecla de flecha izquierda
        Then la nave no debe moverse

    Scenario: Limite derecho de la pantalla
        Given la nave llega al limite derecha de la pantalla
        When presiono la tecla de flecha derecha
        Then la nave no debe moverse
