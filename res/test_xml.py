import os
import sys

cdb_path = '/Users/christian/www/cdb'
sys.path.append(cdb_path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'cdb.settings'

# Prepare the Django models
import django
django.setup()

from cdbmeta.models import CDBRecord

cdb_record = CDBRecord.objects.get(pk=2)
print(cdb_record.as_cdbml())
