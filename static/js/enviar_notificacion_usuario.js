const form = document.getElementById("form-notificacion");

form.addEventListener( "submit", (event) => {
    event.preventDefault();
    var formData = new FormData(event.target);
    fetch(`/notificacion/enviar_notificacion/`, {
      method: "POST",
      body: formData
    })
    .then(function(response) {
      return response.json();
    })
    .then(function(data) {
      if (data && data.success) {
        document.getElementById("notificacion").hidden = true;
        document.getElementById("form-notificacion").reset();
        location.reload()
      } else {
        // Mostramos errores relacionados al enviar una notificacion
        if(data.error){ 
          document.getElementById("div_error").hidden = false;
          document.getElementById("error").textContent = data.error
        }

        for (var field in data.errors) {
          var error = data.errors[field];
          var input = document.getElementById('id_notificacion_'+field);
          input.hidden = false;
          input.textContent = error;
        }
        
      }
    })
    .catch(function(error){
        console.error('Error en la solicitud: ', error);
    });
} );
