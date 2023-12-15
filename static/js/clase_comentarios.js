function borrarComentario(id) {
    form = document.getElementById(id);
    form.elements["contenido"].value = "";
}


function enviarComentario(url, id) {
    var formData = new FormData(document.getElementById(id));

    fetch(url, {
    method: "POST",
    body: formData,
    })
    .then(function (response) {
        return response.json();
    })
    .then(function (data) {
        if (data.success) {
        borrarComentario(id);
        location.reload();
        } else {
        for (var field in data.errors) {
            var error = data.errors[field];
            var input = document.getElementById("id_" + field);
            input.classList.add("error");
            input.nextSibling.textContent = error;
        }
        }
    });
}


function displayContainer(id) {
    let container = document.getElementById(id);
    if (container.style.display === "none") {
        container.style.display = "block";
    } else {
        container.style.display = "none";
    }
}

let comentario = document.getElementById("contenedor-comentarios");

    comentario.addEventListener("click", function (event) {
        event.preventDefault();
        let id = event.target.dataset.id;
        let type = event.target.dataset.type;
        if (type == "send") {
            enviarComentario(`/clase/agregar_comentario/`, id);
        } else if (type == "cancel") {
            borrarComentario(id);
        } else if (type == "display-block") {
            displayContainer(id);
        }
});