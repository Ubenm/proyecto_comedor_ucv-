import streamlit as st
from models import Usuario
from database import get_db
from sqlalchemy.exc import SQLAlchemyError

def mostrar_formulario_login():
    with st.form("login_form", clear_on_submit=True):
        st.subheader("Inicio de Sesión")
        email = st.text_input("Correo electrónico")
        password = st.text_input("Contraseña", type="password")
        
        if st.form_submit_button("Ingresar"):
            if not all([email, password]):
                st.error("¡Correo y contraseña son obligatorios!")
                return
            
            try:
                db = next(get_db())
                usuario = db.query(Usuario).filter(Usuario.email == email).first()
                
                if usuario and usuario.check_password(password):
                    st.session_state["autenticado"] = True
                    st.session_state["usuario"] = {
                        "email": usuario.email,
                        "rol": usuario.rol  # Si existe el campo "rol"
                    }
                    st.success("¡Inicio de sesión exitoso! ✅")
                    st.rerun()  # Actualizar la interfaz
                else:
                    st.error("Credenciales incorrectas ⚠️")
                    
            except SQLAlchemyError as e:
                st.error(f"Error de base de datos: {str(e)}")