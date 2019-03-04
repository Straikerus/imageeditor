from django.conf.urls import url
from .views import ImagesListView, UploadView, ImageView


urlpatterns = [
    url('^$', ImagesListView.as_view(), name='images-list'),
    url('^upload/$', UploadView.as_view(), name='image-upload'),
    url('^(?P<pk>\d+)/$', ImageView.as_view(), name='image')
]
