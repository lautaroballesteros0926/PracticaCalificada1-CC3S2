from game import Game
from meteorite import Meteorite
from behave import given,when,then
import re


game=Game()

######################################################
def movement(move):
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
    if match:
        print('a')
    else:
        raise ValueError(f"No se pudo interpretar el movimiento: {direccion}")


@when('presiono el boton flecha {direccion}')
def do_movement(context,direccion):
    pattern=re.compile(r'(izquierda|derecha|arriba)()')
    match=pattern.match(direccion.lower())
    if match:
        if match.group(1)=='izquierda':
            game.player1.move(-5,0)
        elif match.group(1)=='derecha':
            game.player1.move(5,0)
        else:
            print('No se movio la nave')
    else:
        raise ValueError(f"No se pudo interpretar el boton presionado: {direccion}")
    
@then('debo moverme a la izquierda  pixeles')
def check_movement(context):
    assert movement('izquierda'),"No se movio la nave correctamente"
@then('debo moverme a la derecha  pixeles')
def check_movement_right(context):
    assert movement('derecha'),"No se movio la nave correctamente"
@then('no debe suceder ningun movimiento')
def check_movement_up(context):
    assert not movement('derecha'),"La nave no debio haberse movido"



########################################

@given('que el meteorito colisiona con la nave')
def colision_metoerite(context):
    game.player1.rect.top=(100,50)
    meteorite=Meteorite()
    meteorite.rect.bottom=(100,50)

    if meteorite.rect.bottom==game.player1.rect.top:
        print('Las posiciones del meteorito y la nave son las mismas')
    else:
        raise ValueError()




