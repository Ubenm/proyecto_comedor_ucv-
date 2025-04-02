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
from database_menu import (insertar_menu, obtener_menus, actualizar_menu, eliminar_menu, restar_racion)
from registro_de_comidas import (
    obtener_registros_comida,
    actualizar_registro_comida,
    eliminar_registro_comida,
    crear_registro_comida,
    verificar_registro_existente
)

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

# ------------------------- Configuración de la Aplicación -------------------------
st.set_page_config(
    page_title="Comedor UCV",
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
    st.subheader("Gestión de Menús")
    
    opcion = st.selectbox(
        "Operaciones",
        ["Ver todos", "Agregar", "Editar", "Eliminar"]
    )
    
    if opcion == "Ver todos":
        menus = obtener_menus()
        st.table([{
            "Fecha": m.fecha.strftime("%d/%m/%Y"),
            "Comida": m.tipo_comida,
            "Descripción": m.descripcion,
            "Disponibles": m.cantidad_disponible
        } for m in menus])
    
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
        st.table([{
            "Nombre": u.nombre, 
            "Rol": u.rol, 
            "Cédula": u.cedula,
        } for u in usuarios])
    
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

                    if st.form_submit_button("Actualizar"):
                        with Session_usuarios() as session:
                            usuario_actualizado = session.query(Usuario).filter_by(cedula=cedula_editar).first()
                            usuario_actualizado.nombre = nuevo_nombre
                            usuario_actualizado.rol = nuevo_rol
                            if nueva_pass:
                                usuario_actualizado.password_hash = bcrypt.hashpw(nueva_pass.encode('utf-8'), bcrypt.gensalt())
                            session.commit()
                        st.success("Usuario actualizado!")
            else:
                st.error("Usuario no encontrado")
    
    elif opcion == "Eliminar usuario":
        cedula_eliminar = st.text_input("Ingrese cédula del usuario a eliminar")
        if cedula_eliminar:
            if st.button("Confirmar eliminación"):
                eliminar_usuario(cedula_eliminar)
                st.success("Usuario eliminado del sistema")
    

def gestionar_registros():
    st.subheader("Gestión Central de Registros")
    
    registros = obtener_registros_comida()
    st.write("Registros históricos:")
    st.table([{
        "ID": r.id,
        "Cédula": r.cedula_usuario,
        "Fecha": r.fecha_hora.strftime("%d/%m/%Y"),
        "Comida": r.tipo_comida,
        "Descipción": r.descripcion_menu
    } for r in registros])
    
    st.divider()
    registro_id = st.number_input("ID del Registro a Editar", min_value=1)
    
    if registro_id:
        registro = next((r for r in registros if r.id == registro_id), None)
        if registro:
            nuevos_datos = {
                "cedula_usuario": st.text_input("Cédula", value=registro.cedula_usuario),
                "tipo_comida": st.selectbox(
                    "Tipo Comida", 
                    ["Desayuno", "Almuerzo", "Cena"],
                    index=["Desayuno", "Almuerzo", "Cena"].index(registro.tipo_comida)
                ),
                "descripcion_menu": st.text_area("Descripción", value=registro.descripcion_menu)
            }
            
            if st.button("Actualizar Registro"):
                actualizar_registro_comida(registro_id, nuevos_datos)
                st.success("¡Registro actualizado!")
                
            if st.button("Eliminar Registro", type="primary"):
                eliminar_registro_comida(registro_id)
                st.success("¡Registro eliminado!")

# ------------------------- Módulo de Trabajadores -------------------------
def modulo_trabajador():
    st.subheader("Registro de Consumo")
    
    cedula = st.text_input("Cédula del usuario")
    tipo_comida = st.selectbox("Tipo de Comida", ["Desayuno", "Almuerzo", "Cena"])
    
    if cedula and tipo_comida:
        # Paso 1: Verificar si es usuario válido
        usuarios = [u.cedula for u in obtener_usuarios()]
        if cedula not in usuarios:
            st.error("¡Usuario no registrado en el sistema!")
            return
            
        # Paso 2: Verificar registro previo
        if verificar_registro_existente(cedula, tipo_comida):
            st.error("¡Ya registró este consumo hoy!")
            return
            
        # Paso 3: Restar ración y crear registro
        if st.button("Registrar consumo"):
            if restar_racion(tipo_comida):
                if crear_registro_comida(cedula, tipo_comida):
                    st.success("✅ Consumo registrado exitosamente")
                    st.balloons()
                else:
                    st.error("Error al crear registro")
            else:
                st.error("¡No hay raciones disponibles o menú no configurado!")
# ------------------------- Módulo de Comensales -------------------------
def modulo_comensal():
    st.subheader("Estado de Consumo Diario")
    
    cedula = st.session_state.user_info['cedula']
    hoy = datetime.date.today()
    
    # Obtener registros de comida del usuario actual
    registros = obtener_registros_comida()
    consumos_hoy = [
        r for r in registros 
        if r.cedula_usuario == cedula 
        and r.fecha_hora.date() == hoy
    ]
    
    # Mostrar estado
    st.markdown(f"""
    **Estado de consumo:**  
    {"✅ Ya has recibido tu ración hoy" if consumos_hoy else "⚠️ Pendiente de recibir"}
    """)
    
    # Mostrar menús disponibles
    with Session_menu() as session:
        menus = session.query(MenuDia).filter(
            MenuDia.fecha == hoy
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
        st.title("Bienvenido al Comedor")
        
        with st.form("Login"):
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
                        st.error("¡Credenciales incorrectas!")
    
    else:
        # Barra de navegación
        co1, co2 = st.columns([0.15, 0.85])
        with co1:
            st.markdown(sty.logo(), unsafe_allow_html=True)
        
        with co2:
            menu_items = ["Inicio", "Estado Alimenticio"]
            if st.session_state.user_info["rol"] == "administrador":
                menu_items.append("Administración de menús")
                menu_items.append("Gestionar Usuarios")
                menu_items.append("Gestionar Registros")

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
        elif navbar == "Gestionar Usuarios" and st.session_state.user_info["rol"] == "administrador":
            gestion_de_usuarios()
        elif navbar == "Gestionar Registros" and st.session_state.user_info["rol"] == "administrador":
            gestionar_registros()
        elif navbar == "Control de Acceso" and st.session_state.user_info["rol"] == "trabajador":
            modulo_trabajador()
        else:
            modulo_comensal()

        # Botón de cierre de sesión
        if st.sidebar.button("🚪 Cerrar sesión"):
            st.session_state.logged_in = False
            st.session_state.user_info = None
            st.rerun()

if __name__ == "__main__":
    main()