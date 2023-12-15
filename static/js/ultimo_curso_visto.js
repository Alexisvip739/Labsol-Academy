async function cursoActual(id_curso,id_usuario) {
  let redireccionURL = `/clase/clases_estudiante/${id_curso}/`;

  try{
    const csrfToken = document.querySelector('#csrf-form [name=csrfmiddlewaretoken]').value;
    const data = await fetchData("/api/clases_vistas/", csrfToken);
    const clases_curso = data.filter(clase => clase.estudiante === id_usuario && clase.curso === id_curso);

    const fecha_reciente = Math.max(
      ...clases_curso.map((clase) => new Date(clase.fecha_ultima_visualizacion).getTime())
    );

    const ultima_clase_curso = clases_curso.find(clase => new Date(clase.fecha_ultima_visualizacion).getTime() === fecha_reciente);
    
    if (ultima_clase_curso) {
      redireccionURL = `/clase/clases_estudiante/${ultima_clase_curso.curso}/?page=${ultima_clase_curso.clase}`;
    }
  }
  catch(error){
    console.error("Error data:", error);
  }
  finally{
    window.location.href = redireccionURL;
  }
  
}

  async function fetchData(url, csrfToken) {
    try {
      const response = await axios.get(url, {
        headers: {
          'X-CSRFToken': csrfToken,
          'Content-type': 'application/json',
        },
      });
      return response.data;
    } catch (error) {
      console.error("Error fetching data:", error);
      throw error;
    }
  }

