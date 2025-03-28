from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

# Configuración de la base de datos
DATABASE_URL = "sqlite:///registros_comida.db"
engine = create_engine(DATABASE_URL, echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)

class RegistroComida(Base):
    __tablename__ = "registros_comida"
    id = Column(Integer, primary_key=True, autoincrement=True)
    cedula_usuario = Column(String, nullable=False)
    fecha_hora = Column(DateTime, default=datetime.now)
    tipo_comida = Column(String, nullable=False)
    descripcion_menu = Column(String)

# Funciones CRUD mejoradas
def obtener_registros_comida():
    """Obtiene todos los registros de comida"""
    session = Session()
    registros = session.query(RegistroComida).all()
    session.close()
    return registros

def crear_registro_comida(cedula, tipo_comida, descripcion=""):
    """Crea un nuevo registro revolucionario"""
    session = Session()
    nuevo_registro = RegistroComida(
        cedula_usuario=cedula,
        tipo_comida=tipo_comida,
        descripcion_menu=descripcion
    )
    session.add(nuevo_registro)
    session.commit()
    session.close()
    return True

def actualizar_registro_comida(id_registro, nuevos_datos):
    """Actualiza un registro existente"""
    session = Session()
    registro = session.get(RegistroComida, id_registro)
    if registro:
        for key, value in nuevos_datos.items():
            setattr(registro, key, value)
        session.commit()
    session.close()

def eliminar_registro_comida(id_registro):
    """Elimina un registro contrarrevolucionario"""
    session = Session()
    registro = session.get(RegistroComida, id_registro)
    if registro:
        session.delete(registro)
        session.commit()
    session.close()

def verificar_registro_existente(cedula, tipo_comida):
    """Verifica si ya existe un registro para hoy"""
    hoy = datetime.now().date()
    session = Session()
    existe = session.query(RegistroComida).filter(
        RegistroComida.cedula_usuario == cedula,
        RegistroComida.tipo_comida == tipo_comida,
        RegistroComida.fecha_hora >= hoy
    ).first()
    session.close()
    return existe is not None


# Crear tablas al importar
Base.metadata.create_all(engine)