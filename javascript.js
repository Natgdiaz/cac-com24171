/*-----carrusel-----*/
document.addEventListener('DOMContentLoaded', () => {
    const carruselInterno = document.getElementById('carrusel-interno');
    const carruselItems = carruselInterno.querySelectorAll('.carrusel-item');
    const botonPrev = document.getElementById('prev');
    const botonSig = document.getElementById('sig');
    let indiceActual = 0;

    function actualizarCarrusel() {
        const anchoItemCarrusel = carruselItems[0].offsetWidth;
        const desplazamiento = -indiceActual * anchoItemCarrusel;
        carruselInterno.style.transform = `translateX(${desplazamiento}px)`;
    }

    botonPrev.addEventListener('click', () => {
        indiceActual = (indiceActual > 0) ? indiceActual - 1 : carruselItems.length - 1;
        actualizarCarrusel();
    });

    botonSig.addEventListener('click', () => {
        indiceActual = (indiceActual < carruselItems.length - 1) ? indiceActual + 1 : 0;
        actualizarCarrusel();
    });

    // Initialize the carousel
    actualizarCarrusel();
});

/*-----menú hamburguesa-----*/
function alternarMenu() {
    const menu = document.getElementById('menu');
    menu.classList.toggle('mostrar');
}

/*-----validaciones registro-----*/
document.getElementById('form-registro').addEventListener('submit', function(evento) {
    evento.preventDefault();

    const usuario = document.getElementById('usuario').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const confirmarPassword = document.getElementById('confirmarPassword').value;
    const dob = document.getElementById('dob').value;
    const genero = document.querySelector('input[name="genero"]:checked');
    const intereses = document.querySelectorAll('input[name="intereses"]:checked');

    const formDatos = new FormData(evento.target);

    const datos = {};
    formDatos.forEach((valor, clave) => {
        datos[clave] = valor;
    });

    // Validaciones
    if (!validarUsuario(usuario)) {
        alert('El nombre de usuario debe tener al menos 3 caracteres.');
        return;
    }

    if (!validarEmail(email)) {
        alert('Por favor, ingresa un correo electrónico válido.');
        return;
    }

    if (!validarPassword(password)) {
        alert('La contraseña debe tener al menos 6 caracteres.');
        return;
    }

    if (password !== confirmarPassword) {
        alert('Las contraseñas no coinciden.');
        return;
    }

    if (!validarDob(dob)) {
        alert('Por favor, ingresa una fecha de nacimiento válida.');
        return;
    }

    if (!genero) {
        alert('Por favor, selecciona tu género.');
        return;
    }

    if (intereses.length === 0) {
        alert('Por favor, selecciona al menos un interés.');
        return;
    }

    alert('Registro exitoso y correo enviado.');
    window.location.href = 'index.html'; // Redirige al usuario después del registro
})

function validarUsuario(usuario) {
    return usuario.length >= 3;
}

function validarEmail(email) {
    const re = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
    return re.test(email);
}

function validarPassword(password) {
    return password.length >= 6;
}

function validarDob(dob) {
    const hoy = new Date();
    const fechaNacimiento = new Date(dob);
    return fechaNacimiento < hoy;
}

document.addEventListener('DOMContentLoaded', function () {
    const passwordInput = document.getElementById('password');
    const confirmarPasswordInput = document.getElementById('confirmarPassword');
    const botonAlternarPassword = document.getElementById('alternarPassword');
    const botonAlternarConfirmarPassword = document.getElementById('alternarConfirmarPassword');
    const iconoOjo = document.getElementById('icono-ojo');
    const confirmarIconoOjo = document.getElementById('confirmar-icono-ojo');

    botonAlternarPassword.addEventListener('click', function () {
        const tipo = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
        passwordInput.setAttribute('type', tipo);
        iconoOjo.classList.toggle('fa-eye');
        iconoOjo.classList.toggle('fa-eye-slash');
    });

    botonAlternarConfirmarPassword.addEventListener('click', function () {
        const tipo = confirmarPasswordInput.getAttribute('type') === 'password' ? 'text' : 'password';
        confirmarPasswordInput.setAttribute('type', tipo);
        confirmarIconoOjo.classList.toggle('fa-eye');
        confirmarIconoOjo.classList.toggle('fa-eye-slash');
    });
});

