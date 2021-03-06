import os
from flask import *
import datetime
from models import *
import json
from werkzeug import secure_filename
from flask_mail import Message
from flask_mail import Mail

def create_routes(app, model):
    app.config['UPLOAD_FOLDER'] = 'static/local_images'
    app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg'])
    app.config['SESSION_TYPE'] = 'memcached'
    app.config['SECRET_KEY'] = 'super secret key'
    session = Session()
    session['user'] = None
    
    app.config['MAIL_SERVER']='smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = 'daily.planet.email.ati@gmail.com'
    app.config['MAIL_PASSWORD'] = 'ati123456'
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    
    mail = Mail(app)
    
    def allowed_file(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']
    
    #Routes Definition
    @app.route('/')
    def index():
    	return render_template('index.html', user=session['user'])
    
    @app.route('/login', methods=['POST'])
    def login():
        if session['user'] != None:
            return render_template('opexito.html', msg="Debes cerrar sesión para hacer esta acción", user=None)
        email = request.form['email']
        password  = request.form['password']
        log_in = model.login(email, password)
        if not log_in:
            return render_template('opexito.html', msg="Log In fallido, intente de nuevo")
        session['user'] = log_in;
        return render_template('index.html', user=session['user'])
    	
    @app.route('/logout')
    def logout():
        if session['user'] == None:
            return render_template('opexito.html', msg="No puedes cerrar sesión sino has entrado aún", user=None)
        session['user'] = None
        return render_template('opexito.html', msg="Log Out Exitoso", user=None)
    	
    @app.route('/registro')
    def registro():
        return render_template('registro.html')
        
    #profile
    @app.route('/perfil/<username>')
    def perfil(username):
        if not session['user']:
            return render_template('opexito.html', msg="No ha iniciado sesión", user=None)
        
        articulos_favoritos = model.articulos_favoritos(session['user']['_id'])
        articulos = None
        articulos = model.articulos(session['user']['_id'])
        return render_template('perfil.html', user=session['user'], articulos_favoritos = articulos_favoritos, articulos = articulos )
        
    @app.route('/perfil/modificar/<username>')
    def perfil_modify(username):
        if not session['user']:
            return render_template('opexito.html', msg="No ha iniciado sesión, no puede modificar perfil", user=None)
        return render_template('modificar_perfil.html', user=session['user'])
        
        
    @app.route('/registro_save', methods=['POST'])
    def registro_save():
        password = request.form['password']
        repeat = request.form['password_r']
        if password != repeat:
            return render_template('opexito.html', msg="Registro fallido, contraseñas no coinciden")
            
        nombre = request.form['nombre']
        email = request.form['email']
        tipo = request.form['tipo']
        respuestadb = model.registro(nombre,email,password,tipo)
        if respuestadb:
            return render_template('opexito.html', msg="Registro exitoso!")
        else:
            return render_template('opexito.html', msg="Registro fallido, nombre o email ya existen")
        # Salvar data
        # Generar Mensage
    
    @app.route('/recuperar_contrasena', methods=['POST'])
    def recuperar_contrasena():
        email = request.form['recoverpass_email']
        info = model.get_info(email)
        
        if info:
            msg = Message("[Daily Planet - Recuperación de contraseña]", sender="moises.berenguer@gmail.com.com", recipients=[email])
            msg.body = "Estimado " + info['nombre'] + ".\n" + "    Se le informa que su contraseña para acceder a nuestra plataforma es la siguiente: " + info['password']
            mail.send(msg)
            return render_template('opexito.html', msg="La contraseña ha sido enviada a su correo." ,user=session['user'])
        else:
            return render_template('opexito.html', msg="Introdujo una dirección de correo incorrecta, intente de nuevo." ,user=session['user'])
    
    @app.route('/single', methods=['GET'])
    def single():
        _id = int(request.args.get('id'))
        if session['user'] == None:
            today = datetime.datetime.now()
            if not model.VerloInvitado(_id,today):
                return render_template('opexito.html', msg="Lo siento los invitados solo pueden acceder a los artículos del día." ,user=session['user'])
        data = model.getSingle(_id)
        if session['user'] == None:
            return render_template('single.html', item=data, user=session['user'])
        else:
            session['user']=model.get_user_data(session['user']['_id'])
            return render_template('single.html', item=data, user=session['user'])
        
        
    @app.route('/add_favorito', methods=['GET'])
    def addfav():
        if session['user'] == None:
             return render_template('opexito.html', msg="No puedes agregar a favoritos si eres Invitado", user=None)
        _id = request.args.get('id')
        add_favorito = model.addfav(int(float(_id)), session['user']['_id'])
        if add_favorito:
            return render_template('opexito.html',msg="Has agregado a favoritos este artículo",user=session['user'])
        return render_template('opexito.html',msg="Ya habías agregado a favoritos este artículo",user=session['user'])
        
    @app.route('/crear')
    def crear():
        if session['user'] == None:
            return render_template('opexito.html', msg="No puedes crear artículos sino eres Autor", user=None)
            
        if session['user']['tipo'] == "editor" or session['user']['tipo'] == "lector":
            return render_template('opexito.html', msg="No puedes crear artículos sino eres Autor", user=None)
            
        return render_template('crear.html', autor=session['user']['_id'], user=session['user'])
        
        
    @app.route('/crear_save', methods=['POST'])
    def crear_save():
        if session['user'] == None:
            return render_template('opexito.html', msg="No puedes crear artículos sino eres Autor", user=None)
            
        if session['user']['tipo'] == "editor" or session['user']['tipo'] == "lector":
            return render_template('opexito.html', msg="No puedes crear artículos sino eres Autor", user=None)
            
        image = request.files['image']
        nombre  = request.form['nombre']
        resumen = request.form['resumen']
        palabras = request.form['palabras']
        cuerpo = request.form['cuerpo']
        autor = request.args.get('autor')
        #File 
        # Check if the file is one of the allowed types/extensions
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            # Move the file form the temporal folder to
            # the upload folder we setup
            image.save(os.path.join(app.config['UPLOAD_FOLDER']+'/art', filename))
            model.crear(nombre,resumen,palabras,'local_images/art/'+filename,cuerpo,autor)
            return render_template('opexito.html',msg="Creación exitosa", user=session['user'])
        return render_template('opexito.html',msg="Tipo de archivo incorrecto", user=session['user'])
        
        
    @app.route('/articulos_publicados', methods=['GET'])
    def articulos_publicados():
        return render_template('articulos_publicados.html', user=session['user'])
    
    
    @app.route('/articulos_no_publicados', methods=['GET'])
    def articulos_no_publicados():
        if session['user'] == None:
            return render_template('opexito.html', msg="No puedes ver los artículos no publicados si eres Invitado", user=None)
            
        if session['user']['tipo'] == "lector":
            return render_template('opexito.html', msg="No puedes ver los artículos no publicados si eres Lector", user=None)
            
        return render_template('articulos_no_publicados.html', user=session['user'])
    
    
    @app.route('/modificar_articulo', methods=['GET'])
    def modificar_articulo():
        if session['user'] == None:
            return render_template('opexito.html', msg="No puedes modificar artículos sino eres Editor", user=None)
            
        if session['user']['tipo'] == "autor" or session['user']['tipo'] == "lector":
            return render_template('opexito.html', msg="No puedes crear artículos sino eres Editor", user=None)
            
        obj = {'nombre':request.args.get('nombre'),'_id':int(request.args.get('id')),'resumen':request.args.get('resumen'),'palabras':request.args.get('palabras'),'imagen':request.args.get('imagen'),'cuerpo':request.args.get('cuerpo')}
        return render_template('modificar_articulo.html', data=obj, editor=session['user']['_id'], user=session['user'])
        
        
    @app.route('/modificar_articulo_save', methods=['GET','POST'])
    def modificar_articulo_save():
        if session['user'] == None:
            return render_template('opexito.html', msg="No puedes modificar artículos sino eres Editor", user=None)
            
        if session['user']['tipo'] == "autor" or session['user']['tipo'] == "lector":
            return render_template('opexito.html', msg="No puedes crear artículos sino eres Editor", user=None)
            
        image = request.files['image']
        nombre  = request.form['nombre']
        resumen = request.form['resumen']
        palabras = request.form['palabras']
        cuerpo = request.form['cuerpo']
        _id = int(request.args.get('id'))
        editor = request.args.get('editor')
        #File 
        # Check if the file is one of the allowed types/extensions
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            # Move the file form the temporal folder to
            # the upload folder we setup
            image.save(os.path.join(app.config['UPLOAD_FOLDER']+'/art', filename))
            model.modificar(_id,nombre,resumen,palabras,'local_images/art/'+filename,cuerpo,editor)
            session['user']=model.get_user_data(_id)
            return render_template('opexito.html',msg="Modificación exitosa", user=session['user'])

        model.modificar_no_image(_id,nombre,resumen,palabras,cuerpo,editor)
        session['user']=model.get_user_data(_id)
        return render_template('opexito.html',msg="Modificación exitosa")

        
    @app.route('/publicar', methods=['GET'])
    def publicar():
        if session['user'] == None:
            return render_template('opexito.html', msg="No puedes modificar artículos sino eres Editor", user=None)
            
        if session['user']['tipo'] == "autor" or session['user']['tipo'] == "lector":
            return render_template('opexito.html', msg="No puedes crear artículos sino eres Editor", user=None)
            
        _id = int(request.args.get('id'))
        editor = int(request.args.get('editor'))
        model.publicar(_id,editor)
        return render_template('opexito.html',msg="Publicación exitosa", user=session['user'])
       
        
    @app.route('/modificar_perfil')
    def modificar_perfil():
        if not session['user']:
            return render_template('opexito.html', msg="No ha iniciado sesión, no puede modificar perfil", user=None)
        return render_template('modificar_perfil.html',data=session['user'])
        
        
    @app.route('/modificar_perfil_save', methods=['POST'])
    def modificar_perfil_save():
        if not session['user']:
            return render_template('opexito.html', msg="No ha iniciado sesión, no puede modificar perfil", user=None)
            
        nombre = request.form['nombre']
        avatar = request.files['avatar']
        descripcion = request.form['descripcion']
        _id = int(float(request.form['_id']))
        
        #modificacion
        if avatar and allowed_file(avatar.filename):
            filename = secure_filename(avatar.filename)
            # Move the file form the temporal folder to
            # the upload folder we setup
            avatar.save(os.path.join(app.config['UPLOAD_FOLDER']+'/user', filename))
            model.modificar_perfil(_id, nombre, descripcion, 'local_images/user/'+filename )
            session['user']= model.get_user_data(_id)
            return render_template('opexito.html',msg="Modificación de perfil exitosa !", user=session['user'])
        model.modificar_perfil_no_image(_id, nombre, descripcion)
        session['user']=model.get_user_data(_id)
        return render_template('opexito.html',msg="Modificación de perfil exitosa sin imagen !", user=session["user"])


    @app.route('/get_no_pub', methods=['GET'])
    def get_feed_no_pub():
        n_elem = int(request.args.get('number_elements')) - 6
        data = json.dumps( model.getSixFeedNoPub(n_elem) )
        return Response(data, status=200, headers=None, mimetype='application/json')
         
         
         
    @app.route('/get_feed', methods=['GET'])
    def get_feed():
        n_elem = int(request.args.get('number_elements')) - 6
        data = list()
        if not session['user']:
            today = datetime.datetime.now()
            data = json.dumps( model.getSixFeedInv(n_elem,today))
        else:
            data = json.dumps( model.getSixFeed(n_elem))
        return Response(data, status=200, headers=None, mimetype='application/json')
        
    @app.route('/get_feed_pub', methods=['GET'])
    def get_feed_pub():
        n_elem = int(request.args.get('number_elements')) - 6
        tipo = (request.args.get('type'))
        busqueda = (request.args.get('search'))
        if not session['user']:
            today = datetime.datetime.now()
            data = json.dumps( model.getSixFeedPubInv(n_elem,tipo,busqueda,today) )
        else:
            data = json.dumps( model.getSixFeedPub(n_elem,tipo,busqueda) )
        
        return Response(data, status=200, headers=None, mimetype='application/json')
    
    @app.route('/get_image', methods=['GET'])
    def get_image():
        path = 'static/' + request.args.get('path')
        spli = path.split(".")
        valor = spli[len(spli)-1] 
        print(path)
        return send_file(path, mimetype='image/'+valor)
        #http://localhost:5000/get_image?path=local_images/art/2.jpg
        
    @app.route('/get_image_username', methods=['GET'])
    def get_image_username():
        name = request.args.get('name')
        path = 'static/' + model.get_image_username(name)
        spli = path.split(".")
        valor = spli[len(spli)-1] 
        return send_file(path, mimetype='image/'+valor)
        
    @app.route('/upload_comentario', methods=['GET', 'POST'])
    def upload_comentario():
        id_usuario = int(request.args.get('id_usuario'))
        id_articulo = int(request.args.get('id_articulo'))
        if not id_usuario:
            no_usuario = {'_id':-1}
            Response(json.dumps(no_usuario), status=200, headers=None, mimetype='application/json')
        #text = request.args.get('comentario_cuerpo')
        text = request.form['comentario_cuerpo']
        data = json.dumps(model.upload_comentario(id_articulo, id_usuario, text))
        return Response(data, status=200, headers=None, mimetype='application/json')


    @app.route('/upload_comentario_recursive', methods=['GET', 'POST'])
    def upload_comentario_recursive():
        id_usuario = int(float(request.args.get('id_usuario')))
        id_articulo = int(float(request.args.get('id_articulo')))
        id_padre = int(float(request.args.get('id_padre')))
        #text = request.args.get('comentario_cuerpo')
        text = request.form['comentario_cuerpo']
        data = json.dumps(model.upload_comentario_recursive(id_articulo, id_usuario, id_padre, text))
        return Response(data, status=200, headers=None, mimetype='application/json')

    @app.route('/suscribete', methods=['POST'])
    def suscribete():
        return render_template('opexito.html', msg="Está suscrito, gracias por formar parte del grupo Daily Planet !", user=session["user"])