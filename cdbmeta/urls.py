from django.urls import path, re_path
from django.views.generic import TemplateView

from . import views

app_name = 'cdbmeta'
urlpatterns = [
    re_path(r'cdbrecord/json/(?P<cdbrecord_id>\d+)/$', views.cdbrecord,
        {'fmt': 'json'}, name='json'),
    re_path(r'cdbrecord/xml/(?P<cdbrecord_id>\d+)/$', views.cdbrecord,
        {'fmt': 'xml'}, name='xml'),
    re_path(r'cdbrecord/txt/(?P<cdbrecord_id>\d+)/$', views.cdbrecord,
        {'fmt': 'txt'}, name='txt'),
    re_path(r'cdbrecord/(?P<cdbrecord_id>\d+)/$', views.cdbrecord,
        {'fmt': 'html'}, name='html'),
    path('manifest/', views.manifest, name='manifest'),
    path(r'doc', TemplateView.as_view(template_name='cdbmeta/doc.html'),
        name='documentation'),
    path(r'refs', views.refs, name='refs'),
    path(r'', views.cdb_search, name='cdb_search'),
    path(r'browse', views.cdb_browse, name='cdb_browse'),
]
