import base64
import subprocess
from django.conf import settings
import os

def eliminar_archivo(ruta_archivo):
    if os.path.exists(ruta_archivo):
        try:
            os.remove(ruta_archivo)
            print(f"SE ELIMINIÓ EL ARCHIVO: {ruta_archivo}")
        except OSError as e:
            print(f"No se pudo eliminar el archivo en {ruta_archivo}. Error: {e}")
        except:
            print(f"NO SE PUDO ELIMINAR EL ARCHIVO {ruta_archivo}")
    else:
        print(f"El archivo {ruta_archivo} no existe.")

def comprimir_video(video, cadena_timestamp):

    try:
        # Ruta del video original
        ruta_video_original = os.path.join(settings.BASE_DIR, str(video) )
        ruta_video_destino = os.path.join(settings.BASE_DIR, 'media/videos/comp_' + str(cadena_timestamp) + str('.mp4') )
        ruta_de_video_relativa = os.path.relpath(ruta_video_destino,settings.MEDIA_ROOT)
        
        # Comando ffmpeg para comprimir el video
        # Para poder modificar la calidad del video es necesario modificar este comando 
        comando = f"ffmpeg -i {ruta_video_original} -vcodec libx264 -crf 28 {ruta_video_destino}"
        
        # Ejecutar el comando ffmpeg
        subprocess.call(comando, shell=True)
        
        # Devolver la nueva ruta
        return ruta_de_video_relativa
    except:
        return None
    
   