from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from collections import namedtuple
import os
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from cdb.settings import DATA_DIR
from .models import CDBRecord
from refs.models import Ref
from .filters import CDBRecordFilter

CDBOutputFormat = namedtuple('CDBOutputFormat', ('stylesheet', 'content_type'))
_output_formats = {
    'xml': CDBOutputFormat(None, 'text/xml'),
    'html': CDBOutputFormat('cdbml2html.xsl', 'text/xml'),
    'txt': CDBOutputFormat('cdbml2txt.xsl', 'text/xml'),
}

def cdbrecord(request, cdbrecord_id, fmt='html'):
    cdb_record = get_object_or_404(CDBRecord, pk=cdbrecord_id)
    xsl_name = _output_formats[fmt].stylesheet
    content_type = _output_formats[fmt].content_type
    return HttpResponse(cdb_record.as_cdbml(xsl_name=xsl_name),
                        content_type=content_type)

def cdb_search(request):
    cdbrecord_list = CDBRecord.objects.all()
    cdbrecord_filter = CDBRecordFilter(request.GET, queryset=cdbrecord_list)
    filtered_qs = cdbrecord_filter.qs
    paginator = Paginator(filtered_qs, 10)

    page = request.GET.get('page')
    try:
        response = paginator.page(page)
    except PageNotAnInteger:
        response = paginator.page(1)
    except EmptyPage:
        response = paginator.page(paginator.num_pages)

    c = {'filter': cdbrecord_filter, 'filtered_cdbrecords': response}
    return render(request, 'cdbmeta/search.html', c)

def refs(request):
    c = {'refs': Ref.objects.all()} 
    return render(request, 'cdbmeta/refs.html', c)

def manifest(request):
    filenames = os.listdir(DATA_DIR)
    filesizes = [(filename, os.path.getsize(os.path.join(DATA_DIR, filename)))
                    for filename in filenames]
    response = '\n'.join('{} {}'.format(*e) for e in filesizes)
    return HttpResponse(response, content_type='text/plain; charset=utf-8')
