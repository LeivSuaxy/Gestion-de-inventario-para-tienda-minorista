from PIL import Image
from io import BytesIO
import os
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def process_image(image):
    img = Image.open(image)

    if img.width != 1024 and img.height != 1024:
        img = img.resize((1024, 1024))
        buffer = BytesIO()
        img.save(fp=buffer, format='PNG')
        path = default_storage.save('stock/' + image.name, ContentFile(buffer.getvalue()))
        url_imagen = os.path.join(path)
    else:
        path = default_storage.save('stock/' + image.name, ContentFile(image.read()))
        url_imagen = os.path.join(path)

    return url_imagen
