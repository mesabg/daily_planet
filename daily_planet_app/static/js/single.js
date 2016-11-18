jQuery(document).ready(function($) {
    $("#upload_comentario").click(function(){
        comment();
    });
    
    $("button.btn-responder.btn.btn-default").click(function(){
    	console.log("Hola");
    	console.log($(this));
    	$(this).parent().siblings('.responder').slideToggle("slow");
    });
    
    $(".responder").hide(); 
    
});

function comment(){
    if ( $("#comentario").val()=="" ) return;
    var id_articulo = parseInt($("#upload_comentario").attr('id_articulo'));
    var id_usuario = $("#upload_comentario").attr('id_usuario');
    $.ajax({
        url: '/upload_comentario?id_articulo='+id_articulo+'&id_usuario='+id_usuario,
        dataType: 'json',
        type: 'POST',
        data: { comentario_cuerpo: $("#comentario").val() }
    })
    .done(function(data) {
        /*Render*/
        
        var div = $('<div class="media response-info"><div class="media-left response-text-left"><img class="media-object" src="/get_image_username?name='+data.nombre+'" alt=""> <h5>' + data.nombre +'</h5></div>    <div class="media-body response-text-right">  <p>'+data.cuerpo+'</p>   <ul> <li>' + data.fecha + '</li> <li> <a href="#">Responder</a> </li> </ul> </div>  </div>'   )
        
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