from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.db.models import Sum

from collections import namedtuple
import os
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from cdb.settings import DATA_DIR, POTENTIAL_URL
from .models import CDBRecord, Material, Attribution, Potential
from miniclerval.models import Person
from refs.models import Ref
from .filters import CDBRecordFilter

# Rough compression factor for data archives
APPROX_COMPRESSION_RATIO = 5

CDBOutputFormat = namedtuple('CDBOutputFormat', ('stylesheet', 'content_type'))
_output_formats = {
    'xml': CDBOutputFormat(None, 'text/xml'),
    'html': CDBOutputFormat('cdbml2html.xsl', 'text/xml'),
    'txt': CDBOutputFormat('cdbml2txt.xsl', 'text/xml'),
    'json': CDBOutputFormat(None, 'application/json'),
}

def home(request):
    total_size = CDBRecord.objects.aggregate(Sum('archive_filesize')
                        )['archive_filesize__sum'] * APPROX_COMPRESSION_RATIO
    total_size = int(round(total_size / 1024 / 1024 / 1024))
    narchives = CDBRecord.objects.all().count()
    nsims = CDBRecord.objects.aggregate(Sum('nsim'))['nsim__sum']
    c = {'total_size': '{} GB'.format(total_size),
         'narchives': narchives, 'total_sims': nsims}
    return render(request, 'cdbmeta/index.html', c)

def cdbrecord(request, cdbrecord_id, fmt='html'):
    cdb_record = get_object_or_404(CDBRecord, pk=cdbrecord_id)
    xsl_name = _output_formats[fmt].stylesheet
    content_type = _output_formats[fmt].content_type
    if fmt == 'json':
        output_record = cdb_record.as_json()
    else:
        output_record = cdb_record.as_cdbml(xsl_name=xsl_name)
    
    return HttpResponse(output_record, content_type=content_type)

def cdb_search(request):
    cdbrecord_list = CDBRecord.objects.all()
    cdbrecord_filter = CDBRecordFilter(request.GET, queryset=cdbrecord_list)
    filtered_qs = sorted(cdbrecord_filter.qs,
                         key=lambda objects: objects.attribution.person.name)

    paginator = Paginator(filtered_qs, 10)

    c = {}
    if request.GET:
        page = request.GET.get('page')
        try:
            response = paginator.page(page)
        except PageNotAnInteger:
            response = paginator.page(1)
        except EmptyPage:
            response = paginator.page(paginator.num_pages)

        querydict = request.GET.copy()
        try:
            del querydict['page']
        except KeyError:
            pass
        c['querystring'] = '&' + querydict.urlencode()
    else:
        response = None

    c.update({'filter': cdbrecord_filter, 'filtered_cdbrecords': response})
    return render(request, 'cdbmeta/search.html', c)

def cdb_browse(request):
    c = {}
    c['refs'] = Ref.objects.filter(pk__in=Attribution.objects.all()
                                   .values('source').distinct())
    c['materials'] = Material.objects.values('chemical_formula').distinct()

    people = Person.objects.filter(pk__in=Attribution.objects.all()
                                   .values('person').distinct())
    people = list(people)
    people.sort(key=lambda e: e.surname)
    c['people'] = people

    c['potentials'] = Potential.objects.all()

    return render(request, 'cdbmeta/browse.html', c)


def refs(request):
    c = {'refs': Ref.objects.all()} 
    return render(request, 'cdbmeta/refs.html', c)

def manifest(request):
    filenames = os.listdir(DATA_DIR)
    filesizes = [(filename, os.path.getsize(os.path.join(DATA_DIR, filename)))
                    for filename in filenames]
    response = '\n'.join('{} {}'.format(*e) for e in filesizes)
    return HttpResponse(response, content_type='text/plain; charset=utf-8')

def potential(request, potential_id):
    potential = get_object_or_404(Potential, pk=potential_id)
    c = {'potential': potential, 'POTENTIAL_URL': POTENTIAL_URL}
    return render(request, 'cdbmeta/potential.html', c)
