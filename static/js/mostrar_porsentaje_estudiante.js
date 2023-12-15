const csrfToken = document.querySelector('#csrf-form [name=csrfmiddlewaretoken]').value;

async function obtenerDatosApi() {
  try {
    const usuario_id = parseInt(document.getElementById("id_usuario").textContent);
    const responseCursosVistos = await obtenerCursosVistos();
    
    const InscripcionesUsuario = responseCursosVistos.filter(cursos_usuario => cursos_usuario.estudiante === usuario_id);
    
    await mostrarCursosConPromedio(InscripcionesUsuario);
  } catch (error) {
    console.error('Error:', error);
  }
}

async function obtenerCursosVistos() {
  const response = await axios.get('/api/clases_vistas/', {
    headers: {
      'X-CSRFToken': csrfToken,
      'Content-type': 'application/json',
    },
  });
  
  return response.data;
}

async function obtenerCursosYClases() {
  const [responseCursos, responseClases] = await Promise.all([
    axios.get('/api/curso_api/', {
      headers: {
        'X-CSRFToken': csrfToken,
        'Content-type': 'application/json',
      },
    }),
    axios.get('/api/clase_api/', {
      headers: {
        'X-CSRFToken': csrfToken,
        'Content-type': 'application/json',
      },
    }),
  ]);

  return {
    cursos: responseCursos.data,
    clases: responseClases.data,
  };
}

function calcularPromedioPorcentaje(clasesVistasCount, totalClases) {
  return (clasesVistasCount / totalClases) * 100;
}

    
  
async function mostrarCursosConPromedio(data_curso) {
  const data = await obtenerCursosYClases();
  const cursosContainer = document.getElementById('cursos-container');
  const obtenerCursosVistos = data_curso;

  const cursosVistosCount = new Map();
  const cursosMostrados = new Set(); // Set to keep track of displayed courses

  if (obtenerCursosVistos.length === 0) {
    document.getElementById('sin_cursos').style.display = 'flex';
  } else {
    document.getElementById('sin_cursos').style.display = 'none';

    obtenerCursosVistos.forEach(item => {
      const cursosEncontrados = data.cursos.filter(cursos => cursos.id === item.curso);

      cursosEncontrados.forEach(curso => {
        if (!cursosMostrados.has(curso.id)) {
          const clasesDelCurso = data.clases.filter(clase => clase.curso === curso.id);
          const clasesVistas = obtenerCursosVistos.filter(visto => visto.curso === curso.id);

          const totalClases = clasesDelCurso.length;
          const clasesVistasCount = clasesVistas.length;

          if (totalClases > 0) {
            const averagePorcentaje = calcularPromedioPorcentaje(clasesVistasCount, totalClases);

            const cardContainer = `
              <div class="col-lg-6">
                <div class="card">
                  <div class="card-body">
                    <div class="row align-items-center">
                      <div class="col-3">
                        <img class="rounded course-image" src="${curso.miniatura}" style="width: 100px; height: 90px;">
                      </div>
                      <div class="col">
                        <h3 class="card-title mb-1">
                          <a href="/clase/clases_estudiante/${item.id}" class="text-reset" style="white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 300px;">
                            ${curso.nombre}
                          </a>
                        </h3>
                        <div class="text-muted">Ha mirado ${clasesVistasCount} de ${totalClases} clases</div>
                        <div class="mt-3">
                          <div class="row g-2 align-items-center">
                            <div class="col-auto">${averagePorcentaje.toFixed(2)}%</div>
                            <div class="col">
                              <div class="progress progress-sm">
                                <div class="progress-bar" style="width: ${averagePorcentaje}%" role="progressbar" aria-valuenow="${averagePorcentaje}" aria-valuemin="0" aria-valuemax="100" aria-label="${averagePorcentaje}% Completado">${averagePorcentaje}% Visto</div>
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            `;

            cursosContainer.insertAdjacentHTML('beforeend', cardContainer);

            // Add the course ID to the set of displayed courses
            cursosMostrados.add(curso.id);
          }
        }
      });
    });
  }
}

// Rest of your code remains the same...


obtenerDatosApi();