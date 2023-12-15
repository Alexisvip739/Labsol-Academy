$(document).ready(function() { 
    $('#btnFreeze').click(function() {
      // Obtenemos el valor de los campos
      var titulo = $('#id_titulo').val();
      var descripcion = $('#id_descripcion').val();
      var video = $('#id_video');
      var accion = $('#accion');
      $('#id_video').prop('required', true); // La propiedad required no esta cuando se actualiza una clase por ello se agrega aquí.

      if(accion.val()=='Editar'){
        // Validamos que el campo de título, descripción y video no estén vacíos
        if ( (titulo.trim() === '' || descripcion.trim() === '') ) {
          return;
        }

      }else{

        // Validamos que el campo de título, descripción y video no estén vacíos
        if ( (titulo.trim() === '' || descripcion.trim() === '') || !video[0].files[0] ) {
          return;
        }

        // Validamos que el archivo sea un MP4
        var inputFile = $('#id_video')[0];
        var file = inputFile.files[0];
        var fileName = file.name;
        var fileExtension = fileName.split('.').pop().toLowerCase();

        if (fileExtension !== 'mp4') {
          return
        }

      }
      
      // Si todos los campos pasan la validación, se pasa a subir o editar la clase
      $('#block-layer').show();
      $('#bloqueo').css('display', 'block');
      $('#spinner').show();
      $('body *').css('pointer-events', 'none');

    });
  

});
