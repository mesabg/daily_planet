var n_elems = 6;


jQuery(document).ready(function($) {
    load_more_pub();
    $("#load_more_pub").click(function(){
        load_more_pub();
    });
});


function load_more_pub(){
    $.ajax({
        url: '/get_feed',
        type: 'GET',
        dataType: 'json',
        data: {number_elements: n_elems},
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