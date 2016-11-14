function login() {
    if (!$('.login').hasClass('visible')) {
        $('.login').css({
            visibility: 'visible',
            opacity: 0,
            "z-index": 100
        });
        $('.content').animate({
            opacity: 0.2
        }, 1000);
        $('.login').animate({
            opacity: 1
        }, 1000);
        $(".login").addClass('visible');
        if ($('.forgetpass').hasClass('visible')) {
            $('.forgetpass').animate({
                opacity: 0
            }, 1000, function() {
                $('.forgetpass').css({
                    visibility: 'hidden',
                    "z-index": 0
                });
            });
            $(".forgetpass").removeClass('visible');
        }
    }
}

function cancel() {
    if ($('.login').hasClass('visible')) {
        $('.content').animate({
            opacity: 1
        }, 1000);
        $('.login').animate({
            opacity: 0
        }, 1000, function() {
            $('.login').css({
                visibility: 'hidden',
                "z-index": 0
            });
        });
        $(".login").removeClass('visible');
    }
    if ($('.forgetpass').hasClass('visible')) {
        $('.content').animate({
            opacity: 1
        }, 1000);
        $('.forgetpass').animate({
            opacity: 0
        }, 1000, function() {
            $('.forgetpass').css({
                visibility: 'hidden',
                "z-index": 0
            });
        });
        $(".forgetpass").removeClass('visible');
    }
}

function forgetpass() {
    if (!$('.forgetpass').hasClass('visible')) {
        $('.forgetpass').css({
            visibility: 'visible',
            opacity: 0,
            "z-index": 100
        });
        $('.content').animate({
            opacity: 0.2
        }, 1000);
        $('.forgetpass').animate({
            opacity: 1
        }, 1000);
        $(".forgetpass").addClass('visible');
        if ($('.login').hasClass('visible')) {
            $('.login').animate({
                opacity: 0
            }, 1000, function() {
                $('.login').css({
                    visibility: 'hidden',
                    "z-index": 0
                });
            });
            $(".login").removeClass('visible');
        }
    }
}


function publicar(element){
    var form = {
        nombre: element.getElementsByClassName('Nombre')[1].innerHTML,
        fecha: element.getElementsByClassName('Fecha')[1].innerHTML
    }
    
    $.post( "/crear_save", form );
}