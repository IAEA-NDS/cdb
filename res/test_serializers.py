import os
import sys
from conf import www_cdb_path
sys.path.append(www_cdb_path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'cdb.settings'
# Prepare the Django models
import django
django.setup()

import io
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from cdbmeta.models import CDBRecord
from miniclerval.models import Institution, Person
from miniclerval.serializers import InstitutionSerializer, PersonSerializer

if False:
    p1 = Person.objects.get(pk=2)
    serializer = PersonSerializer(p1)
    print(serializer.data)
    content = JSONRenderer().render(serializer.data)
    print(content)


    stream = io.BytesIO(content)
    data = JSONParser().parse(stream)
    serializer = PersonSerializer(data=data)
    print(serializer.is_valid())
    print(serializer.errors)
    print(serializer.validated_data)

    sys.exit()

if True:
    s = b'{"qid":"C2", "institution":"I2"}'
    s = b'"C2"'
    stream = io.BytesIO(s)
    data = JSONParser().parse(stream)
    serializer = PersonSerializer(data=data)
    print(serializer)
    print(serializer.is_valid())
    print(serializer.errors)
    print(serializer.validated_data)

    content = JSONRenderer().render(serializer.data)
    stream = io.BytesIO(content)
    data = JSONParser().parse(stream)
    serializer = InstitutionSerializer(data=data)
    print(serializer.is_valid())
    print(serializer.validated_data)


if False:
    i1 = Institution.objects.get(pk=1)
    serializer = InstitutionSerializer(i1)
    print(serializer.data)
    content = JSONRenderer().render(serializer.data)
    print(content)


    stream = io.BytesIO(content)
    data = JSONParser().parse(stream)
    serializer = InstitutionSerializer(data=data)
    print(serializer.is_valid())
    print(serializer.validated_data)
