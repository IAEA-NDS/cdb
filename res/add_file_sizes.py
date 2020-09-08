# add_file_sizes.py
import os
import sys
import urllib.request
from conf import www_cdb_path
sys.path.append(www_cdb_path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'cdb.settings'
# Prepare the Django models
import django
django.setup()

from cdbmeta.models import CDBRecord

dry_run = False

cdbrecords = CDBRecord.objects.all()
filenames = cdbrecords.values_list('archive_name', flat=True)

import urllib.request
req = urllib.request.Request('https://cascadesdb.org/cdbmeta/manifest/')
response = urllib.request.urlopen(req)
content = response.read()

charset = response.headers.get_content_charset()
#charset = 'utf-8'
manifest = content.decode(charset)
manifest = dict(line.split() for line in manifest.split('\n'))
non_matching = set(filenames).difference(manifest.keys())
if non_matching:
    print('Non-matching filenames:', non_matching)
    sys.exit(1)

for cdbrecord in cdbrecords:
    filename = cdbrecord.archive_name
    filesize = manifest[filename]
    print(filename, ':', filesize)
    if not dry_run:
        cdbrecord.archive_filesize = filesize
        cdbrecord.save()

#for filename in filenames:
#    print(filename)

