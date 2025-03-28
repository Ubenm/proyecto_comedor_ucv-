import streamlit as st
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker
import bcrypt

# Configuración de SQLAlchemy
DATABASE_URL = "sqlite:///usuarios.db"  # Base de datos SQLite local
engine = create_engine(DATABASE_URL, echo=False)  # Motor de la base de datos
Base = declarative_base()  # Base para los modelos
Session = sessionmaker(bind=engine)  # Sesión para interactuar con la base de datos

# Definición del modelo de usuario
class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String, nullable=False)
    rol = Column(String, nullable=False)
    cedula = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    
    def verificar_password(self, password):
        """Verifica si la contraseña coincide con el hash almacenado"""
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash)

# Crear la tabla si no existe
engine_usuarios = create_engine("sqlite:///usuarios.db", echo=False)
Base.metadata.create_all(engine_usuarios)

# Funciones de utilidad
def insertar_usuario(nombre, rol, cedula, password):
    """Inserta un nuevo usuario en la base de datos"""
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    usuario = Usuario(nombre=nombre, rol=rol, cedula=cedula, password_hash=password_hash)
    session = Session()
    session.add(usuario)
    session.commit()
    session.close()

def verificar_login(cedula, password):
    """Verifica las credenciales del usuario"""
    session = Session()
    usuario = session.query(Usuario).filter(Usuario.cedula == cedula).first()
    session.close()
    
    if usuario and usuario.verificar_password(password):
        return {"nombre": usuario.nombre, "rol": usuario.rol, "cedula": usuario.cedula}
    return None

def obtener_usuarios():
    """Obtiene todos los usuarios de la base de datos"""
    session = Session()
    usuarios = session.query(Usuario).all()
    session.close()
    return usuarios

def eliminar_usuario(cedula):
    """Elimina un usuario por su cédula"""
    session = Session()
    usuario = session.query(Usuario).filter(Usuario.cedula == cedula).first()
    if usuario:
        session.delete(usuario)
        session.commit()
    session.close()

def actualizar_usuario(cedula, nombre=None, rol=None, password=None, banderin=None):
    """Actualiza los datos de un usuario"""
    session = Session()
    usuario = session.query(Usuario).filter(Usuario.cedula == cedula).first()
    if usuario:
        if nombre:
            usuario.nombre = nombre
        if rol:
            usuario.rol = rol
        if password:
            usuario.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        usuario.banderin = banderin
        session.commit()
    session.close()

def poblar_base_datos():
    """Pobla la base de datos con usuarios de prueba"""
    usuarios_prueba = [
        ("Admin1", "administrador", "001", "admin123"),
        ("Comensal1", "comensal", "101", "comensal123"),
        ("Trabajador1", "trabajador", "201", "trab123"),
        ("Juan Pérez", "comensal", "102", "1234"),
        ("María García", "trabajador", "202", "5678")
    ]
    
    for usuario in usuarios_prueba:
        try:
            insertar_usuario(*usuario)
        except:
            continue  # Si el usuario ya existe, lo saltamos

# Módulo de manipulación de tablas para el administrador
def modulo_administrador():
    st.subheader("Gestión de Usuarios")
    
    # Opciones de gestión
    opcion = st.selectbox(
        "Seleccione una acción",
        ["Ver usuarios", "Agregar usuario", "Editar usuario", "Eliminar usuario"]
    )
    
    if opcion == "Ver usuarios":
        st.write("Lista de usuarios registrados:")
        usuarios = obtener_usuarios()
        st.table([{"Nombre": u.nombre, "Rol": u.rol, "Cédula": u.cedula} for u in usuarios])
    
    elif opcion == "Agregar usuario":
        st.write("Agregar nuevo usuario:")
        with st.form("Agregar usuario"):
            nombre = st.text_input("Nombre")
            rol = st.selectbox("Rol", ["administrador", "comensal", "trabajador"])
            cedula = st.text_input("Cédula")
            password = st.text_input("Contraseña", type="password")
            submit_button = st.form_submit_button("Agregar")
            
            if submit_button:
                try:
                    insertar_usuario(nombre, rol, cedula, password)
                    st.success("Usuario agregado correctamente.")
                except Exception as e:
                    st.error(f"Error al agregar usuario: {e}")
    
    elif opcion == "Editar usuario":
        st.write("Editar usuario existente:")
        cedula_editar = st.text_input("Cédula del usuario a editar")
        if cedula_editar:
            usuario = next((u for u in obtener_usuarios() if u.cedula == cedula_editar), None)
            if usuario:
                with st.form("Editar usuario"):
                    nuevo_nombre = st.text_input("Nombre", value=usuario.nombre)
                    nuevo_rol = st.selectbox("Rol", ["administrador", "comensal", "trabajador"], index=["administrador", "comensal", "trabajador"].index(usuario.rol))
                    nueva_password = st.text_input("Nueva contraseña (dejar en blanco para no cambiar)", type="password")
                    submit_button = st.form_submit_button("Actualizar")
                    
                    if submit_button:
                        actualizar_usuario(cedula_editar, nuevo_nombre, nuevo_rol, nueva_password)
                        st.success("Usuario actualizado correctamente.")
            else:
                st.error("Usuario no encontrado.")
    
    elif opcion == "Eliminar usuario":
        st.write("Eliminar usuario:")
        cedula_eliminar = st.text_input("Cédula del usuario a eliminar")
        if cedula_eliminar:
            if st.button("Eliminar"):
                eliminar_usuario(cedula_eliminar)
                st.success("Usuario eliminado correctamente.")

def main():
    st.title("Sistema de Login con SQLAlchemy")
    
    # Poblar datos de prueba
    poblar_base_datos()
    
    # Inicializar estado de sesión
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.user_info = None

    # Mostrar formulario de login si no está autenticado
    if not st.session_state.logged_in:
        with st.form("Login"):
            cedula = st.text_input("Número de cédula")
            password = st.text_input("Contraseña", type="password")
            submit_button = st.form_submit_button("Ingresar")

            if submit_button:
                usuario = verificar_login(cedula, password)
                if usuario:
                    st.session_state.logged_in = True
                    st.session_state.user_info = usuario
                    st.rerun()
                else:
                    st.error("Credenciales incorrectas. Intente nuevamente.")

    # Mostrar contenido según el rol si está autenticado
    else:
        st.success(f"✅ Bienvenido {st.session_state.user_info['nombre']}")
        st.subheader(f"Panel de {st.session_state.user_info['rol'].capitalize()}")
        
        # Contenido para Administrador
        if st.session_state.user_info["rol"] == "administrador":
            modulo_administrador()

        # Contenido para Trabajador
        elif st.session_state.user_info["rol"] == "trabajador":
            st.write("Funcionalidades para trabajadores:")
            st.write("- Registrar pedidos")
            st.write("- Ver horarios")
            st.write("- Gestión de mesas")

        # Contenido para Comensal
        elif st.session_state.user_info["rol"] == "comensal":
            st.write("Bienvenido comensal:")
            st.write("- Ver menú")
            st.write("- Hacer pedido")
            st.write("- Llamar al mesero")

        # Botón de logout
        if st.button("Cerrar sesión"):
            st.session_state.logged_in = False
            st.session_state.user_info = None
            st.rerun()

if __name__ == "__main__":
    main()