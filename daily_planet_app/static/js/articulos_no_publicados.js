var n_elems = 6;


jQuery(document).ready(function($) {
    load_more_nopub();
    $("#load_more_nopub").click(function(){
        load_more_nopub();
    });
});


function load_more_nopub(){
    $.ajax({
        url: '/get_no_pub',
        type: 'GET',
        dataType: 'json',
        data: {number_elements: n_elems},
    })
    .done(function(data) {
        /*Render*/
        for(var i=0; i<data.length;i++){
            console.log(data[i]);
            var tr = $('<tr><td class="Nombre">'+data[i].nombre+'</td> <td class="Fecha">'+data[i].fecha+'</td> <td><center>'+data[i].editando+'</center></td> <td><a href="/modificar_articulo?id='+data[i]._id+'&nombre='+data[i].nombre+'&resumen='+data[i].resumen+'&palabras='+data[i].palabras+'&cuerpo='+data[i].cuerpo+'&imagen='+data[i].imagen+'" class="btn btn-warning col-md-6">Modificar</a><button class="btn btn-success col-md-6" onclick="publicar(this.parentNode.parentNode)">Publicar</button></td></tr>')
           // var div = $('<div class="col-md-4 banner-bottom-grid"> <a href="/single?id='+data[i]._id+'" > <img src="/get_image?path='+data[i].imagen+'"/>  </a><h4>'+data[i].nombre+'</h4> <p>'+data[i].resumen+'</p> </div>');
            $("#table").append(tr);
        }
        if(data.length < 6){
            var boton = document.getElementById("load_more_nopub");
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

                        <tr>
							<td class="Nombre">Artículo Interesante</td>
							<td class="Fecha">10/10/2016</td>
							<td><center>Si</center></td>
							<td><a href="/modificar_articulo" class="btn btn-warning col-md-6">Modificar</a><button class="btn btn-success col-md-6" onclick="publicar(this.parentNode.parentNode)">Publicar</button></td>
						</tr>
						
						
						*/