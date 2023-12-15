document.addEventListener("DOMContentLoaded", function () {
  const etiquetaContainers = document.querySelectorAll(".etiqueta-container");

  // Función para mostrar u ocultar el texto
  function toggleTextoCompleto(container) {
    const descripcion = container.querySelector(".card-text");
    const btnLeerMas = container.querySelector(".leer-mas-btn");
    const mostrandoTextoCompleto = descripcion.style.whiteSpace === "normal";

    if (mostrandoTextoCompleto) {
      descripcion.style.whiteSpace = "nowrap";
      descripcion.style.overflow = "hidden";
      descripcion.style.textOverflow = "ellipsis";
      btnLeerMas.textContent = "Leer mas";
    } else {
      descripcion.style.whiteSpace = "normal";
      descripcion.style.overflow = "visible";
      descripcion.style.textOverflow = "inherit";
      btnLeerMas.textContent = "Ocultar";
    }
  }

  // Agregar la función de toggleTextoCompleto a todas las etiquetas al cargar la página
  etiquetaContainers.forEach(function (container) {
    const descripcion = container.querySelector(".card-text");
    const btnLeerMas = container.querySelector(".leer-mas-btn");

    if (descripcion.scrollWidth > descripcion.clientWidth) {
      btnLeerMas.style.display = "block";
    }

    btnLeerMas.addEventListener("click", function () {
      toggleTextoCompleto(container);
    });
  });
});

