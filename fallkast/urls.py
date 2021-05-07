from django.conf import settings
from django.urls import path, re_path

from .views import upload_home, upload

app_name = 'fallkast'
urlpatterns = [
    path('', upload_home, name='upload_home'),
    path('upload', upload, name='upload'),
]

