jQuery(document).ready(function($) {
    $("#upload_comentario").click(function(){
        comment();
    });
    
    $(".btn-responder").click(function(){
    	$(this).parent().siblings('.responder').slideToggle("slow");
    });
    
    $(".upload_comentario_recursive").click(function(){
        comment_recursive($(this).parent().parent(), $($(this).siblings('.comentario_recursive')[0]), $(this));
    });
    
    
    $(".responder").hide(); 
    
});

function comment(){
    if ( $("#comentario").val()=="" ) return;
    var id_articulo = parseInt($("#upload_comentario").attr('id_articulo'));
    var id_usuario = parseInt($("#upload_comentario").attr('id_usuario'));

    if (!id_usuario){
        alert('Es un usuario invitado, no puede comentar !');
        return;
    }


    $.ajax({
        url: '/upload_comentario?id_articulo='+id_articulo+'&id_usuario='+id_usuario,
        dataType: 'json',
        type: 'POST',
        data: { comentario_cuerpo: $("#comentario").val() }
    })
    .done(function(data) {
        /*Render*/
        if (data._id == -1){
            alert('Es un usuario invitado, no puede comentar !');
            return;
        }

        var div = $('<div class="media response-info"><div class="media-left response-text-left"><img class="media-object" src="/get_image?name='+data.nombre+'" width="100" height="100" alt=""> <h5>' + data.nombre +'</h5></div>    <div class="media-body response-text-right">  <p>'+data.cuerpo+'</p>   <ul> <li>' + data.fecha + '</li> <li><button class="btn-responder btn btn-default">Responder</button></li> </ul> </div>  </div>'   )
        
        $($($($(div.children('div')[1]).children('ul')[0]).children('li')[1]).children('button')[0]).click(function(){
        	$(this).parent().siblings('.responder').slideToggle("slow");
        });
    			 
        							
        $("#fondo").prepend(div);
        
        $("#comentario").val("");
        
    })
    .fail(function(error) {
        console.log("error", error);
    })
    .always(function() {
        console.log("complete");
    });
}


function comment_recursive(padre,texto,boton){
	if (texto.val()=="") return;
	var id_articulo = parseInt(boton.attr('id_articulo'));
    var id_usuario = parseInt(boton.attr('id_usuario'));
    var id_padre = parseInt(boton.attr('id_padre'));
    
    if (!id_usuario){
        alert('Es un usuario invitado, no puede comentar !');
        return;
    }

    
    $.ajax({
        url: '/upload_comentario_recursive?id_articulo='+id_articulo+'&id_usuario='+id_usuario+'&id_padre='+id_padre,
        dataType: 'json',
        type: 'POST',
        data: { comentario_cuerpo: texto.val() }
    })
    .done(function(data) {
        /*Render*/
        
        var div = $('<div class="media response-info"><div class="media-left response-text-left"><img class="media-object" src="/get_image_username?name='+data.nombre+'" alt="" width="100" height="100"> <h5>' + data.nombre +'</h5></div>    <div class="media-body response-text-right">  <p>'+data.cuerpo+'</p>   <ul> <li>' + data.fecha + '</li> <li><button class="btn-responder btn btn-default">Responder</button></li> </ul> </div>  </div>'   )
        
        $($($($(div.children('div')[1]).children('ul')[0]).children('li')[1]).children('button')[0]).click(function(){
        	$(this).parent().siblings('.responder').slideToggle("slow");
        });
        
        padre.prepend(div);
        
        texto.val("");
        

    })
    .fail(function(error) {
        console.log("error", error);
    })
    .always(function() {
        console.log("complete");
    });
    
    
	
}

/*
            <div class="response">
							<h3>Comentarios</h3>
							{% for comentario in item.comentarios recursive %}
							        {% if comentario.respuestas %}
							        	<div class="media response-info">
							                <div class="media-left response-text-left">
							                	<img class="media-object" src="/get_image_username?name={{comentario.nombre}}" alt=""> <!-- Aqui cambiar la ruta -->
							                	<h5>{{comentario.nombre}}</h5>
							                </div>
							                
							                
							                <div class="media-body response-text-right">
								                <p>{{comentario.cuerpo}}</p>
								                
								                <ul>
								                	<li>{{comentario.fecha}}</li>
								                	<li><a href="#">Responder</a></li>
								                </ul>
								                
								                <div class="media response-info">
								                	{{loop(comentario.respuestas)}}
								                	<div class="clearfix"> </div>
								                </div>
				
							                </div>
							             </div> 
							        {% else %}
							        	<div class="media response-info">
							               <div class="media-left response-text-left">
							                	<img class="media-object" src="/get_image_username?name={{comentario.nombre}}" alt="">
							                	<h5>{{comentario.nombre}}</h5>
							                </div>
							                
							                <div class="media-body response-text-right">
							                	<p>{{comentario.cuerpo}}</p>
								                <ul>
								                	<li>{{comentario.fecha}}</li>
								                	<li><a href="#">Responder</a></li>
								                </ul>
							                </div>
							                <div class="clearfix"> </div>
							            </div>
							        {% endif %}
							{% endfor %}
						</br>
						
							<div class="opinion">
								<h3>Deja tu comentario</h3>
								<form>
									<textarea placeholder="Mensaje" name="comentario" id="comentario" required=""></textarea>
									<input id="upload_comentario" type="submit" value="ENVIAR" id_usuario="1" id_articulo="{{item._id}}" >
								</form>
							</div>
					</div>
*/