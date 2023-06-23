
import web # se importa la libreria de web.py para hacer sus del framework
import pyrebase # se importa la libreria de firebase para hacer uso de la fire base creada de google
import firebase_config as token # se importa la libreria de firebase_comfig para hacer uso de nuestro token de fire base
import json # se importa la libreria de json para hacer uso y modificación de estos elementos



render = web.template.render("mvc/views/public/",base="layout")

class Logout:
    def GET(self):
        web.setcookie('localid',"") # configuramos la cookie para que cuando el usuario presione el logout , la cookie cambie a un valor vacio asi limitando su acesso si es que quisieran entrar otra vez a la raiz
        return web.seeother("/login")  # nos devuelve el login