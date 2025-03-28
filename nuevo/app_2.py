import streamlit as st
from streamlit_option_menu import option_menu
from sqlalchemy import create_engine, Column, Integer, String, Boolean, Date
from sqlalchemy.orm import declarative_base, sessionmaker
import bcrypt
import datetime
import styles as sty
from database import (
    obtener_usuarios,
    insertar_usuario,
    eliminar_usuario,
    actualizar_usuario,
    verificar_login,
    poblar_base_datos)
from database_menu import (insertar_menu, obtener_menus, actualizar_menu, eliminar_menu)

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
    desayuno_comido = Column(Boolean, default=False)
    almuerzo_comido = Column(Boolean, default=False)
    cena_comido = Column(Boolean, default=False)

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
def modulo_administrador_menus():
    st.subheader("Gestión Revolucionaria de Menús")
    
    opcion = st.selectbox(
        "Operaciones",
        ["Ver todos", "Agregar", "Editar", "Eliminar"]
    )
    
    # Ver todos los menús
    if opcion == "Ver todos":
        menus = obtener_menus()
        st.table([{
            "Fecha": m.fecha.strftime("%d/%m/%Y"),
            "Comida": m.tipo_comida,
            "Descripción": m.descripcion,
            "Disponibles": m.cantidad_disponible
        } for m in menus])
    
    # Agregar nuevo menú
    elif opcion == "Agregar":
        with st.form("Nuevo menú"):
            fecha = st.date_input("Fecha")
            tipo = st.selectbox("Tipo comida", ["Desayuno", "Almuerzo", "Cena"])
            desc = st.text_area("Descripción")
            img = st.text_input("URL Imagen")
            cant = st.number_input("Cantidad", min_value=1)
            
            if st.form_submit_button("Guardar"):
                try:
                    insertar_menu(fecha, tipo, desc, img, cant)
                    st.success("¡Menú añadido!")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    # Editar menú existente
    elif opcion == "Editar":
        menus = obtener_menus()
        menu_sel = st.selectbox("Seleccionar menú", 
                              [f"{m.id} | {m.fecha} - {m.tipo_comida}" for m in menus])
        
        if menu_sel:
            id_menu = int(menu_sel.split("|")[0].strip())
            with Session_menu() as session:
                menu = session.get(MenuDia, id_menu)
                
                with st.form("Editar"):
                    nueva_desc = st.text_area("Descripción", value=menu.descripcion)
                    nueva_img = st.text_input("Imagen", value=menu.imagen_url)
                    nueva_cant = st.number_input("Cantidad", 
                                               value=menu.cantidad_disponible,
                                               min_value=0)
                    
                    if st.form_submit_button("Actualizar"):
                        actualizar_menu(id_menu, {
                            "descripcion": nueva_desc,
                            "imagen_url": nueva_img,
                            "cantidad_disponible": nueva_cant
                        })
                        st.success("¡Actualización exitosa!")
    
    # Eliminar menú
    elif opcion == "Eliminar":
        menus = obtener_menus()
        menu_sel = st.selectbox("Seleccionar menú a eliminar", 
                              [f"{m.fecha} - {m.tipo_comida} - {m.descripcion}" for m in menus])
        
        if st.button("Confirmar eliminación"):
            fecha, tipo, descripcion = menu_sel.split(" - ")
            with Session_menu() as session:
                menu = session.query(MenuDia).filter(
                    MenuDia.fecha == datetime.datetime.strptime(fecha, "%Y-%m-%d").date(),
                    MenuDia.tipo_comida == tipo,
                    MenuDia.descripcion == descripcion
                ).first()
                eliminar_menu(menu.id)
                st.success("¡Menú eliminado!")
    
