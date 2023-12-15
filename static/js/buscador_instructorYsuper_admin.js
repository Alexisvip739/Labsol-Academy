function buscarCursos(idUsuario) {
  const searchCurso = document.getElementById('buscador-cursos');
  const cardCurso = document.getElementById('card_display');
  
  cardCurso.style.flexWrap = 'wrap';
  let cursosUsuario = [];
  let searchArreglo=[]
  fetch('/api/solicitudCursos_api/')
    .then((response) => response.json())
    .then((data) => {
      searchArreglo = data;
      
    })

  fetch('/api/curso_api/')
    .then(response => {
      if (!response.ok) {
        throw new Error(`La solicitud falló con estado ${response.status}`);
      }
      return response.json();
    })
    .then(data => {
      
      if (idUsuario === 'admin') {
          cursosUsuario = data;
      } else {
        cursosUsuario = data.filter(curso => curso.instructor === idUsuario);
          
      }
        cursosInstructor=cursosUsuario.filter((dataResult)=>{
          return !searchArreglo.some(
            
            (searchResult)=> searchResult.curso === dataResult.id
          )
        })

       
        searchCurso.addEventListener('input', () => {
          const textoBusqueda = searchCurso.value.toLowerCase();
          const desplegarBuscador = document.getElementById('desplegar_info');

          if (textoBusqueda.trim() === '') {
              desplegarBuscador.style.display = 'none';
              return '';
          } else {
              desplegarBuscador.style.display = 'block';
              const cursosSimilares = cursosInstructor.filter(curso => {
                  const nombreCurso = curso.nombre.toLowerCase();
                  return nombreCurso.includes(textoBusqueda);
              });
      
              if (cursosSimilares.length === 0) {
                  desplegarBuscador.innerHTML = `
                      <p class="text-center p-2 m-0">No se encontró ningún curso</p>
                  `;
              } else {
                  const resultadoHTML = cursosSimilares.map(cursoEncontrado =>`
                  <div class="resultado_busqueda">
                    <a href="/curso/ver_curso/${cursoEncontrado.id}" class="resultado_info" style="text-decoration: none;">
                        <img src="${cursoEncontrado.miniatura}" class="miniatura-busqueda">
                        <p>${cursoEncontrado.nombre}</p>
                    </a>  
                  </div>
                  `);
      
                  // Asignar el contenido HTML al elemento desplegarBuscador
                  desplegarBuscador.innerHTML = resultadoHTML.join(''); // Usar join para convertir el array en una cadena
                  desplegarBuscador.style.padding = '10px';
              }
          }
      });
      
      
      
    });
}

const idUsuario = document.getElementById('id_usuario')
const idSuperAdmin = document.getElementById('id_super_admin');
  if (idUsuario) {
      buscarCursos(parseInt(idUsuario.textContent));
  }else if  (idSuperAdmin) {
      const userType = idSuperAdmin.getAttribute('data-user-type');
  if (userType === 'admin') {
      buscarCursos('admin');
  }

}
