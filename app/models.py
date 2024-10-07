from sqlalchemy import Column, Integer, String
from app.database import Base
#Define una tabla de la base de datos
class GameStats(Base):
    __tablename__="gamestats"

    id= Column(Integer,primary_key=True,index=True)
    player1_collisions= Column(Integer)
    player2_collisions= Column(Integer)
    winner= Column(String)
    score_player1= Column(Integer)
    score_player2= Column(Integer)
