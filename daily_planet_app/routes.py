from flask import *
import datetime
from models import *
import json



def create_routes(app, model):
    app.config['SESSION_TYPE'] = 'memcached'
    app.config['SECRET_KEY'] = 'super secret key'
    session = Session()
    
    #Routes Definition
    @app.route('/')
    def index():
    	return render_template('index.html')
    
    @app.route('/login', methods=['POST'])
    def login():
    	email = request.form['email']
    	password  = request.form['password']
    	log_in = model.login(email, password)
    	if not log_in:
    	    return render_template('opexito.html', msg="Log In fallido, intente de nuevo")
    	session['username'] = log_in['_id'];
    	print(session['username'])
    	return render_template('index.html')
    	
    @app.route('/logout')
    def logout():
    	session.pop('username', None)
    	return render_template('opexito.html', msg="Log Out Exitoso")
    	
   
#   @app.route('/login', methods = ['GET', 'POST'])
#def login():
#   if request.method == 'POST':
#      session['username'] = request.form['username']
#      return redirect(url_for('index'))
#   return '''
	
#@app.route('/logout')
#def logout():
   # remove the username from the session if it is there
   
 #  return redirect(url_for('index'))


    	
    @app.route('/registro')
    def registro():
        return render_template('registro.html')
        
        
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
        return render_template('opexito.html')
    
    
    @app.route('/single', methods=['GET'])
    def single():
        _id = int(request.args.get('id'))
        l = model.getSingle(_id)
        data = None        
        for doc in l:
            data = doc
        return render_template('single.html', item=data)
        
    @app.route('/crear')
    def crear():
        return render_template('crear.html')
        
        
    @app.route('/crear_save', methods=['POST'])
    def crear_save():
        return render_template('crear_save.html')
        
        
    @app.route('/articulos_publicados', methods=['GET'])
    def articulos_publicados():
        return render_template('articulos_publicados.html')
    
    
    @app.route('/articulos_no_publicados', methods=['GET'])
    def articulos_no_publicados():
        return render_template('articulos_no_publicados.html')
    
    
    @app.route('/modificar_articulo', methods=['GET'])
    def modificar_articulo():
        obj = {'nombre':request.args.get('nombre'),'_id':int(request.args.get('id')),'resumen':request.args.get('resumen'),'palabras':request.args.get('palabras'),'imagen':request.args.get('imagen'),'cuerpo':request.args.get('cuerpo')}
        return render_template('modificar_articulo.html', data=obj)
        
        
    @app.route('/modificar_articulo_save', methods=['POST'])
    def modificar_articulo_save():
        return render_template('opexito.html')
        
        
    @app.route('/publicar', methods=['GET'])
    def publicar():
        _id = int(request.args.get('id'))
        editor = int(request.args.get('editor'))
        model.publicar(_id,editor)
        return render_template('opexito.html',msg="Publicación exitosa")
       
        
    @app.route('/modificar_perfil')
    def modificar_perfil():
        return render_template('modificar_perfil.html')
        
        
    @app.route('/modificar_perfil_save', methods=['POST'])
    def modificar_perfil_save():
        return render_template('opexito.html')
        
        
    @app.route('/perfil')
    def perfil():
        return render_template('perfil.html', usuario="Nombre")
        
        
    @app.route('/get_no_pub', methods=['GET'])
    def get_feed_no_pub():
        n_elem = int(request.args.get('number_elements')) - 6
        data = json.dumps( model.getSixFeedNoPub(n_elem) )
        return Response(data, status=200, headers=None, mimetype='application/json')
         
         
         
    @app.route('/get_feed', methods=['GET'])
    def get_feed():
        n_elem = int(request.args.get('number_elements')) - 6
        data = json.dumps( model.getSixFeed(n_elem) )
        return Response(data, status=200, headers=None, mimetype='application/json')
        
    @app.route('/get_feed_pub', methods=['GET'])
    def get_feed_pub():
        n_elem = int(request.args.get('number_elements')) - 6
        tipo = (request.args.get('type'))
        busqueda = (request.args.get('search'))
        data = json.dumps( model.getSixFeedPub(n_elem,tipo,busqueda) )
        return Response(data, status=200, headers=None, mimetype='application/json')
    
    @app.route('/get_image', methods=['GET'])
    def get_image():
        path = 'static/' + request.args.get('path')
        spli = path.split(".")
        valor = spli[len(spli)-1] 
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
        id_articulo = int(float(request.args.get('id_articulo')))
        #text = request.args.get('comentario_cuerpo')
        text = request.form['comentario_cuerpo']
        data = json.dumps(model.upload_comentario(id_articulo, id_usuario, text))
        return Response(data, status=200, headers=None, mimetype='application/json')


