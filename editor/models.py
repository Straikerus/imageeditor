from django.core.urlresolvers import reverse
from django.db import models


class Image(models.Model):
    image_file = models.ImageField('Файл изображения')

    def __str__(self):
        return str(self.id)
    
    def get_absolute_url(self):
        return reverse('image', kwargs={'pk': self.id})

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'
