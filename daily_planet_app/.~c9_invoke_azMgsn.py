from flask import *
import datetime
from models import *
import json


def create_routes(app, model):
    #Routes Definition
    @app.route('/')
    def index():
    	return render_template('index.html')
    
    @app.route('/login', methods=['POST'])
    def login():
    	email = request.form['email']
    	password  = request.form['password']
    	return render_template('index.html')
    	
    	
    @app.route('/registro')
    def registro():
        return render_template('registro.html')
        
        
    @app.route('/registro_save', methods=['POST'])
    def registro_save():
        # Salvar data
        # Generar Mensage
        return render_template('opexito.html')
    
    
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
        print (data)
      #  print (list(l['comentarios']))
        return render_template('single.html', item=data)
        
   http://127.0.0.1:5000/single?comentario=hola
        
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
    
    
    @app.route('/modificar_articulo')
    def modificar_articulo():
        return render_template('modificar_articulo.html')
        
        
    @app.route('/modificar_articulo_save', methods=['POST'])
    def modificar_articulo_save():
        return render_template('opexito.html')
        
        
    @app.route('/modificar_perfil')
    def modificar_perfil():
        return render_template('modificar_perfil.html')
        
        
    @app.route('/modificar_perfil_save', methods=['POST'])
    def modificar_perfil_save():
        return render_template('opexito.html')
        
        
    @app.route('/perfil')
        return render_template('perfil.html', usuario="Nombre")
        return render_template('perfil.html', usuario="Nombre")
        
    @app.route('/get_feed', methods=['GET'])
    def get_feed():
        n_elem = int(request.args.get('number_elements')) - 6
        data = json.dumps( model.getSixFeed(n_elem) )
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
        
    @app.route('/upload_comentario', methods=['GET','POST'])
    def upload_comentario():
        id_usuario = int(request.args.get('id_usuario'))
        id_articulo = int(request.args.get('id_articulo'))
        text = request.form['comentario_cuerpo']
        comentario_nuevo = model.upload_comentario(id_articulo, id_usuario, text)
        return Response(comentario_nuevo, status=200, headers=None, mimetype='application/json')
