import os
import sys

cdb_record_id = int(sys.argv[1])

cdb_path = '/Users/christian/www/cdb'
sys.path.append(cdb_path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'cdb.settings'

# Prepare the Django models
import django
django.setup()

from cdbmeta.models import CDBRecord

cdb_record = CDBRecord.objects.get(pk=cdb_record_id)
print(cdb_record.as_cdbml())
