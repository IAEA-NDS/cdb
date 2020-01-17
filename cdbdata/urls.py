from django.conf import settings
from django.urls import path, re_path

from .views import (upload_home,
    ChunkedUploadDemo, MyChunkedUploadView, MyChunkedUploadCompleteView
)


urlpatterns = [
    path(r'', upload_home, name='upload_home'),
    path(r'upload/',
        ChunkedUploadDemo.as_view(), name='chunked_upload'),
    re_path(r'^api/chunked_upload/?$',
        MyChunkedUploadView.as_view(), name='api_chunked_upload'),
    re_path(r'^api/chunked_upload_complete/?$',
        MyChunkedUploadCompleteView.as_view(),
        name='api_chunked_upload_complete'),
    #re_path(r'^static/(.*)$',
    #    'django.views.static.serve',
    #    {'document_root': settings.STATIC_ROOT, 'show_indexes': False}),
]
