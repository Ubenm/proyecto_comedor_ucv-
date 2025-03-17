import streamlit as st
import streamlit_authenticator as stauth
from streamlit_option_menu import option_menu
import styles as sty
import yaml
from yaml.loader import SafeLoader
import datetime

# set layout page
st.set_page_config(
  page_title="Comedor UCV",
  page_icon=":knife_fork_plate:",
  layout="wide"
)
st.markdown(sty.css_login, unsafe_allow_html=True)

with open('config.yaml') as file:
  config = yaml.load(file, Loader=SafeLoader)
  
authenticator = stauth.Authenticate(
  config['credentials'],
  config['cookie']['name'],
  config['cookie']['key'],
  config['cookie']['expiry_days'],
  config['preauthorized']
)

# render login widget
name, authentication_status, username = authenticator.login(
  key='Login', location='main',
  fields= {'Form name':'Bienvenido', 'Username':'Usuario', 'Password':'Contraseña', 'Login':'Entrar'})

# into to the app
if authentication_status:
  if username in ['jcoello_admin','uluna_admin','jhernandez_admin']:
    st.title('Modulo de Administración')
    st.write(f'Welcome *{name}*')
    authenticator.logout('Salir', 'main')
    st.markdown(sty.css_button, unsafe_allow_html=True)
  else:
    # set margins
    st.markdown(sty.margin, unsafe_allow_html=True)
    
    st.markdown(sty.margin2, unsafe_allow_html=True)
    
    # set navbar and logo ucv
    co1,co2 = st.columns([0.15,0.85],vertical_alignment="top")
    with co1:
      logo=sty.logo()
      st.markdown(logo, unsafe_allow_html=True)
    
    with co2:
      navbar = option_menu(None, ["Inicio","Registro", "Consulta de Menú Semanal", "Info. de Contacto para Donaciones","Reseñas"], 
                          icons=["display",'menu-down', 'calendar-week', "info-circle", "list-stars"], 
                          menu_icon="cast", default_index=0, orientation="horizontal",
                          styles={
                          "container": {"padding": "0!important", "background-color": "rgba(13, 71, 161, 0.8)"},
                          "icon": {"color": "#ffffff", "font-size": "13px"},
                          "nav-link": {"font-size": "15px", "text-align": "left", "margin":"5px", "--hover-color": "rgba(13, 71, 161, 0.8)", "color":"#ffffff"},
                          "nav-link-selected": {"background-color": "rgba(0,38,78,0.6)"},
                          })
    # mensaje de bienvenida
    st.write(f'Bienvenido: ***{name}***')
    authenticator.logout('Salir', 'main')
    st.markdown(sty.css_button, unsafe_allow_html=True)
    # menus
    comidas = {'Desayuno':['Arepa con jugo de papelon', 'https://tofuu.getjusto.com/orioneat-local/resized2/32M3QTFQqFqCXk4CH-800-x.webp'],
               'Almuerzo':['Pabello Criollo con jugo de naranja', 'https://www.196flavors.com/wp-content/uploads/2013/04/pabellon-criollo-1fp.jpg'],
               'Cena':['Arroz chino con jugo de fresa', 'https://pedidos.palaciolungfung.com/web/image/product.template/4264/image_1024?unique=536f9f5']}
    background_image = sty.comedor_image()
    # variable global registro de usuario
    if not ('cedula' in st.session_state and 'registro' in st.session_state):
      st.session_state.cedula = False
      st.session_state.registro = False
    if navbar == 'Inicio':
      # Set the background image using CSS
      st.markdown(sty.main_image(), unsafe_allow_html=True)
      # Set the title of the app
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
      if not all([st.session_state.cedula, st.session_state.registro]):
        if cedula.strip().isdigit():
          st.session_state.cedula = True
        if not st.session_state.cedula and cedula != '':
          co2.error('Cédula invalida, ingrese solo numeros')
        # si cedula de usuario es validada subir registro al comedor
        if st.session_state.cedula:
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
    elif navbar == "Info. de Contacto para Donaciones":
      pass
    else:
      pass
elif authentication_status == False:
    st.error('Usuario o Contraseña invalida')
elif authentication_status == None:
    st.warning('Ingrese usuario y contraseña')





