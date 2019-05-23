from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from .models import Ref

def bibtex(request, pk):
    ref = get_object_or_404(Ref, pk=pk)
    if not ref.bibtex:
        raise Http404
    return HttpResponse(ref.bibtex, content_type='text/plain')
