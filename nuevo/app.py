# app.py
import streamlit as st
from streamlit_option_menu import option_menu
from prueba import poblar_base_datos, verificar_login

# Configuración de la página
st.set_page_config(
    page_title="Comedor UCV",
    page_icon=":knife_fork_plate:",
    layout="wide"
)

# Estilos CSS
st.markdown("""
<style>
.block-container {
    padding-top: 0px;
    padding-bottom: 0rem;
    padding-left: 5rem;
    padding-right: 5rem;
}
.st-emotion-cache-12fmjuu {
    height: 0px;
}
</style>
""", unsafe_allow_html=True)

# Sistema de autenticación
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_info = None

# Botón de cerrar sesión
if st.session_state.logged_in:
    if st.sidebar.button("🚪 Cerrar sesión"):
        st.session_state.logged_in = False
        st.session_state.user_info = None
        st.rerun()

# Login
if not st.session_state.logged_in:
    #poblar_base_datos()  # Solo en desarrollo, quitar en producción
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

# Contenido principal
if st.session_state.logged_in:
    # Navbar y logo
    col1, col2 = st.columns([0.15, 0.85])
    with col1:
        st.image("https://upload.wikimedia.org/wikipedia/commons/f/f4/Logo_Universidad_Central_de_Venezuela.svg", width=120)
    
    with col2:
        menu_options = ["Inicio", "Reserva de Turnos", "Consulta de Menú Semanal", 
                       "Info. de Contacto para Donaciones", "Reseñas"]
        
        if st.session_state.user_info["rol"] == "administrador":
            menu_options.append("Gestión de Usuarios")
        
        navbar = option_menu(
            None, menu_options,
            icons=["house", "clock", "calendar", "info-circle", "chat", "gear"],
            menu_icon="cast", default_index=0, orientation="horizontal",
            styles={
                "container": {"background-color": "#0d47a1"},
                "nav-link": {"--hover-color": "#1565c0"},
                "nav-link-selected": {"background-color": "#0d47a1"}
            }
        )

    # Contenido según sección
    if navbar == "Inicio":
        st.markdown("""
        <style>
        .stApp {
            background-image: url("http://www.ucv.ve/fileadmin/templates/core/img/img_carrusel/1_UCV_CIUDAD_UNIVERSITARIA_DE_CARACAS_F_JUAN_PEREZ_HERNANDEZ.png");
            background-size: cover;
        }
        </style>
        """, unsafe_allow_html=True)
        st.title("Bienvenido al Comedor UCV")
        st.subheader(f"Usuario: {st.session_state.user_info['nombre']}")

    # Añadir aquí el resto de las secciones...