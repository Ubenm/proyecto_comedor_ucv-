from sqlalchemy import create_engine, Column, Integer, String, Boolean, Date, UniqueConstraint, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker
import bcrypt
from datetime import date


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
def restar_racion(tipo_comida):
    """Resta 1 ración del menú del día"""
    session = Session()
    try:
        menu = session.query(MenuDia).filter(
            MenuDia.fecha == date.today(),
            MenuDia.tipo_comida == tipo_comida
        ).first()
        
        if menu and menu.cantidad_disponible > 0:
            menu.cantidad_disponible -= 1
            session.commit()
            return True
        return False
    except Exception as e:
        print(f"Error: {str(e)}")
        session.rollback()
        return False
    finally:
        session.close()
Base.metadata.create_all(engine)