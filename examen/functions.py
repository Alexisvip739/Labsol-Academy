from django.contrib import messages

def calcular_promedio(puntaje, total):
	promedio = (puntaje/total) * 100
	return promedio

def mensaje(request, porcentaje):
	if porcentaje< 60:
		messages.error(request, 'No has aprobado el examen, ¡Suerte para la próxima!.')
	elif porcentaje < 90:
		messages.warning(request, '¡Felicidades! Aprobaste el examen')
	elif porcentaje <100:
		messages.info(request, '¡Felicidades! Aprobaste el examen con un buen promedio')
	else:
		messages.success(request, '¡Felicidades! Aprobaste el examen con excelente promedio')