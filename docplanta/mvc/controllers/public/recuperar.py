import web # se importa la libreria de web.py para hacer sus del framework
import pyrebase # se importa la libreria de firebase para hacer uso de la fire base creada de google
import firebase_config as token # se importa la libreria de firebase_comfig para hacer uso de nuestro token de fire base
import json # se importa la libreria de json para hacer uso y modificación de estos elementos



render = web.template.render("mvc/views/public/",base="recuperar_layout")


class Recuperar:
    def GET(self):
        return render.recuperar()

    def POST(self):
        firebase = pyrebase.initialize_app(token.firebaseConfig) # se inicializa la configuración del fire base
        auth = firebase.auth() # se inicializa el metodo de autentificación
        formulario = web.input() # se crea una variable formulario para recibir los datos del login
        email = formulario.email # se crea una varible donde se guardara los datos ingresados en el formulario
        result = auth.send_password_reset_email(email)  # se crea una varible donde se pondra resetar la contraseña
        return web.seeother("/") # nos devuelve al html bievenida
      
