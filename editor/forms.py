import mimetypes
import shutil
import urllib
import os
from urllib.error import HTTPError
from django.conf import settings
from django import forms
from PIL import Image


class ImageUploadForm(forms.Form):
    file = forms.ImageField(label='Файл изображения', required=False)
    url = forms.URLField(label='Ссылка на изображение', required=False)

    def clean(self):
        data = super(ImageUploadForm, self).clean()
        if self._errors:
            return
        file = self.files.get('file')
        url = data.get('url')
        if file and url:
            self.add_error(None, 'Вы заполнили оба поля, выберите только один способ загрузки')
        elif not file and not url:
            self.add_error(None, 'Вы не заполнили ни одного поля')
        elif data.get('url'):
            try:
                # Получение изображения по ссылке и проверка, является ли полученный файл изображением
                file_path, http_message = urllib.request.urlretrieve(data.get('url'))
                im = Image.open(file_path)
                im.verify()
                im.close()

                # Формирование названия файла с расширением и перенос файла в media
                file_extension = mimetypes.guess_extension(http_message.__getitem__('Content-Type'))
                filename = os.path.basename(file_path)
                filename_with_extension = '{}{}'.format(filename, file_extension)
                new_file_path = os.path.join(
                    settings.MEDIA_ROOT,
                    filename_with_extension
                )
                data['filename'] = filename_with_extension
                shutil.move(file_path, new_file_path)
            except OSError:
                self.add_error('url', 'Файл по указанному адресу не является изображением')
                os.remove(file_path)
            except HTTPError:
                self.add_error('url', 'Невозможно получить изображение по данному адресу')


class ImageResizeForm(forms.Form):
    width = forms.IntegerField(label='Ширина', required=False, min_value=1, max_value=4000)
    height = forms.IntegerField(label='Высота', required=False, min_value=1, max_value=4000)
    size = forms.FloatField(label='Размер выходного файла(Kb)', required=False, min_value=0.1)

    def clean(self):
        data = super(ImageResizeForm, self).clean()
        if all(value == None for value in data.values()):
            self.add_error(None, 'Вы не заполнили ни одного поля')
