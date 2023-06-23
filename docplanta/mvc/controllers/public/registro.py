import web # se importa la libreria de web.py para hacer sus del framework
import pyrebase # se importa la libreria de firebase para hacer uso de la fire base creada de google
import firebase_config as token # se importa la libreria de firebase_comfig para hacer uso de nuestro token de fire base
import json # se importa la libreria de json para hacer uso y modificación de estos elementos


render = web.template.render("mvc/views/admin",base="layout_add_users_admin")

class Add_users_admin:
    def GET(self): 
        try: # prueba el  codigo
            message2 = None # se crear una variable para el mensaje de error
            return render.add_users_admin(message2) # renderiza la pagina login.html con el mensaje
        except Exception as error: # atrapa el error a arreglar
            message2 = "Error en el sistema" # se alamacena un mensaje de error
            print("Error Login.GET: {}".format(error)) # se imprime el error que ocurrio
            return render.add_users_admin(message2) # se renderiza nuevamente login con el mensaje de error

    def POST(self):
        try:
            firebase = pyrebase.initialize_app(token.firebaseConfig) # se inicializa la configuración del fire base
            auth = firebase.auth()  # se inicializa el metodo de autentificación
            db = firebase.database()  # se inicializa el metodo de base de datos en firebase
            formulario = web.input() # se crea una variable formulario para recibir los datos del registrar.html
            nombre = formulario.nombre # se crea la variable nombre donde se guardara los datos ingresados en el formulario
            telefono = formulario.telefono  # se crea la variable telefono donde se guardara los datos ingresados en el formulario
            email = formulario.email  # se crea la variable email donde se guardara los datos ingresados en el formulario
            level= formulario.level # se crea la variable level donde se guardara los datos ingresados en el formulario
            password= formulario.password  # se crea la variable password donde se guardara los datos ingresados en el formulario
            usuario_creado = auth.create_user_with_email_and_password(email, password) # se crea una varible donde se verificara si el email y la contraseña son correctas para crear un nuevo usuario
            print("localid :" ,usuario_creado ['localId'] ) # se imprimeel localid
            data = { "nombre": nombre,  # se hace uso de la base de datos de fire base donde se mostraran los soguiientes campos
                "telefono" : telefono,
                "email" : email,
                "level" : level
            }
            results = db.child("usuario_creado").child(usuario_creado ['localId'] ).set(data) # nos dara la creacion de un hijo en firebase
            return web.seeother("/user_list_admin")# nos devuelve el login
        except Exception as error: # atrapa el error a arreglar
            formato = json.loads(error.args[1]) # Error en formato JSON
            error = formato['error'] # se obtiene el json de error
            message2 = error['message'] # se obtiene el mensaje de error
            if message2 == "EMAIL_EXISTS" :
                return render.add_users_admin("el correo que quiso ingresar ya está registrado, porfavor pruebe con otros datos ") 
            print("Error Login.POST: {}".format(message2)) # se imprime el message enviado por firebase