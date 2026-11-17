// ============================================================
// main.js - comportamiento del sitio (menú móvil y animación
// de aparición al hacer scroll)
// ============================================================

// Avisa a la "red de seguridad" de base.html que este archivo sí cargó
window.mainCargado = true;

// 1) MENÚ HAMBURGUESA (solo se ve en pantallas chicas)
const cabecera = document.querySelector(".cabecera");
const boton = document.querySelector(".menu-boton");

if (cabecera && boton) {
  boton.addEventListener("click", () => {
    // classList.toggle devuelve true si la clase quedó puesta
    const abierto = cabecera.classList.toggle("abierto");
    boton.setAttribute("aria-expanded", abierto);
  });

  // Al elegir una sección, el menú se vuelve a cerrar
  document.querySelectorAll(".menu a").forEach((enlace) => {
    enlace.addEventListener("click", () => {
      cabecera.classList.remove("abierto");
      boton.setAttribute("aria-expanded", "false");
    });
  });
}

// 2) ANIMACIÓN DE APARICIÓN AL HACER SCROLL
// Los elementos con la clase "reveal" empiezan ocultos (ver style.css)
// y reciben la clase "visible" cuando entran en la pantalla.
const elementos = document.querySelectorAll(".reveal");

if ("IntersectionObserver" in window) {
  const observador = new IntersectionObserver(
    (entradas) => {
      entradas.forEach((entrada) => {
        if (entrada.isIntersecting) {
          entrada.target.classList.add("visible");
          observador.unobserve(entrada.target); // se anima una sola vez
        }
      });
    },
    { threshold: 0.15 }
  );
  elementos.forEach((el) => observador.observe(el));
} else {
  // Navegador viejo: mostramos todo sin animar
  elementos.forEach((el) => el.classList.add("visible"));
}
