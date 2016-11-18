var n_elems = 6;


jQuery(document).ready(function($) {
    load_more_nopub();
    $("#load_more_nopub").click(function(){
        load_more_nopub();
    });
});


function load_more_nopub(){
    var tipo = $("#load_more_nopub").attr("tipo_usuario");
    
    $.ajax({
        url: '/get_no_pub',
        type: 'GET',
        dataType: 'json',
        data: {number_elements: n_elems},
    })
    .done(function(data) {
        /*Render*/
        for(var i=0; i<data.length;i++){
            if(tipo=="autor"){
                var tr = $('<tr><td class="Nombre">'+data[i].nombre+'</td> <td class="Fecha">'+data[i].fecha+'</td> <td><center>'+data[i].editando+'</center></td> <td><a href="/modificar_articulo?id='+data[i]._id+'&nombre='+data[i].nombre+'&resumen='+data[i].resumen+'&palabras='+data[i].palabras+'&cuerpo='+data[i].cuerpo+'&imagen='+data[i].imagen+'" style="pointer-events: none; cursor: default;" class="btn btn-warning col-md-6">Modificar</a> <a style="pointer-events: none; cursor: default;" href="/publicar?editor=1&id='+data[i]._id+'" class="btn btn-success col-md-6" >Publicar</a></td></tr>')
            }else{
             var tr = $('<tr><td class="Nombre">'+data[i].nombre+'</td> <td class="Fecha">'+data[i].fecha+'</td> <td><center>'+data[i].editando+'</center></td> <td><a href="/modificar_articulo?id='+data[i]._id+'&nombre='+data[i].nombre+'&resumen='+data[i].resumen+'&palabras='+data[i].palabras+'&cuerpo='+data[i].cuerpo+'&imagen='+data[i].imagen+'" class="btn btn-warning col-md-6">Modificar</a> <a href="/publicar?editor=1&id='+data[i]._id+'" class="btn btn-success col-md-6" >Publicar</a></td></tr>')
            }
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