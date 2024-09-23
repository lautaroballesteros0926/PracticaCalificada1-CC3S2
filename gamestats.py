from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class GameStats(Base):
    __tablename__ = 'game_stats'
    
    id = Column(Integer, primary_key=True)
    player1_collisions = Column(Integer)
    player2_collisions = Column(Integer)
    winner = Column(String)
    score_player1 = Column(Integer)
    score_player2 = Column(Integer)

engine = create_engine('sqlite:///game_stats.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
