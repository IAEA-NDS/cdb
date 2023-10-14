from django.urls import re_path

from . import views

app_name = 'refs'
urlpatterns = [
    re_path(r'^bibtex/(?P<pk>\d+)/$', views.bibtex, name='bibtex'),
]
