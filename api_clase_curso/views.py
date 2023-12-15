from django.http import Http404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from curso.models import Curso, Inscripcion, SolicitudCurso
from .serializers import  ClaseSerializers, ClaseVistaSerializers, CursoSerializers, InscripcionSerializers, SolicitudSerializers, UsuarioPersonalizadoSerializers, SolicitudUsuarioSerializers
from clase.models import Clase, VistaClase
from usuario.models import UsuarioPersonalizado, Solicitud

# Create your views here.
# Create your views here.

class Clase_APIView(APIView): 
    def get(self, request, format=None, *args, **kwargs):
        post = Clase.objects.all()
        serializer = ClaseSerializers(post, many=True)
        
        return Response(serializer.data)
    def post(self, request, format=None):
        serializer = ClaseSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class Clase_APIView_Detail(APIView):
    def get(self, request, pk, format=None):
        try:
            clase = Clase.objects.get(pk=pk)
        except Clase.DoesNotExist:
            raise Http404

        serializer = ClaseSerializers(clase)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        try:
            clase = Clase.objects.get(pk=pk)
        except Clase.DoesNotExist:
            raise Http404

        serializer = ClaseSerializers(clase, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        try:
            clase = Clase.objects.get(pk=pk)
        except Clase.DoesNotExist:
            raise Http404

        serializer = ClaseSerializers(clase, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        try:
            clase = Clase.objects.get(pk=pk)
        except Clase.DoesNotExist:
            raise Http404

        clase.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class Curso_APIView(APIView):
    def get(self, request, format=None, *args, **kwargs):
        post = Curso.objects.all()
        serializer = CursoSerializers(post, many=True)
        
        return Response(serializer.data)
    def post(self, request, format=None):
        serializer = CursoSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class Inscripcion_APIView(APIView): 
    def get(self, request, format=None, *args, **kwargs):
        post = Inscripcion.objects.all()
        serializer = InscripcionSerializers(post, many=True)
        
        return Response(serializer.data)
    def post(self, request, format=None):
        serializer = InscripcionSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        try:
            clase = Inscripcion.objects.get(pk=pk)
        except Inscripcion.DoesNotExist:
            raise Http404

        Inscripcion.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class Inscripcion_APIView_Detail(APIView):
    def get(self, request, pk, format=None):
        try:
            inscripcion = Inscripcion.objects.get(pk=pk)
        except Inscripcion.DoesNotExist:
            raise Http404

        serializer = InscripcionSerializers(inscripcion)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        try:
            inscripcion = InscripcionSerializers.objects.get(pk=pk)
        except Clase.DoesNotExist:
            raise Http404

        serializer = InscripcionSerializers(inscripcion, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        try:
            inscripcion = Inscripcion.objects.get(pk=pk)
        except Clase.DoesNotExist:
            raise Http404

        serializer = InscripcionSerializers(inscripcion, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        try:
            inscripcion = Inscripcion.objects.get(pk=pk)
        except Inscripcion.DoesNotExist:
            raise Http404

        inscripcion.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)





class ClaseVista_APIView(APIView): 
    def get(self, request, format=None, *args, **kwargs):
        post = VistaClase.objects.all()
        serializer = ClaseVistaSerializers(post, many=True)
        
        return Response(serializer.data)
    def post(self, request, format=None):
        serializer = ClaseVistaSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class ClaseVista_APIView_Detail(APIView):
    def get(self, request, pk, format=None):
        try:
            clase_vista = VistaClase.objects.get(pk=pk)
        except VistaClase.DoesNotExist:
            raise Http404

        serializer = ClaseVistaSerializers(clase_vista)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        try:
            clase_vista = ClaseVistaSerializers.objects.get(pk=pk)
        except VistaClase.DoesNotExist:
            raise Http404

        serializer = ClaseVistaSerializers(clase_vista, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        try:
            clase_vista = VistaClase.objects.get(pk=pk)
        except VistaClase.DoesNotExist:
            raise Http404

        serializer = ClaseVistaSerializers(clase_vista, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        try:
            clase_vista = VistaClase.objects.get(pk=pk)
        except VistaClase.DoesNotExist:
            raise Http404

        clase_vista.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class UsuarioPersonalizado_APIView_Detail(APIView):
     def get(self, request, format=None, *args, **kwargs):
        post = UsuarioPersonalizado.objects.all()
        serializer = UsuarioPersonalizadoSerializers(post, many=True)
        return Response(serializer.data)
        

class SolicituCursoVista_APIView(APIView): 
    def get(self, request, format=None, *args, **kwargs):
        post = SolicitudCurso.objects.all()
        serializer = SolicitudSerializers(post, many=True)
        return Response(serializer.data)    
    
class SolicitudUsuario_APIView(APIView):
    def get(self, request, format=None, *args, **kwargs):
        post = Solicitud.objects.all()
        serializer = SolicitudUsuarioSerializers(post, many=True)
        return Response(serializer.data)