/*Comentarios*/
const formComentarios = document.getElementById('form-comentarios');
const inputComentarios = document.getElementById('input-comentarios');
const contenedorComentarios = document.getElementById('contenedor-comentarios');

formComentarios.addEventListener('submit', (evento) => {
    evento.preventDefault();
    const textoComentarios = inputComentarios.value;
    
    if (textoComentarios.trim() !== "") {
        const elementoComentarios = document.createElement('div');
        elementoComentarios.classList.add('comentario');
        elementoComentarios.innerText = textoComentarios;
        contenedorComentarios.appendChild(elementoComentarios);
        inputComentarios.value = ""; // Limpiar el campo de texto
    }
});

// validar la entrada en tiempo real
document.getElementById("usuario").addEventListener("input", function() {
    var usuarioInput = this; // Almacenar el elemento de entrada del usuario en una variable
    var usernameIcon = document.getElementById("username-icon"); // Obtener el icono asociado al nombre de usuario
    // Verificar si el valor del campo de entrada del usuario está vacío o no
    if (usuarioInput.value.trim().length > 0) {
        // Si el valor no está vacío, agregar la clase "valid" y quitar la clase "invalid" para aplicar estilos adecuados
        usuarioInput.classList.remove("invalid");
        usuarioInput.classList.add("valid");
        // Cambiar el icono a un check circle para indicar que el valor es válido
        usernameIcon.classList.remove("fa-times-circle");
        usernameIcon.classList.add("fa-check-circle");
    } else {
        // Si el valor está vacío, agregar la clase "invalid" y quitar la clase "valid" para aplicar estilos adecuados
        usuarioInput.classList.remove("valid");
        usuarioInput.classList.add("invalid");
        // Cambiar el icono a un cross circle para indicar que el valor es inválido
        usernameIcon.classList.remove("fa-check-circle");
        usernameIcon.classList.add("fa-times-circle");
    }
});

/*Imagen previa perfil*/
document.getElementById('foto-perfil').addEventListener('change', function(event) {
    var imagenPreview = document.getElementById('imagen-preview');
    var archivo = event.target.files[0];
    var lector = new FileReader();

    lector.onload = function(e) {
        imagenPreview.src = e.target.result;
        imagenPreview.style.display = 'block'; // Muestra la imagen previa
    };

    lector.readAsDataURL(archivo);
});

/*-----contraseña-----*/
document.getElementById('alternarPassword').addEventListener('click', function () {
    const passwordInput = document.getElementById('password');
    const icono = document.getElementById('icono-ojo');
    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        icono.classList.remove('fa-eye-slash');
        icono.classList.add('fa-eye');
    } else {
        passwordInput.type = 'password';
        icono.classList.remove('fa-eye');
        icono.classList.add('fa-eye-slash');
    }
});

/*-----Formulario de personajes
document.addEventListener('DOMContentLoaded',()=>{
const URL = "http://127.0.0.1:5000/" //Despues cambiar con la URL de pythonAnywhere

// Capturamos el evento de envío del formulario
document.getElementById('formulario').addEventListener('submit', function (event) {
    event.preventDefault(); // Evitamos que se envie el form 

    var formData = new FormData(this);

    // Realizamos la solicitud POST al servidor
    fetch(URL + 'personajes', {
        method: 'POST',
        body: formData // Aquí enviamos formData. Dado que formData puede contener archivos, no se utiliza JSON.
    })

    //Después de realizar la solicitud POST, se utiliza el método then() para manejar la respuesta del servidor.
    .then(function (response) {
        if (response.ok) { 
            //Si la respuesta es exitosa, convierte los datos de la respuesta a formato JSON.
            return response.json(); 
        } else {
            // Si hubo un error, lanzar explícitamente una excepción
            // para ser "catcheada" más adelante
            throw new Error('Error al agregar el personaje.');
        }
    })

    //Respuesta OK, muestra una alerta informando que el producto se agregó correctamente y limpia los campos del formulario para que puedan ser utilizados para un nuevo producto.
    .then(function (data) {
        alert('personaje agregado correctamente.');
    })

    // En caso de error, mostramos una alerta con un mensaje de error.
    .catch(function (error) {
        alert('Error al agregar el personaje.');
    })

    // Limpiar el formulario en ambos casos (éxito o error)
    .finally(function () {
        document.getElementById('nombre').value = "";
        document.getElementById('descripcion').value = "";
        document.getElementById('imagenPersonaje').value = "";
    });
});
})-----*/