var n_elems = 6;
var tipo = "Fecha";

jQuery(document).ready(function($) {
    load_more_pub();
    $("#load_more_pub").click(function(){
        load_more_pub();
    });
    
    $('#order_by').change(function(){
        n_elems = 6;
       if( $('#order_by').val()=="Autor" ){
          tipo = "Autor";
          
       }else{
          tipo = "Fecha";
       }
       load_more_pub();
    });
});


function load_more_pub(){
    $.ajax({
        url: '/get_feed_pub',
        type: 'GET',
        dataType: 'json',
        data: {number_elements: n_elems,type: tipo},
    })
    .done(function(data) {
        /*Render*/
        for(var i=0; i<data.length;i++){
            var div = $('<div class="col-md-4 banner-bottom-grid"> <a href="/single?id='+data[i]._id+'" > <img src="/get_image?path='+data[i].imagen+'"/>  </a><h4>'+data[i].nombre+'</h4> <p>'+data[i].resumen+'</p> </div>');
            $("#feed").append(div);
        }
        if(data.length < 6){
            var boton = document.getElementById("load_more_pub");
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
