from src.game import Game
from src.meteorite import Meteorite
from behave import given,when,then
import re
import pygame
pygame.init()

game=Game()
meteorite=Meteorite()

######################################################
def movement(move):
    print(game.player2.rect.centerx)
    if move=='izquierda' and game.player1.rect.centerx==595:
        game.player1.rect.centerx=600
        return True
    elif move=='derecha' and game.player1.rect.centerx==605:
        game.player1.rect.centerx=600
        return True
    else:
        return False

@given('que quiero moverme en direccion {direccion}')
def check_movimiento(context,direccion):
    pattern=re.compile(r'(izquierda|derecha|arriba)')
    match=pattern.match(direccion.lower())
    print(game.player1.rect)
    if match:
        print('a')
    else:
        raise ValueError(f"No se pudo interpretar el movimiento: {direccion}")


@when('presiono el boton flecha {direccion}')
def do_movement(context,direccion):
    pattern=re.compile(r'(izquierda|derecha|arriba)')
    match=pattern.match(direccion.lower())
    if match:
        if match.group(1)=='izquierda':
            game.player1.move(0,0)
        elif match.group(1)=='derecha':
            game.player1.move(0,0)
        else:
            print('No se movio la nave')
    else:
        raise ValueError(f"No se pudo interpretar el boton presionado: {direccion}")
    
@then('debo mover a la izquierda 5 pixeles')
def check_movement(context):
    assert movement('izquierda'),"No se movio la nave correctamente"
@then('debo mover a la derecha 5 pixeles')
def check_movement_right(context):
    assert movement('derecha'),"No se movio la nave correctamente"
@then('no debe suceder ningun movimiento')
def check_movement_up(context):
    assert not movement('derecha'),"La nave no debio haberse movido"



########################################

@given('que la nave se encuentra en la posicion {posicion}')
def colision_player(context,posicion):
    pattern=re.compile(r'(\d+),(\d+)')
    match=pattern.match(posicion.lower())
    if match:
        x_player=int(match.group(1))
        y_player=int(match.group(2))
        game.player1.rect.topleft=(x_player,y_player)
    else:
        raise(f'sdas')


@when('el meteorito se encuentra en la posicion {posicion}')
def colision_meteorite(context,posicion):
    pattern=re.compile(r'(\d+),(\d+)')
    match=pattern.match(posicion.lower())
    if match:
        x_met=int(match.group(1))
        y_met=int(match.group(2))
        meteorite.rect.bottomleft=(x_met,y_met)
        game.meteorites=meteorite

    else:
        raise(f'sdas')
    
@then('Se le resta una vida al jugador')
def colision_life(context):
    game.check_collisions(game.player1,1)
    assert game.collision_count_p1==1,"Se deberia restar una vida al jugador"



