
async function eliminarSuscripcion(estudianteId, cursoId) {
    try {
        const csrfToken = document.querySelector('#csrf-form [name=csrfmiddlewaretoken]').value;
        
        const data = await obtenerInscripciones();
        const curso = await obtenerCursosVistos();

        const elementoEliminar = data.find(item => (item.curso === cursoId && item.estudiante === estudianteId));
        const cursosVisto=curso.find(item=>(item.curso===cursoId && item.estudiante === estudianteId))
        if (elementoEliminar && cursosVisto ) {
            await eliminarInscripcion(elementoEliminar.id, csrfToken);
            await cursoVistoEliminar(cursosVisto.id,csrfToken)
            window.location.reload();
        }
    } catch (error) {
        console.error(error);
    }
}

async function obtenerInscripciones() {
    try {
        const response = await fetch('/api/inscripcion/');
        const data = await response.json();
        return data;
    } catch (error) {
        throw new Error('Error al obtener los datos');
    }
}
async function obtenerCursosVistos(){
    try {
        const response = await fetch('/api/clases_vistas/');
        const data = await response.json();
        return data;
    } catch (error) {
        throw new Error('Error al obtener los datos');
    }
}
async function eliminarInscripcion(idEliminar, csrfToken) {
    try {
        const response = await fetch(`/api/inscripcion/${idEliminar}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
        });
        if (!response.ok) {
            throw new Error('Error al eliminar la suscripción');
        }
    } catch (error) {
        throw new Error('Error al realizar la solicitud DELETE');
    }
}
async function cursoVistoEliminar(idEliminar,csrfToken){
    try {
        const response = await fetch(`/api/clase_vista/${idEliminar}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
        });
        if (!response.ok) {
            throw new Error('Error al eliminar la suscripción');
        }
    } catch (error) {
        throw new Error('Error al realizar la solicitud DELETE');
    }
}