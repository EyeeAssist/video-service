import pytube
import re
import uuid


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
