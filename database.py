from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,Session

database = "postgres_db"
contraseña = "postgres" #contraseña de tu usuario postgres
#Referencia al servidor de la base de datos
SQlALCHEMY_DATABASE_URL = f"postgresql://postgres:{contraseña}@{database}:5432/pygame"

# Crear el motor de SQLAlchemy para la conexión
engine = create_engine(SQlALCHEMY_DATABASE_URL)

# Crear una fábrica de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos
Base = declarative_base()

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()