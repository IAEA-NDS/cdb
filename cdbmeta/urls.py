from django.conf.urls import url

from . import views

app_name = 'cdbmeta'
urlpatterns = [
    url(r'cdbrecord/(?P<cdbrecord_id>\d+)/$', views.cdbrecord,
                name='cdbrecord'),
    url(r'cdbrecord/xml/(?P<cdbrecord_id>\d+)/$', views.cdbrecord_xml,
                name='cdbrecord_xml'),
    url(r'cdbrecord/txt/(?P<cdbrecord_id>\d+)/$', views.cdbrecord_txt,
                name='cdbrecord_xml'),
    url(r'^$', views.cdb_search, name='cdb_search')
]
