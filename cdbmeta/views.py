from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from collections import namedtuple

from .models import CDBRecord
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
    return render(request, 'cdbmeta/search.html', {'filter': cdbrecord_filter})
