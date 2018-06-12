from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from .models import CDBRecord
from .filters import CDBRecordFilter

def cdbrecord_xml(request, cdbrecord_id, xsl_name=None):
    cdb_record = get_object_or_404(CDBRecord, pk=cdbrecord_id)
    return HttpResponse(cdb_record.as_cdbml(xsl_name=xsl_name),
                        content_type='text/xml')

def cdbrecord(request, cdbrecord_id):
    return cdbrecord_xml(request, cdbrecord_id, xsl_name='cdbml2html.xsl')

def cdbrecord_txt(request, cdbrecord_id):
    return cdbrecord_xml(request, cdbrecord_id, xsl_name='cdbml2txt.xsl')

def cdb_search(request):
    cdbrecord_list = CDBRecord.objects.all()
    cdbrecord_filter = CDBRecordFilter(request.GET, queryset=cdbrecord_list)
    return render(request, 'cdbmeta/search.html', {'filter': cdbrecord_filter})
