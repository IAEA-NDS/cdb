from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'cdbrecord/(?P<cdbrecord_id>\d+)/$', views.cdbrecord,
                name='cdbrecord'),
    url(r'cdbrecord/xml/(?P<cdbrecord_id>\d+)/$', views.cdbrecord_xml,
                name='cdbrecord_xml'),
]
