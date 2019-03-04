import os
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from django.core.files.temp import NamedTemporaryFile
from django.views.generic import View, ListView
from django.core.urlresolvers import reverse
from wsgiref.util import FileWrapper
from django.shortcuts import render
from django.conf import settings

from .forms import ImageUploadForm, ImageResizeForm
from .utils import resize_image
from .models import Image


class ImagesListView(ListView):
    model = Image
    context_object_name = 'images'
    template_name = 'images-list.html'
    paginate_by = 12


class UploadView(View):
    def get(self, request, *args, **kwargs):
        form = ImageUploadForm()
        return render(request, 'image-upload.html', {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = ImageUploadForm(request.POST, request.FILES)
        if not form.is_valid():
            return render(request, 'image-upload.html', {'form': form})
        file = form.cleaned_data['file']
        if form.cleaned_data['url']:
            file = form.cleaned_data['filename']
        image = Image()
        image.image_file = file
        image.save()
        return HttpResponseRedirect(reverse('image', kwargs={'pk': image.id}))


class ImageView(View):
    def get(self, request, *args, **kwargs):
        image = Image.objects.get(id=kwargs.get('pk'))
        form = ImageResizeForm()
        if len(request.GET) > 0:
            form = ImageResizeForm(request.GET)
            if not form.is_valid():
                return render(request, 'image.html', {'image_src': image.image_file.url, 'form': form})
            
            # Получение параметров из формы, к которым необходимо привести изображение
            width = form.cleaned_data['width']
            height = form.cleaned_data['height']
            size = form.cleaned_data['size']

            # Попытка приведения изображения к нужным параметрам и возврат ошибки при неудаче
            resize_result = resize_image(
                image,
                width if width else image.image_file.width,
                height if height else image.image_file.height,
                size,
            )
            if not resize_result:
                form.add_error(
                    None,
                    'Невозможно получить файл заданного размера {} Kb'.format(form.cleaned_data['size'])
                )
                return render(request, 'image.html', {'image_src': image.image_file.url, 'form': form})
            edited_file_url = '{}{}'.format(settings.MEDIA_URL, resize_result)
            return render(request, 'image.html', {'image_src': edited_file_url, 'form': form})
        return render(request, 'image.html', {'image_src': image.image_file.url, 'form': form})
