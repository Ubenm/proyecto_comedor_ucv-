import streamlit as st
from streamlit_option_menu import option_menu
from database import (
    obtener_usuarios,
    insertar_usuario,
    eliminar_usuario,
    actualizar_usuario,
    verificar_login,
    poblar_base_datos
)
import styles as sty

# Configuración de la página
st.set_page_config(
    page_title="Comedor UCV",
    page_icon=":knife_fork_plate:",
    layout="wide"
)

background_image = sty.comedor_image()
# Sistema de autenticación
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_info = None

# Botón de cerrar sesión
if st.session_state.logged_in:
    if st.sidebar.button("🚪 Salir"):
        st.session_state.logged_in = False
        st.session_state.user_info = None
        st.rerun()

# Login
if not st.session_state.logged_in:
    #poblar_base_datos()  # Solo para desarrollo
    st.markdown(sty.css_login, unsafe_allow_html=True)
    st.title("Inicio de Sesión Comedor UCV")
    
    with st.form("Login"):
        cedula = st.text_input("Cédula")
        password = st.text_input("Contraseña", type="password")
        if st.form_submit_button("Ingresar"):
            usuario = verificar_login(cedula, password)
            if usuario:
                st.session_state.logged_in = True
                st.session_state.user_info = {
                    "nombre": usuario['nombre'],
                    "rol": usuario['rol'],
                    "cedula": usuario['cedula']
                }
                st.rerun()
            else:
                st.error("Credenciales incorrectas")            
    st.stop()

# Contenido principal según rol
if st.session_state.logged_in:
    # Navbar y logo
    co1, co2 = st.columns([0.15, 0.85], vertical_alignment="top")
    with co1:
        st.markdown(sty.logo(), unsafe_allow_html=True)
    
    with co2:
        menu_options = ["Inicio", "Registro", "Consulta de Menú Semanal", 
                       "Info. de Contacto para Donaciones", "Reseñas"]
        
        if st.session_state.user_info["rol"] == "administrador":
            menu_options.append("Gestión de Usuarios")
        
        navbar = option_menu(
            None, menu_options,
            icons=["house", "clipboard-check", "calendar", "info-circle", "chat", "gear"],
            menu_icon="cast", default_index=0, orientation="horizontal",
            styles={
                "container": {"background-color": "#0d47a1"},
                "nav-link": {"--hover-color": "#1565c0"},
                "nav-link-selected": {"background-color": "#0d47a1"}
            }
        )

    # Mensaje de bienvenida
    st.write(f'Bienvenido: ***{st.session_state.user_info["nombre"]}***')
    st.markdown(sty.css_button, unsafe_allow_html=True)

    # Funcionalidades comunes
    comidas = {
        'Desayuno': ['Arepa con jugo de papelon', 'https://tofuu.getjusto.com/orioneat-local/resized2/32M3QTFQqFqCXk4CH-800-x.webp'],
        'Almuerzo': ['Pabello Criollo con jugo de naranja', 'https://www.196flavors.com/wp-content/uploads/2013/04/pabellon-criollo-1fp.jpg'],
        'Cena': ['Arroz chino con jugo de fresa', 'https://pedidos.palaciolungfung.com/web/image/product.template/4264/image_1024?unique=536f9f5']
    }

    # Módulo de administración
    if navbar == "Gestión de Usuarios" and st.session_state.user_info["rol"] == "administrador":
        st.subheader("Panel de Administración")
        
        opcion = st.selectbox(
            "Acciones:",
            ["Ver usuarios", "Agregar usuario", "Editar usuario", "Eliminar usuario"]
        )
        
        if opcion == "Ver usuarios":
            usuarios = obtener_usuarios()
            st.table([{"Nombre": u.nombre, "Rol": u.rol, "Cédula": u.cedula} for u in usuarios])
        
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
                            actualizar_usuario(
                                cedula_editar,
                                nuevo_nombre,
                                nuevo_rol,
                                nueva_pass if nueva_pass else None
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

    # Funcionalidades para todos los usuarios
    elif navbar == 'Inicio':
        st.markdown(sty.main_image(), unsafe_allow_html=True)
        st.title("Servicio de Comedor")
        st.subheader("Universidad Central de Venezuela")

    elif navbar == 'Registro':
      st.markdown(background_image, unsafe_allow_html=True)
      co1,co2,co3,co4 = st.columns([0.3,0.3,0.2,0.2],vertical_alignment="top")
      # comidas a seleccionar para control de veces que el usuario asistira al comedor
      co1.write('*Seleccione las comidas que asistirá al comedor*')
      desayuno = co1.checkbox("Desayuno")
      almuerzo = co1.checkbox("Almuerzo")
      cena = co1.checkbox("Cena")
      cedula = co2.text_input(label='Ingrese su cédula para validar su asistencia', placeholder = 'cédula')
      if not all([st.session_state.user_info['cedula'], st.session_state.registro]):
        if cedula.strip().isdigit():
          st.session_state.user_info['cedula'] = True
        if not st.session_state.user_info['cedula'] and cedula != '':
          co2.error('Cédula invalida, ingrese solo numeros')
        # si cedula de usuario es validada subir registro al comedor
        if st.session_state.user_info['cedula']:
          if any([desayuno, almuerzo, cena]):
            co3.write('\n')
            if co3.button('Subir registro'):
              st.session_state.registro = True
              co2.write('Su registro fue subido satisfactoriamente, buen apetito :sunglasses:')
          else:
            co2.warning('Seleccione al menos una comida a ingerir')
      else:
        co2.write('Su registro fue subido satisfactoriamente, buen apetito :sunglasses:')
    elif navbar == "Consulta de Menú Semanal":
        st.markdown(background_image, unsafe_allow_html=True)
        co1,co2 = st.columns([0.3,0.7],vertical_alignment="top")
        opt_day = ['Lunes','Martes','Miercoles','Jueves','Viernes']
        opt_meal = ['Desayuno', 'Almuerzo', 'Cena']
        caption = ['De 7:00 am a 8:30 am', 'De 12:00 pm a 2:00 pm', 'De 6:00 pm a 7:30 pm']
        st.session_state['dia_menu'] = co1.selectbox('Día que desea consultar', opt_day, index = None, placeholder = 'Selecione un día')
        st.session_state['plato'] = co1.radio(label='Seleccione una opción:', options=opt_meal, captions=caption)
        if st.session_state['dia_menu'] != None:
            co2.subheader(f"Menú de {st.session_state['plato']} para el día {st.session_state['dia_menu']}:")
            co2.write('Descripción del menú: ' + comidas[st.session_state['plato']][0])
            img = """
            <style>.img2 {
            width:600px;
            height:500px;
            }
            </style>
            <img class = "img2" src= '%s' >""" % comidas[st.session_state['plato']][1]
            co2.markdown(img, unsafe_allow_html=True)