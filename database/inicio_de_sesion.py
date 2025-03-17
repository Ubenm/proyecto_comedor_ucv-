# app_streamlit.py
import streamlit as st
from database import SessionLocal, Usuario
from werkzeug.security import check_password_hash

# Función de login
def login():
    with st.form("login_form"):
        email = st.text_input("Correo electrónico")
        password = st.text_input("Contraseña", type="password")
        submitted = st.form_submit_button("Iniciar Sesión")

        if submitted:
            db = Session()
            usuario = db.query(Usuario).filter(Usuario.email == email).first()
            
            if usuario and check_password_hash(usuario.password_hash, password):
                st.session_state["autenticado"] = True
                st.session_state["usuario"] = usuario.email
                st.success("¡Inicio de sesión exitoso! ✅")
                st.rerun()
            else:
                st.error("Credenciales incorrectas ⚠️")

# Interfaz
if "autenticado" not in st.session_state:
    st.title("Login Comedor UCV 🍴")
    login()
else:
    st.title(f"Bienvenido, {st.session_state.usuario}!")
    if st.button("Cerrar Sesión"):
        st.session_state.clear()
        st.rerun()