from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

app_name = 'cdbmeta'
urlpatterns = [
    url(r'cdbrecord/xml/(?P<cdbrecord_id>\d+)/$', views.cdbrecord,
        {'fmt': 'xml'}, name='xml'),
    url(r'cdbrecord/txt/(?P<cdbrecord_id>\d+)/$', views.cdbrecord,
        {'fmt': 'txt'}, name='txt'),
    url(r'cdbrecord/(?P<cdbrecord_id>\d+)/$', views.cdbrecord,
        {'fmt': 'html'}, name='html'),
    url(r'manifest/$', views.manifest, name='manifest'),
    url(r'^doc$', TemplateView.as_view(template_name='cdbmeta/doc.html')),
    url(r'^$', views.cdb_search, name='cdb_search')
]
