import streamlit as st
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

from database.models import Usuario
from database.database import get_db
from sqlalchemy.exc import IntegrityError
#from werkzeug.security import generate_password_hash

# Función para registro
def mostrar_formulario_registro():
    with st.form("registro_form", clear_on_submit=True):
        st.subheader("Registro de Usuario")
        nombre = st.text_input("Nombre completo")
        email = st.text_input("Correo electrónico")
        password = st.text_input("Contraseña", type="password")
        rol = st.selectbox("Rol", ["estudiante", "empleado", "admin"])
        
        if st.form_submit_button("Registrar"):
            if not all([nombre, email, password]):
                st.error("¡Todos los campos son obligatorios!")
                return

            try:
                db = next(get_db())
                nuevo_usuario = Usuario(
                    nombre=nombre,
                    email=email,
                    rol=rol
                )
                nuevo_usuario.set_password(password)
                db.add(nuevo_usuario)
                db.commit()
                st.success("Usuario registrado exitosamente ✅")
                
            except IntegrityError:
                db.rollback()
                st.error("⚠️ Este correo electrónico ya está registrado")
                
            except Exception as e:
                st.error(f"Error: {str(e)}")

