// Script para ocultar el botón cuando el menú está abierto
const menuButton = document.getElementById('menuButton');
const menuLateral = document.getElementById('menuLateral');

// Ocultar el boton
menuLateral.addEventListener('shown.bs.offcanvas', function () {
  menuButton.classList.add('btn-menu-hidden');
});

// Muestra el botón cuando se cierra el menú (sin importar cómo se cerró)
menuLateral.addEventListener('hidden.bs.offcanvas', function () {
  menuButton.classList.remove('btn-menu-hidden');
});
