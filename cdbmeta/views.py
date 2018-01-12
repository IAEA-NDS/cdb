from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from .models import CDBRecord

# Create your views here.
def cdbrecord_xml(request, cdbrecord_id):
    cdb_record = get_object_or_404(CDBRecord, pk=cdbrecord_id)
    return HttpResponse(cdb_record.as_cdbml(), content_type='text/xml')