def gestion_de_usuarios():
        st.subheader("Panel de Administración")
        
        opcion = st.selectbox(
            "Acciones:",
            ["Ver usuarios", "Agregar usuario", "Editar usuario", "Eliminar usuario"]
        )
        
        if opcion == "Ver usuarios":
            usuarios = obtener_usuarios()
            st.table([{"Nombre": u.nombre, "Rol": u.rol, "Cédula": u.cedula, 'Desayuno':u.desayuno_comido} for u in usuarios])
        
        elif opcion == "Agregar usuario":
            with st.form("Agregar"):
                nombre = st.text_input("Nombre completo")
                rol = st.selectbox("Rol", ["administrador", "trabajador", "comensal"])
                cedula = st.text_input("Cédula")
                password = st.text_input("Contraseña", type="password")
                
                if st.form_submit_button("Guardar"):
                    try:
                        insertar_usuario(nombre, rol, cedula, password)
                        st.success("Usuario creado!")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
        
        elif opcion == "Editar usuario":
            cedula_editar = st.text_input("Ingrese cédula del usuario a editar")
            if cedula_editar:
                usuario = next((u for u in obtener_usuarios() if u.cedula == cedula_editar), None)
                
                if usuario:
                    with st.form("Editar"):
                        nuevo_nombre = st.text_input("Nombre", value=usuario.nombre)
                        nuevo_rol = st.selectbox("Rol", 
                                            ["administrador", "trabajador", "comensal"],
                                            index=["administrador", "trabajador", "comensal"].index(usuario.rol))
                        nueva_pass = st.text_input("Nueva contraseña (dejar vacío para mantener)", type="password")
                       # nuevo_band = st.selectbox("Banderin", [True, False], index=[True, False].index(usuario.banderin))
                        if st.form_submit_button("Actualizar"):
                            actualizar_usuario(
                                cedula_editar,
                                nuevo_nombre,
                                nuevo_rol,
                                nueva_pass if nueva_pass else None
                               # nuevo_band
                            )
                            st.success("Usuario actualizado!")
                else:
                    st.error("Usuario no encontrado")
        
        elif opcion == "Eliminar usuario":
            cedula_eliminar = st.text_input("Ingrese cédula del usuario a eliminar")
            if cedula_eliminar:
                if st.button("Confirmar eliminación"):
                    eliminar_usuario(cedula_eliminar)
                    st.success("Usuario eliminado del sistema")

# ------------------------- Módulo de Trabajadores -------------------------
def modulo_trabajador():
    st.subheader("Control de Distribución Proletaria")
    
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
        
        # Verificar existencia del menú primero
        with Session_menu() as session:


            tipo_comida = st.selectbox("Tipo de comida", ["Desayuno", "Almuerzo", "Cena"])

            menu = session.query(MenuDia).filter(
                (MenuDia.fecha == datetime.date.today()) and (MenuDia.tipo_comida==tipo_comida)  # Asegurar coincidencia exacta
            ).first()
                  
            if not menu:
                st.error("⚠️ El menú del día no ha sido cargado")
                return
                
            if menu.cantidad_disponible <= 0:
                st.error("¡No hay raciones disponibles!")
                return
        
        if st.button("Registrar consumo"):
            
            try:
                # Actualizar usuario
                with Session_usuarios() as session:
                    usuario = session.query(Usuario).filter(Usuario.cedula == cedula).first()
                    usuario.banderin = True
                    session.commit()
                
                # Actualizar menú
                with Session_menu() as session:
                    menu = session.query(MenuDia).filter((MenuDia.fecha == datetime.date.today())and
                                                         (MenuDia.tipo_comida==tipo_comida)).first()
                    
                    menu.cantidad_disponible -= 1
                    session.commit()
                    
                st.success("¡Consumo registrado con éxito!")
                st.rerun()
                
            except Exception as e:
                st.error(f"Error revolucionario: {str(e)}")
                session.rollback()

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
    #poblar_usuarios_iniciales()
    
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
                menu_items.append("Administración de menús")
                menu_items.append("Gestionar Ciudadanos")
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
        if navbar == "Administración de menús" and st.session_state.user_info["rol"] == "administrador":
            modulo_administrador_menus()
        elif navbar == "Gestionar Ciudadanos" and st.session_state.user_info["rol"] == "administrador":
            gestion_de_usuarios()
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