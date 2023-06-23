import web # se importa la libreria de web.py para hacer sus del framework
import json # se imporúyta la libreria de json para hacer uso y modificación de estos elementos


urls = (
      #ulrs o raices de las diferentes dpáginas html que vamos a utlizar
    '/', 'mvc.controllers.public.login.Login',
      
)
app = web.application(urls, globals())#configura las urls en la aplicacion web
wsgiapp = app.wsgifunc()







if __name__ == "__main__":
    web.config.debug = True # activa o desactiva el modo de repuracion de firebase
    app.run()