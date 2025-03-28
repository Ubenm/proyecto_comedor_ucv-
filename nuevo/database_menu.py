from sqlalchemy import create_engine, Column, Integer, String, Boolean, Date, UniqueConstraint, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker
import bcrypt
from datetime import datetime
from database import Base_usuarios  # Importar Base desde usuarios

class RegistroComida(Base_usuarios):  # Usar la misma Base declarativa
    __tablename__ = "registro_comidas"
    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    menu_id = Column(Integer, ForeignKey('menus.id')) 
    fecha = Column(Date, default=datetime.now())
    tipo_comida = Column(String)
    # Configurar motor y sesión
engine_menu = create_engine("sqlite:///menu.db")
Session_menu = sessionmaker(bind=engine_menu)
Base_usuarios.metadata.create_all(engine_menu)  # Crear todas las tablas

DATABASE_URL = "sqlite:///menu.db"
engine = create_engine(DATABASE_URL, echo=False)  # Motor de la base de datos
Base = declarative_base()  # Base para los modelos
Session = sessionmaker(bind=engine)  # Sesión para interactuar con la base de datos

# Añadir después de la clase Usuario
Base_menu = declarative_base()
class MenuDia(Base_menu):
    __tablename__ = "menus"
    id = Column(Integer, primary_key=True, autoincrement=True)
    fecha = Column(Date, nullable=False)
    tipo_comida = Column(String, nullable=False)  # Desayuno/Almuerzo/Cena
    descripcion = Column(String, nullable=False)
    imagen_url = Column(String)
    cantidad_disponible = Column(Integer, nullable=False)
    __table_args__ = (UniqueConstraint('fecha', 'tipo_comida', name='uq_fecha_comida'),)

# Funciones CRUD para menús
def insertar_menu(fecha, tipo_comida, descripcion, imagen_url, cantidad):
    session = Session()
    nuevo_menu = MenuDia(
        fecha=fecha,
        tipo_comida=tipo_comida,
        descripcion=descripcion,
        imagen_url=imagen_url,
        cantidad_disponible=cantidad
    )
    session.add(nuevo_menu)
    session.commit()
    session.close()

def obtener_menus(fecha=None):
    session = Session()
    query = session.query(MenuDia)
    if fecha:
        query = query.filter(MenuDia.fecha == fecha)
    resultados = query.all()
    session.close()
    return resultados

def actualizar_menu(id_menu, nuevos_datos):
    session = Session()
    menu = session.query(MenuDia).get(id_menu)
    for key, value in nuevos_datos.items():
        setattr(menu, key, value)
    session.commit()
    session.close()

def eliminar_menu(id_menu):
    session = Session()
    menu = session.query(MenuDia).get(id_menu)
    session.delete(menu)
    session.commit()
    session.close()