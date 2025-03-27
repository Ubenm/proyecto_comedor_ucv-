import streamlit as st
from streamlit_option_menu import option_menu
from sqlalchemy import create_engine, Column, Integer, String, Boolean, Date
from sqlalchemy.orm import declarative_base, sessionmaker
import bcrypt
import datetime
import styles as sty

# ------------------------- Configuración de Bases de Datos -------------------------
Base_usuarios = declarative_base()
Base_menu = declarative_base()

# Modelo para usuarios.db
class Usuario(Base_usuarios):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String, nullable=False)
    rol = Column(String, nullable=False)
    cedula = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    banderin = Column(Boolean, default=False)

# Modelo para menu.db
class MenuDia(Base_menu):
    __tablename__ = "menus"
    id = Column(Integer, primary_key=True, autoincrement=True)
    fecha = Column(Date, nullable=False)
    tipo_comida = Column(String, nullable=False)
    descripcion = Column(String, nullable=False)
    imagen_url = Column(String)
    cantidad_disponible = Column(Integer, nullable=False)

# Configurar motores de bases de datos
engine_usuarios = create_engine("sqlite:///usuarios.db")
engine_menu = create_engine("sqlite:///menu.db")

# Crear tablas si no existen
Base_usuarios.metadata.create_all(engine_usuarios)
Base_menu.metadata.create_all(engine_menu)

# Configurar sesiones
Session_usuarios = sessionmaker(bind=engine_usuarios)
Session_menu = sessionmaker(bind=engine_menu)

# ------------------------- Funciones Esenciales -------------------------
def poblar_usuarios_iniciales():
    usuarios = [
        ("Admin Revolucionario", "administrador", "001", "admin123"),
        ("Trabajador Ejemplar", "trabajador", "201", "trab123"),
        ("Ciudadano Modelo", "comensal", "101", "comensal123")
    ]
    
    with Session_usuarios() as session:
        for nombre, rol, cedula, password in usuarios:
            if not session.query(Usuario).filter_by(cedula=cedula).first():
                hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                usuario = Usuario(
                    nombre=nombre,
                    rol=rol,
                    cedula=cedula,
                    password_hash=hashed_pw
                )
                session.add(usuario)
        session.commit()



# ------------------------- Configuración de la Aplicación -------------------------
st.set_page_config(
    page_title="Comedor Popular Socialista",
    page_icon=":knife_fork_plate:",
    layout="wide"
)
st.markdown(sty.css_login, unsafe_allow_html=True)

# ------------------------- Sistema de Autenticación -------------------------
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_info = None

# ------------------------- Módulo de Administración -------------------------
def modulo_administrador():
    st.subheader("Gestión Revolucionaria del Pueblo")
    
    opcion = st.selectbox(
        "Acciones Administrativas:",
        ["Cargar Menú Diario", "Ver Stock Alimenticio", "Gestionar Ciudadanos"]
    )
    
    if opcion == "Cargar Menú Diario":
        with st.form("Formulario Menú"):
            fecha = st.date_input("Fecha del menú", value=datetime.date.today())
            tipo_comida = st.selectbox("Tipo de comida", ["Desayuno", "Almuerzo", "Cena"])
            descripcion = st.text_area("Descripción del menú")
            imagen_url = st.text_input("URL de la imagen (opcional)")
            cantidad = st.number_input("Raciones disponibles", min_value=1, value=150)
            
            if st.form_submit_button("Publicar para el Pueblo"):
                with Session_menu() as session:
                    nuevo_menu = MenuDia(
                        fecha=fecha,
                        tipo_comida=tipo_comida,
                        descripcion=descripcion,
                        imagen_url=imagen_url,
                        cantidad_disponible=cantidad
                    )
                    session.add(nuevo_menu)
                    session.commit()
                st.success("¡El pueblo tendrá su alimento!")
    
    elif opcion == "Ver Stock Alimenticio":
        fecha_consulta = st.date_input("Consultar stock para:")
        with Session_menu() as session:
            menus = session.query(MenuDia).filter(MenuDia.fecha == fecha_consulta).all()
            if menus:
                st.table([{
                    "Comida": m.tipo_comida,
                    "Raciones": m.cantidad_disponible,
                    "Menú": m.descripcion
                } for m in menus])
            else:
                st.warning("No hay registros para esta fecha")
    
    elif opcion == "Gestionar Ciudadanos":
        # (Implementar CRUD de usuarios similar a versiones anteriores)
        pass

