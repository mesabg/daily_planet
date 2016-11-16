var n_elems = 6;


jQuery(document).ready(function($) {
    load_more();
});


function load_more(){
    $.ajax({
        url: '/get_feed',
        type: 'GET',
        dataType: 'json',
        data: {number_elements: n_elems},
    })
    .done(function(data) {
        /*Render*/
        var datica = data;
        console.log(datica);
        for(var i=0; i<datica.length;i++){
            
            $.ajax({
                url: '/get_image',
                type: 'GET',
                dataType: 'img/jpg',
                data: {path: datica[i].imagen}
            }).done(function(data){
                
                var div = $('<div class="col-md-4 banner-bottom-grid"> <a href="/single?id='+datica[i]._id+'"  <img '+data+' src="http://localhost:5000/get_image?path='+datica[i].imagen+'"/>  </a><h4>'+data[i].nombre+'</h4> <p>'+datica[i].resumen+'</p> </div>');
                $("#feed").append(div);
                
                
                
            }).fail(function() {
                console.log("error");
            })
            .always(function() {
                console.log("complete");
            });
            
            
            
            
        }
        if(data.length < 6){
            var boton = document.getElementById("load_more");
            boton.style.display ='none';
        }
        n_elems += 6;
    })
    .fail(function() {
        console.log("error");
    })
    .always(function() {
        console.log("complete");
    });
}




/*

						<div class="col-md-4 banner-bottom-grid">
							<a href="single.html"><img src="{{ url_for('static', filename='images/c3.jpg') }}" alt="" /></a>
							<h4>Ejemplo Noticia 1</h4>
							<p>Lorem Ipsum is simply dummy text
								of the printing and typesetting industry.
								Lorem Ipsum has been the industry's
								dummy text ever since the 1500s,
								including versions of Lorem Ipsum.
							</p>
						</div>
					*/