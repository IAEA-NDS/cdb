import os
import sys
import urllib.request
from conf import www_cdb_path
sys.path.append(www_cdb_path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'cdb.settings'
# Prepare the Django models
import django
django.setup()

attribution_pk = 5
material_pk = 1
potential_pk = 1
atomic_number = 74

dry_run = False


from cdbmeta.models import CDBRecord
from cdbmeta.models import Attribution, Material, Potential


max_pk = CDBRecord.objects.all().order_by('-id')[0].id + 1
archive_stem = '{:03x}-w-'.format(max_pk)


attribution = Attribution.objects.get(pk=attribution_pk)
material = Material.objects.get(pk=material_pk)
potential = Potential.objects.get(pk=potential_pk)

import glob
E = sys.argv[1]

archive_name = archive_stem + E + '.tar.gz'
print(archive_name)

filenames = glob.glob('./md.movie-' + str(E) + '-*.xyz.header')
times = []
dim = set()
for filename in filenames:
    print(filename)
    with open(filename) as fi:
        print(fi.readline().rstrip())
        line = fi.readline().rstrip()
        print(line)
    fields = line.split()
    times.append(float(fields[3]))
    box_X, box_Y, box_Z = fields[-3:]
    dim.add((box_X, box_Y, box_Z))

nsim = len(times)
time = sum(times)/nsim/1000
time = round(time)
print(time)
print(box_X, box_Y, box_Z, len(dim))
print(E)

cdbrecord = CDBRecord(
    attribution=attribution,
    material=material,
    has_surface=False,
    initially_perfect=True,
    atomic_number=atomic_number,
    energy=float(E),
    recoil=True,
    electronic_stopping=True,
    electronic_stopping_comment="for all atoms with K.E. > 10 eV; see publication",
    thermostat=True,
    thermostat_comment="on borders, 0 Kelvin; see publication",
    total_simulation_time=time,
    initial_temperature=0,
    box_X=box_X, box_Y=box_Y, box_Z=box_Z,
    box_X_orientation='100', box_Y_orientation='010', box_Z_orientation='001',
    potential=potential,
    code_name='PARCAS', code_version='5.02b',
    archive_name=archive_name,
    nsim=nsim)

if not dry_run:
    cdbrecord.save()
