# database.py
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from werkzeug.security import generate_password_hash

# Configuración de SQLite (archivo .db)
Base = declarative_base()
engine = create_engine("sqlite:///comedor_ucv.db")
Session = sessionmaker(bind=engine)

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(200), nullable=False)
    rol = Column(String(20), default="estudiante")

# Crear tablas (ejecutar una vez)
if __name__ == "__main__":
    Base.metadata.create_all(engine)
    print("Base de datos creada ✅")