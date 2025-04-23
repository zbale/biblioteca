const form = document.getElementById('login-form');
form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const correo = document.getElementById('correo').value;
  const contraseña = document.getElementById('contraseña').value;

  try {
    const respuesta = await fetch('/auth/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ correo, contraseña })
    });

    const resultado = await respuesta.json();

    const modalBienvenida = new bootstrap.Modal(document.getElementById('modalBienvenida'));
    const mensajeBienvenida = document.getElementById('mensajeBienvenida');
    const btnIngresar = document.getElementById('btnIngresar');
    const btnIntentar = document.getElementById('btnIntentar'); // Nuevo botón

    if (respuesta.ok) {
      // Restablecer el botón "Ingresar" y el mensaje
      btnIngresar.style.display = 'block'; // Mostrar el botón "Ingresar"
      btnIntentar.style.display = 'none'; // Ocultar el botón "Intentar nuevamente"
      mensajeBienvenida.classList.remove('text-danger');
      mensajeBienvenida.classList.add('text-success');

      // Personalizar el mensaje según el rol
      if (resultado.usuario.rol === 1) {
        mensajeBienvenida.textContent = `Bienvenido, Superadministrador ${resultado.usuario.nombre}`;
        btnIngresar.onclick = () => {
          window.location.href = "/superadmin/dashboard";
        };
      } else if (resultado.usuario.rol === 2) {
        mensajeBienvenida.textContent = `Bienvenido, Estudiante ${resultado.usuario.nombre}`;
        btnIngresar.onclick = () => {
          window.location.href = "/estudiante/dashboard";
        };
      }

      modalBienvenida.show();
    } else {
      // Mostrar el modal con mensaje de error
      mensajeBienvenida.textContent = "Correo o contraseña incorrectos. Por favor, inténtalo de nuevo.";
      mensajeBienvenida.classList.remove('text-success');
      mensajeBienvenida.classList.add('text-danger');
      btnIngresar.style.display = 'none'; // Ocultar el botón "Ingresar"
      btnIntentar.style.display = 'block'; // Mostrar el botón "Intentar nuevamente"
      modalBienvenida.show();
    }
  } catch (error) {
    console.error("Error:", error);
    alert("Ocurrió un error al intentar iniciar sesión. Por favor, inténtalo más tarde.");
  }
});
