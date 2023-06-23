
import web # se importa la libreria de web.py para hacer sus del framework
import pyrebase # se importa la libreria de firebase para hacer uso de la fire base creada de google
import firebase_config as token # se importa la libreria de firebase_comfig para hacer uso de nuestro token de fire base
import json # se importa la libreria de json para hacer uso y modificación de estos elementos



render = web.template.render("mvc/views/public/",base="layout_login")


class Login:
    def GET(self):
        try: # prueba el codigo
            message = None # se crear una variable para el mensaje de error
            return render.login(message) # renderiza la pagina login.html con el mensaje
        except Exception as error: # atrapa el error a arreglar
            message = "Error en el sistema" # se alamacena un mensaje de error
            print("Error Login.GET: {}".format(error)) # se imprime el error que ocurrio
            return render.login(message) # se renderiza nuevamente login con el mensaje de error

    def POST(self):
        try:
            firebase = pyrebase.initialize_app(token.firebaseConfig) # se inicializa la configuración del fire base
            db = firebase.database()  # se inicializa el metodo de base de datos en firebase
            auth = firebase.auth()  # se inicializa el metodo de autentificación
            formulario = web.input() # se crea una variable formulario para recibir los datos del login
            email = formulario.email # se crea una varible donde se guardara los datos ingresados en el formulario
            password= formulario.password # se crea una varible donde se guardara los datos ingresados en el formulario
            print(email,password)  # se imprime el email y contraseña para rectificar internamente
            verificacion_usuario = auth.sign_in_with_email_and_password(email, password) # se crea una varible donde se verificara si el email y la contraseña con correctas
            local_id = ( verificacion_usuario ['localId']) # se crea la varible donde se almacenara el localid
            web.setcookie('localid', local_id) # confguramos nuestra cookie con el nombre y el valor 
            users = db.child("usuario_creado").child(local_id).get() #utilización de base de datos para obtener el local id
            estado = users.val().get('estado') #creación de variable que obtendra el valor de estado
            level = users.val().get('level')#creación de variable que obtendra el valor de level
            if (level) == "admin": # creacion de condicional para cambiar de pagina segun el nivel
             return web.seeother("/bienvenida_admin") 
            elif (level) == "operador":
                if estado == "desactivado":  # creacion de condicional para cambiar de pagina segun este activado o descativado el ususario
                 return render.index()
                else:
                 return web.seeother("/bienvenida_operador")
        except Exception as error: # atrapa el error a arreglar
            formato = json.loads(error.args[1]) # Error en formato JSON
            error = formato['error'] # obtiene el json de error
            message = error['message'] # obtiene el mensaje de error
            if message == "INVALID_PASSWORD" :
                return render.login("la contraseña que ingreso no es válida , intente de nuevo ") 
            print("Error Login.POST: {}".format(message)) # se imprime el message enviado por firebase
           # se muestra nuevamente login mostrando el mensaje de error
