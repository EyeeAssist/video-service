import pytube
import re
import uuid
import cv2
import numpy as np
from PIL import Image


def download_video(url: str):
    """
    Descarga un video de YouTube a un archivo local.
      Args:
      url: La URL del video de YouTube.
    Returns:
        El nombre del archivo local donde se guardó el video.
    """
    video = pytube.YouTube(url)

    print(video.title)
    print(video.length)
    filename = str(uuid.uuid4()) + ".mp4"
    video.streams.filter(file_extension="mp4").get_highest_resolution().download(filename=filename)
    return filename


def is_youtube_url(url):
    """
    Valida si un string es un link de YouTube.

    Args:
        url: El string a validar.

    Returns:
        True si el string es un link de YouTube, False si no.
    """

    regex = r"^(?:https?:\/\/)?(?:m\.|www\.)?(?:youtu\.be\/|youtube\.com\/(?:embed\/|v\/|watch\?v=|watch\?.+&v=))((\w|-){11})(?:\S+)?$"

    match = re.match(regex, url)

    return match is not None


def calcular_similitud(img1, img2):
    # Convierte las imágenes a espacios de color HSV
    hsv_img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV)
    hsv_img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2HSV)

    # Calcula los histogramas 2D de las imágenes
    hist_img1 = cv2.calcHist([hsv_img1], [0, 1], None, [180, 256], [0, 180, 0, 256])
    hist_img2 = cv2.calcHist([hsv_img2], [0, 1], None, [180, 256], [0, 180, 0, 256])

    # Normaliza los histogramas
    cv2.normalize(hist_img1, hist_img1, 0, 1, cv2.NORM_MINMAX)
    cv2.normalize(hist_img2, hist_img2, 0, 1, cv2.NORM_MINMAX)

    # Calcula la similitud entre los histogramas usando la distancia de Bhattacharyya
    similitud = cv2.compareHist(hist_img1, hist_img2, cv2.HISTCMP_BHATTACHARYYA)

    return similitud


def es_frame_borrosa(frame, umbral_variacion_gradiente=100):
    # Convierte el frame a escala de grises
    frame_gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Calcula el gradiente usando el operador Sobel
    gradiente_x = cv2.Sobel(frame_gris, cv2.CV_64F, 1, 0, ksize=5)
    gradiente_y = cv2.Sobel(frame_gris, cv2.CV_64F, 0, 1, ksize=5)

    # Calcula la magnitud del gradiente
    magnitud_gradiente = np.sqrt(gradiente_x**2 + gradiente_y**2)

    # Calcula la varianza de la magnitud del gradiente
    varianza_gradiente = np.var(magnitud_gradiente)

    # Compara la varianza con el umbral
    return varianza_gradiente < umbral_variacion_gradiente

def read_video(path):
    video = cv2.VideoCapture(path)
    if not video.isOpened():
        print('Error al abrir video')
        return None

    frame_interval = 100

    frames_list = []
    current_time = 0.0
    print('Leyendo video ->', path)
    while True:
        video.set(cv2.CAP_PROP_POS_MSEC, current_time)
        ret, frame = video.read()
        if not ret:
            break
        tiempo_actual = video.get(cv2.CAP_PROP_POS_MSEC)/1000
        print('Leyendo tiempo -> ', tiempo_actual)
        if current_time == 0.0:
            imagen_pillow = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            frames_list.append({'time': tiempo_actual,
                                'frame_image': imagen_pillow.convert("RGB"),
                                'cv_image': frame})
        elif current_time > 0.0 and frames_list[-1]:
            similitud = calcular_similitud(frames_list[-1]['cv_image'], frame)
            print('Similitud ->', similitud)
            if similitud > 0.69 and not es_frame_borrosa(frame):
                imagen_pillow = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                frames_list.append({'time': tiempo_actual,
                                    'frame_image': imagen_pillow.convert("RGB"),
                                    'cv_image': frame})

        current_time += frame_interval

    video.release()
    cv2.destroyAllWindows()
    return frames_list
