# background images
def main_image():
  background_image = """
    <style>
    .stApp {
        background-image: url("https://eldiario.com/wp-content/uploads/2023/01/32-Labores-de-restauracion-del-Aula-Magna-de-la-UCV-El-Diario-Jose-Daniel-Ramos.jpg.webp");
        background-size: cover;
    }
    </style>
  """
  return background_image

def logo():
  Logo = """
    <style>.img {
      float:left;
      width:120px;
      height:115px;
    }</style>
    <img class = 'img' src="https://upload.wikimedia.org/wikipedia/commons/f/f4/Logo_Universidad_Central_de_Venezuela.svg">
    """
  return Logo

def comedor_image():
  background_image = """
    <style>
    .stApp {
        background-image: url("https://www.colorcombos.com/images/colors/FAFAFA.png");
        background-size: cover;
    }
    </style>
  """
  return background_image

# margenes
margin = """
<style>
.block-container {
  padding-top: 2rem;
  padding-bottom: 0rem;
  padding-left: 5rem;
  padding-right: 5rem;
  }
</style>"""

margin2 = '''
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
'''

css_login = """
  <style>
  .st-bs {
    background-color: #ffffff;
  }
  .st-bc {
    background-color: #ffffff;
  }
  .st-emotion-cache-1ogbtk7{
    background-color: #0098db;
    color:#ffffff;
    font-weight:bold;
  }
  .st-emotion-cache-pb0dxo {
    border:none;
  }
  .st-emotion-cache-15yozlq {
    text-align:left;
  }
  </style>"""

css_button = '''
  <style>
  .st-emotion-cache-11z1ede {
    display: inline-flex;
    -webkit-box-align: center;
    align-items: center;
    -webkit-box-pack: center;
    justify-content: center;
    font-weight: 400;
    padding: 0.25rem 0.75rem;
    border-radius: 0.5rem;
    min-height: 2.5rem;
    margin: 0px;
    line-height: 1.6;
    color: #ffffff;
    width: 5rem;
    user-select: none;
    background-color: #0098db;
    border: 1px solid rgba(0, 32, 78, 0.2);
  }
  </style>'''




