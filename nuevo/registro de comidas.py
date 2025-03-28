from sqlalchemy import create_engine, Column, Integer, String, Date, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

DATABASE_URL = "sqlite:///registros_comida.db"  # Base de datos SQLite local
engine = create_engine(DATABASE_URL, echo=False)  # Motor de la base de datos
Base = declarative_base()  # Base para los modelos
Session = sessionmaker(bind=engine)  #

class RegistroComida(Base):
    __tablename__ = "registros_comida"
    id = Column(Integer, primary_key=True, autoincrement=True)
    cedula_usuario = Column(String, nullable=False)  # Almacenar cédula directamente
    fecha_hora = Column(DateTime, default=datetime.now())
    tipo_comida = Column(String, nullable=False)  # Desayuno/Almuerzo/Cena
    descripcion_menu = Column(String)  # Almacenar datos relevantes

def obtener_usuarios():
    """Obtiene todos los usuarios de la base de datos"""
    session = Session()
    usuarios = session.query(RegistroComida).all()
    session.close()
    return usuarios

