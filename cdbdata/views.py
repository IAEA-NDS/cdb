from django.shortcuts import render

from django.views.generic.base import TemplateView

from chunked_upload.views import ChunkedUploadView, ChunkedUploadCompleteView

from .models import MyChunkedUpload
import os
from .templatetags.cdbdata_utils import filesize
from cdb.settings import MEDIA_ROOT, CHUNKED_UPLOAD_PATH
upload_dir = os.path.join(MEDIA_ROOT, CHUNKED_UPLOAD_PATH)


class ChunkedUploadDemo(TemplateView):
    template_name = 'cdbdata/chunked_upload.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        file_list = os.listdir(upload_dir)
        files_and_sizes = []
        for filename in file_list:
            files_and_sizes.append((filename, filesize(os.path.join(upload_dir,
                                                      filename))))
        context['file_list'] = files_and_sizes
        return context


class MyChunkedUploadView(ChunkedUploadView):

    model = MyChunkedUpload
    field_name = 'the_file'

    def check_permissions(self, request):
        # Allow non authenticated users to make uploads
        pass


class MyChunkedUploadCompleteView(ChunkedUploadCompleteView):

    model = MyChunkedUpload

    def check_permissions(self, request):
        # Allow non authenticated users to make uploads
        pass

    def on_completion(self, uploaded_file, request):
        # Do something with the uploaded file. E.g.:
        # * Store the uploaded file on another model:
        # SomeModel.objects.create(user=request.user, file=uploaded_file)
        # * Pass it as an argument to a function:
        # function_that_process_file(uploaded_file)
        pass

    def get_response_data(self, chunked_upload, request):
        return {'message': ("You successfully uploaded '%s' (%s bytes)!" %
(chunked_upload.filename, chunked_upload.offset))}
