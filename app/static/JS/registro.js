const form = document.getElementById('register-form');
const mensaje = document.getElementById('mensaje');

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const nombre = document.getElementById('nombre').value;
  const correo = document.getElementById('correo').value;
  const contraseña = document.getElementById('contraseña').value;

  try {
    const respuesta = await fetch('/auth/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ nombre, correo, contraseña })
    });

    const resultado = await respuesta.json();
    mensaje.textContent = resultado.mensaje;
    mensaje.style.display = "block";

    if (respuesta.ok) {
      mensaje.style.backgroundColor = "#388e3c";
      form.reset();
    } else {
      mensaje.style.backgroundColor = "#d32f2f";
    }
  } catch (error) {
    console.error("Error al registrar:", error);
    mensaje.textContent = "Ocurrió un error durante el registro.";
    mensaje.style.display = "block";
    mensaje.style.backgroundColor = "#d32f2f";
  }
});
