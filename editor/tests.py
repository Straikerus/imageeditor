from django.test import TestCase
from .forms import ImageUploadForm, ImageResizeForm


class ImageUploadFormTests(TestCase):
    def setUp(self):
        self.form_class = ImageUploadForm
    
    def test_form_validators(self):
        # Тест валидатора при пустых полях формы
        form = self.form_class(data={'file': '', 'url': ''})
        self.assertEqual(form.is_valid(), False)

        # Тест валидатора при полных полях формы
        form = self.form_class(data={'file': 'file', 'url': 'url'})
        self.assertEqual(form.is_valid(), False)

        # Тест валидатора при указании в поле url ссылки не на изображение
        form = self.form_class(data={'file': '', 'url': 'https://google.com'})
        self.assertEqual(form.is_valid(), False)


class ImageResizeFormTests(TestCase):
    def setUp(self):
        self.form_class = ImageResizeForm
    
    def test_form_validators(self):
        # Тест валидатора при пустых полях формы
        form = self.form_class(data={'width': '', 'height': '', 'size': ''})
        self.assertEqual(form.is_valid(), False)
