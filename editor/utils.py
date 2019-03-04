import shutil
import os
from django.conf import settings
from PIL import Image

def resize_image(image_object, width, height, size=None):
    """

    Создаёт копию переданного изображения в папке media,
    и изменяет размеры изображения в соответствии с переданными,
    а также приводит файл к нужному размеру (Kb).
    Возвращает название нового файла, либо False при неудаче.

    """
    filename, file_extension = os.path.splitext(image_object.image_file.name)
    edited_filename = '{}{}{}'.format(filename, '_edited', file_extension)
    output_file = os.path.join(
        settings.MEDIA_ROOT,
        edited_filename
    )
    shutil.copyfile(
        image_object.image_file.path,
        output_file
    )
    image = Image.open(output_file)
    image = image.resize(
        (width, height),
        Image.ANTIALIAS
    )
    image.save(output_file, optimize=True)
    if size:
        if os.stat(output_file).st_size / 1024 > float(size):
            result = change_image_filesize(image, size, output_file)
            if not result:
                return False
    return edited_filename

def change_image_filesize(image, size, output_file, quality=95):
    """

    Приводит изображение к нужному размеру файла (Kb), путём ухудшения качества.
    Результат записывается в output_file. Функция работает рекурсивно,
    постепенно ухудшая качество изображения.
    Возвращает True, либо False при неудаче.

    """
    if quality == 0:
        return False
    image.save(output_file, optimize=True, quality=quality)
    if os.stat(output_file).st_size / 1024 > size:
        result = change_image_filesize(image, size, output_file, quality - 5)
        if not result:
            return False
    return True

