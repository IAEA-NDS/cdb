from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from .models import CDBRecord

def cdbrecord_xml(request, cdbrecord_id, xml2html=False):
    cdb_record = get_object_or_404(CDBRecord, pk=cdbrecord_id)
    return HttpResponse(cdb_record.as_cdbml(xml2html=xml2html),
                        content_type='text/xml')

def cdbrecord(request, cdbrecord_id):
    return cdbrecord_xml(request, cdbrecord_id, xml2html=True)
