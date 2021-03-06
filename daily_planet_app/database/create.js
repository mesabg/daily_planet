db = db.getSiblingDB('daily_planet_db');
print("-----Inicializando la base de datos-----");

db.createCollection("usuarios");
db.createCollection("articulos");


var array_usuarios = [
    {
        _id: 1,
        correo: "ricardodpds2112@gmail.com",
        password: "123456789",
        tipo: "editor",  
        nombre: "Ricardo",
        avatar: "local_images/user/1.png",
        descripcion: "Hola mi nombre es Ricardo"
    },
    {
        _id: 2,
        correo: "moises.berenguer@yahoo.com",
        password: "123456789",
        tipo: "autor",
        nombre: "Moises",
        avatar: "local_images/user/2.png",
        descripcion: "Hola yo soy Moises"
    },
    {
        _id: 3,
        correo: "carlos.perez@gmail.com",
        password: "123456789",
        tipo: "lector",
        nombre: "Carlos",
        avatar: "local_images/user/2.png",
        descripcion: "Hola yo soy Carlos"
    }
]

//autor: "id del usuario autor", editor: "id del usuario editor", favoritos: "array de usuarios que han indicado que es su favorito"
var array_articulos = [
    {
        _id: 1,
        nombre: "Articulo interesante",
        favoritos: [1,2],
        autor: 1,
        editor: [2],
        publicado: true,
        resumen: "Lorem ipsum consectetur adipiscing elit",
        palabras: "Lorem, Ipsum, Dolor, Sit, Amet",
        cuerpo: "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus id metus non lectus posuere sollicitudin. Nullam venenatis, turpis ac mperdiet dignissim, nisi lectus rhoncus diam, ac malesuada felis augue at lectus. Integer eu justo in nulla hendrerit venenatis eget vel tellus. Sed tincidunt, odio a tincidunt sodales, augue risus sodales velit, sit amet rutrum mauris eros id lacus. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce accumsan lectus sed dolor convallis, ut ultricies arcu pretium. Morbi commodo consequat quam ac blandit. Fusce sodales pretium tortor id congue. Quisque et auctor odio. Fusce sem lorem, blandit ac imperdiet et, auctor eget ligula. Quisque ac felis est. Mauris gravida lacinia ex, a euismod eros faucibus at. Cras eget suscipit enim. Aliquam a faucibus dolor.Vivamus at mattis quam. Donec at luctus diam. Sed malesuada maximus tortor. Proin sodales lobortis lectus, sed pellentesque neque volutpat eget. Suspendisse vitae tellus ex. Duis fermentum ligula sem, ut bibendum eros bibendum vel. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; In vulputate tortor diam. Proin finibus dignissim odio quis maximus.",
        n_comment: 4,
        editando: "No",
        comentarios:  [
            {
             _id: 1, 
             nombre: "Ricardo",
             cuerpo: "Muy Interesante todo ",
             fecha: new Date( Date() ),
             respuestas: [{
                     _id: 2,
                     nombre: "Moises",
                     cuerpo: ":) excelente",
                     fecha: new Date( Date() ),
                     respuestas: []
                     
                    } ,{
                     _id: 3,
                     nombre: "Moises",
                     cuerpo: ":) perfecto",
                     fecha: new Date( Date() ),
                     respuestas: []
                    }],
              },{
               _id: 4,
                 nombre: "Moises",
                 cuerpo: "oh vaya! :/",
                 fecha: new Date( Date() ),
                 respuestas: [] 
            }],
        fecha: new Date( Date() ),
        categoria: "Noticias",
        imagen: "local_images/art/1.jpg"
    },{
        _id: 2,
        nombre: "Articulo no tan interesante",
        favoritos: [],
        autor: 1,
        editor: [],
        publicado: false,
        resumen: "Este no es el lorem",
        palabras: "Es el, Phasellus id metus non lectus, no tan interesante",
        cuerpo: "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus id metus non lectus posuere sollicitudin. Nullam venenatis, turpis ac mperdiet dignissim, nisi lectus rhoncus diam, ac malesuada felis augue at lectus. Integer eu justo in nulla hendrerit venenatis eget vel tellus. Sed tincidunt, odio a tincidunt sodales, augue risus sodales velit, sit amet rutrum mauris eros id lacus. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce accumsan lectus sed dolor convallis, ut ultricies arcu pretium. Morbi commodo consequat quam ac blandit. Fusce sodales pretium tortor id congue. Quisque et auctor odio. Fusce sem lorem, blandit ac imperdiet et, auctor eget ligula. Quisque ac felis est. Mauris gravida lacinia ex, a euismod eros faucibus at. Cras eget suscipit enim. Aliquam a faucibus dolor.Vivamus at mattis quam. Donec at luctus diam. Sed malesuada maximus tortor. Proin sodales lobortis lectus, sed pellentesque neque volutpat eget. Suspendisse vitae tellus ex. Duis fermentum ligula sem, ut bibendum eros bibendum vel. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; In vulputate tortor diam. Proin finibus dignissim odio quis maximus.",
        n_comment: 0,
        editando: "No",
        comentarios:  [],
        fecha: new Date("October 12 2006 00:00:00"),
        categoria: "Intereses",
        imagen: "local_images/art/2.jpg"
    }
]


for ( var i = 0; i < array_usuarios.length; i++ ) db.usuarios.insert(array_usuarios[i]);

for ( var i = 0; i < array_articulos.length; i++ ) db.articulos.insert(array_articulos[i]);

print("------Creación exitosa de la base de datos-----")








