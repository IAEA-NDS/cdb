from django.conf.urls import url

from . import views

app_name = 'refs'
urlpatterns = [
    url(r'^bibtex/(?P<pk>\d+)/$', views.bibtex, name='bibtex'),
]
