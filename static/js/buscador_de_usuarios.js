function buscar_usuarios(tipo_usuario) {
    fetch('/api/usuarios/')
        .then((response) => response.json())
        .then((data) => {
            let resultados = data.filter(usuario => usuario.user_type === tipo_usuario);
            
            if (tipo_usuario === 'instructor') resultados = solicitud_instructores(resultados);

            return resultados;
        })
        .then( (resultados) => {
            buscador.addEventListener( 'input', () =>{
                const consulta = buscador.value.toLowerCase();
                const desplegar_info = document.getElementById("desplegar_info");

                if (consulta.trim() === '') {
                    desplegar_info.style.display = 'none';
                    return '';
                }else{
                    desplegar_info.style.display = 'block';

                    let coincidencias = resultados.filter( (usuario) => {
                        const nombre = (usuario.first_name+usuario.last_name).toLowerCase();
                        const nombre_usuario = usuario.username.toLowerCase();
                        return nombre.includes(consulta) || nombre_usuario.includes(consulta);
                    } )

                    if (coincidencias.length === 0) {
                        desplegar_info.innerHTML = `
                            <p class="text-center p-2 m-0">No se encontró el ${tipo_usuario}</p>
                        `;
                    } else {
                        const resultadoHTML = coincidencias.map( usuario => `
                        <div class="resultado_busqueda">
                            <a href="/usuario/editar/${usuario.id}/" class="resultado_info" style="text-decoration: none;">
                                <img src="${usuario.profile_picture}" class="perfil-busqueda">
                                <div>
                                    <p>${usuario.first_name} ${usuario.last_name}</p>
                                    <p class="fs-5 fst-italic">${usuario.username}</p>
                                </div>
                                
                            </a>  <a href="/usuario/eliminar/${usuario.id}/" class="w-20 btn btn-outline-danger">Eliminar</a>
                        </div>
                        
                     

                        `);
            
                        desplegar_info.innerHTML = resultadoHTML.join(''); 
                        desplegar_info.style.padding = '10px';
                    }
                }
            } );
        } )
        .catch(error => console.error('Error en la solicitud:', error));
}

/* filtrara solo a los instructores que no esten en solicitud */
async function solicitud_instructores(instructores) {
    try {
        let solicitudes = await (await fetch('/api/solicitudUsuarios/')).json();

        return instructores.filter( (instructor) => {
            const esta_en_solicitud = solicitudes.some(solicitud => solicitud.usuario === instructor.id);
            return !esta_en_solicitud;
        } )

    } catch (error) {
        console.error('Error en la solicitud de instructores:', error);
        return null
    }
}

const buscador = document.getElementById("buscador_usuario");

buscar_usuarios(buscador.dataset.usuario);