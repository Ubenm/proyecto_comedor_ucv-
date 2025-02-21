import streamlit as st
from streamlit_option_menu import option_menu
from creacion_usuario import mostrar_formulario_registro

# sit layout page
st.set_page_config(
  page_title="Comedor UCV",
  page_icon=":knife_fork_plate:",
  layout="wide"
)

# set margins
st.markdown("""
<style>
.block-container {
  padding-top: 0px;
  padding-bottom: 0rem;
  padding-left: 5rem;
  padding-right: 5rem;
  }
</style>
""", unsafe_allow_html=True)

st.markdown('''
<style>
.st-emotion-cache-12fmjuu {
  position: fixed;
  top: 0px;
  left: 0px;
  right: 0px;
  height: 0px;
  background: rgb(255, 255, 255);
  outline: none;
  z-index: 999990;
  display: block;
  }
</style>
''', unsafe_allow_html=True)

# set navbar and logo ucv
co1,co2 = st.columns([0.15,0.85],vertical_alignment="top")
with co1:
  logo = """
    <style>.img {
      float:left;
      width:120px;
      height:115px;
    }</style>
    <img class = 'img' src="https://upload.wikimedia.org/wikipedia/commons/f/f4/Logo_Universidad_Central_de_Venezuela.svg">"""
  st.markdown(logo, unsafe_allow_html=True)

with co2:
  navbar = option_menu(None, ["Inicio","Reserva de Turnos", "Consulta de Menú Semanal", "Info. de Contacto para Donaciones","Reseñas","Registro de Usuarios"], 
                      icons=["display",'menu-down', 'calendar-week', "info-circle", "list-stars"], 
                      menu_icon="cast", default_index=0, orientation="horizontal",
                      styles={
                      "container": {"padding": "0!important", "background-color": "rgba(13, 71, 161, 0.8)"},
                      "icon": {"color": "#ffffff", "font-size": "13px"},
                      "nav-link": {"font-size": "15px", "text-align": "left", "margin":"5px", "--hover-color": "rgba(13, 71, 161, 0.8)", "color":"#ffffff"},
                      "nav-link-selected": {"background-color": "rgba(0,38,78,0.6)"},
                      })
# menus
comidas = {'Desayuno':['Arepa con jugo de papelon', 'https://tofuu.getjusto.com/orioneat-local/resized2/32M3QTFQqFqCXk4CH-800-x.webp'],
           'Almuerzo':['Pabello Criollo con jugo de naranja', 'https://www.196flavors.com/wp-content/uploads/2013/04/pabellon-criollo-1fp.jpg'],
           'Cena':['Arroz chino con jugo de fresa', 'https://pedidos.palaciolungfung.com/web/image/product.template/4264/image_1024?unique=536f9f5']}


if navbar == 'Inicio':
  # Set the background image using CSS
  background_image = """
      <style>
      .stApp {
          background-image: url("http://www.ucv.ve/fileadmin/templates/core/img/img_carrusel/1_UCV_CIUDAD_UNIVERSITARIA_DE_CARACAS_F_JUAN_PEREZ_HERNANDEZ.png");
          background-size: cover;
      }
      </style>
      """
  st.markdown(background_image, unsafe_allow_html=True)
  # Set the title of the app
  st.title("Servicio de Comedor")
  st.subheader("Universidad Central de Venezuela")
elif navbar == 'Reserva de Turnos':
  pass
elif navbar == "Consulta de Menú Semanal":
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

## Registro de usuarios ### 

if navbar == "Registro de Usuarios":
  mostrar_formulario_registro()
elif navbar == "Info. de Contacto para Donaciones":
  pass
else:
  pass