# ------------------------- Módulo de Trabajadores -------------------------
def modulo_trabajador():
    st.subheader("Control de Distribución Proletaria")
    
    col1, col2 = st.columns([0.4, 0.6])
    with col1:
        cedula = st.text_input("Cédula del Ciudadano")
        if cedula:
            with Session_usuarios() as session:
                usuario = session.query(Usuario).filter(Usuario.cedula == cedula).first()
                
                if not usuario:
                    st.error("¡Ciudadano no registrado!")
                    return
                
                if usuario.banderin:
                    st.warning("¡Ya recibió su ración diaria!")
                    return
                
                st.success("Acceso autorizado")
                
            if st.button("Registrar consumo"):
                with Session_usuarios() as session:
                    usuario = session.query(Usuario).filter(Usuario.cedula == cedula).first()
                    usuario.banderin = True
                    session.commit()
                
                with Session_menu() as session:
                    menu = session.query(MenuDia).filter(
                        MenuDia.fecha == datetime.date.today(),
                        MenuDia.tipo_comida == "Almuerzo"
                    ).first()
                    menu.cantidad_disponible -= 1
                    session.commit()
                
                st.rerun()

# ------------------------- Módulo de Comensales -------------------------
def modulo_comensal():
    st.subheader("Derechos Alimenticios del Ciudadano")
    
    with Session_usuarios() as session:
        usuario = session.query(Usuario).filter(
            Usuario.cedula == st.session_state.user_info['cedula']
        ).first()
        
        st.markdown(f"""
        **Estado de consumo:**  
        {"✅ Ya has recibido tu ración" if usuario.banderin else "⚠️ Pendiente de recibir"}
        """)
    
    with Session_menu() as session:
        menus = session.query(MenuDia).filter(
            MenuDia.fecha == datetime.date.today()
        ).all()
        
        for menu in menus:
            with st.expander(f"{menu.tipo_comida} - {menu.cantidad_disponible} raciones"):
                col1, col2 = st.columns([0.7, 0.3])
                with col1:
                    st.markdown(f"**Menú:** {menu.descripcion}")
                with col2:
                    if menu.imagen_url:
                        st.image(menu.imagen_url, width=200)

# ------------------------- Interfaz Principal -------------------------
def main():
    poblar_usuarios_iniciales()
    
    if not st.session_state.logged_in:
        st.title("Bienvenido al Comedor Popular")
        
        with st.form("Login Revolucionario"):
            cedula = st.text_input("Cédula")
            password = st.text_input("Contraseña", type="password")
            
            if st.form_submit_button("Ingresar"):
                with Session_usuarios() as session:
                    usuario = session.query(Usuario).filter(
                        Usuario.cedula == cedula
                    ).first()
                    
                    if usuario and bcrypt.checkpw(password.encode('utf-8'), usuario.password_hash):
                        st.session_state.logged_in = True
                        st.session_state.user_info = {
                            "nombre": usuario.nombre,
                            "rol": usuario.rol,
                            "cedula": usuario.cedula
                        }
                        st.rerun()
                    else:
                        st.error("¡Credenciales incorrectas, camarada!")
    
    else:
        # Barra de navegación
        co1, co2 = st.columns([0.15, 0.85])
        with co1:
            st.markdown(sty.logo(), unsafe_allow_html=True)
        
        with co2:
            menu_items = ["Inicio", "Estado Alimenticio"]
            if st.session_state.user_info["rol"] == "administrador":
                menu_items.append("Administración")
            elif st.session_state.user_info["rol"] == "trabajador":
                menu_items.append("Control de Acceso")
            
            navbar = option_menu(
                None, menu_items,
                icons=["house", "clipboard-check", "gear", "shield-check"],
                menu_icon="cast", 
                orientation="horizontal"
                #styles=sty.NAVBAR_STYLES
            )
        
        # Contenido según rol
        if navbar == "Administración" and st.session_state.user_info["rol"] == "administrador":
            modulo_administrador()
        elif navbar == "Control de Acceso" and st.session_state.user_info["rol"] == "trabajador":
            modulo_trabajador()
        else:
            modulo_comensal()

        # Botón de cierre de sesión
        if st.sidebar.button("🚪 Cerrar sesión revolucionaria"):
            st.session_state.logged_in = False
            st.session_state.user_info = None
            st.rerun()

if __name__ == "__main__":
    main()