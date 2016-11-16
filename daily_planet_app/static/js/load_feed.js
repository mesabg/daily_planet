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
        console.log(data);
        for(var i=0; i<data.length;i++){
            var div = $('<div class="col-md-4 banner-bottom-grid"> <a href="/single?id='+data[i]._id+'"  <img src="/get_image?path='+data[i].imagen+'/>  </a><h4>'+data[i].nombre+'</h4> <p>'+data[i].resumen+'</p> </div>');
            $("#feed").append(div);
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