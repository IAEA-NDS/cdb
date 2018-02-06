from django.conf import settings
from django.conf.urls import url

from .views import (
    ChunkedUploadDemo, MyChunkedUploadView, MyChunkedUploadCompleteView
)


urlpatterns = [
    url(r'^$',
        ChunkedUploadDemo.as_view(), name='chunked_upload'),
    url(r'^api/chunked_upload/?$',
        MyChunkedUploadView.as_view(), name='api_chunked_upload'),
    url(r'^api/chunked_upload_complete/?$',
        MyChunkedUploadCompleteView.as_view(),
        name='api_chunked_upload_complete'),
    #url(r'^static/(.*)$',
    #    'django.views.static.serve',
    #    {'document_root': settings.STATIC_ROOT, 'show_indexes': False}),
]
