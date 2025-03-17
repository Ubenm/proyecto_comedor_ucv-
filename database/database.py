# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker, declarative_base

# # Configuración de SQLite (o PostgreSQL)
# #DATABASE_URL = "postgresql://admin:1234/db"
# DATABASE_URL = "sqlite:///comedor_ucv.db"

# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String
from werkzeug.security import generate_password_hash, check_password_hash

# Configuración de la base de datos
Base = declarative_base()
engine = create_engine("sqlite:///comedor_ucv.db")
SessionLocal = sessionmaker(bind=engine)  # Nombre correcto para importar

# Modelo de Usuario
class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(200), nullable=False)
    rol = Column(String(20), default="estudiante")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Crear tablas (ejecutar una vez)
if __name__ == "__main__":
    Base.metadata.create_all(engine)