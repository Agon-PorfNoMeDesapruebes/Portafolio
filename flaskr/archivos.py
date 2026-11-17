import os
import uuid

from flask import current_app
from PIL import Image, ImageOps, UnidentifiedImageError


def guardar_imagen(archivo, lado_max=1200):
    """Verifica que sea una imagen real, la achica y la guarda como WebP.

    Devuelve el nombre del archivo guardado. Lanza ValueError si no es una imagen.
    """
    try:
        imagen = Image.open(archivo.stream)
        imagen = ImageOps.exif_transpose(imagen)
        if imagen.mode not in ("RGB", "RGBA"):
            imagen = imagen.convert("RGB")
        imagen.thumbnail((lado_max, lado_max))  # solo achica, nunca agranda
    except (UnidentifiedImageError, OSError, Image.DecompressionBombError):
        raise ValueError("El archivo no es una imagen válida.")

    nombre = f"{uuid.uuid4().hex}.webp"  # nombre propio: el del usuario no se usa
    carpeta = current_app.config["UPLOAD_FOLDER"]
    os.makedirs(carpeta, exist_ok=True)
    imagen.save(os.path.join(carpeta, nombre), "WEBP", quality=82)
    return nombre


def guardar_pdf(archivo):
    """Verifica que sea un PDF de verdad (por su cabecera) y lo guarda con nombre propio.

    Devuelve el nombre del archivo guardado. Lanza ValueError si no es un PDF.
    """
    cabecera = archivo.stream.read(5)
    archivo.stream.seek(0)
    if cabecera != b"%PDF-":
        raise ValueError("El archivo no es un PDF válido.")

    nombre = f"{uuid.uuid4().hex}.pdf"
    carpeta = current_app.config["UPLOAD_FOLDER"]
    os.makedirs(carpeta, exist_ok=True)
    archivo.save(os.path.join(carpeta, nombre))
    return nombre


def borrar_imagen(nombre):
    """Borra un archivo de la carpeta de subidas (si existe)."""
    if not nombre:
        return
    ruta = os.path.join(current_app.config["UPLOAD_FOLDER"], os.path.basename(nombre))
    if os.path.isfile(ruta):
        os.remove(ruta)