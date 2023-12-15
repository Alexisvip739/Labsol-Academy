input_password1 = document.getElementById('id_new_password1');
input_password1.classList.add("form-control");
input_password1.classList.add("form-control-sm");
input_password1.classList.add("mb-2");
input_password1.placeholder = "Escribe la nueva contraseña";

input_password2 = document.getElementById('id_new_password2');
input_password2.classList.add("form-control");
input_password2.classList.add("form-control-sm");
input_password2.placeholder = "Confirma la nueva contraseña";

error_p = document.getElementById("errors");
error_p.classList.add('text-danger');