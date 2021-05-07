from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.core.files.storage import FileSystemStorage
from django.conf import settings

def is_allowed_to_upload(u):
    return u.groups.filter(name='data-provider').exists() or u.is_superuser

@user_passes_test(is_allowed_to_upload)
def upload_home(request):
    return render(request, 'fallkast/upload-index.html', {})

@user_passes_test(is_allowed_to_upload)
def upload(request):
    if request.method == 'POST' and request.FILES['uploaded_file']:
        uploaded_file = request.FILES['uploaded_file']
        fs = FileSystemStorage(location=settings.UPLOAD_DIR)
        filename = fs.save(uploaded_file.name, uploaded_file)
        uploaded_file_url = fs.url(filename)
        return render(request, 'fallkast/upload.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'fallkast/upload.html', {})
