import os
import sys
import glob
import json
from conf import www_cdb_path
sys.path.append(www_cdb_path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'cdb.settings'
# Prepare the Django models
import django
django.setup()

from cdbmeta.models import (Attribution, Material, Potential, DataColumn,
                            CDBRecord)

# XXX Aslak Fellman's data XXX

attribution = Attribution.objects.get(pk=14)
material = Material.objects.get(pk=1)
potential = Potential.objects.get(pk=15)

adc_atom_identifier = DataColumn.objects.get(pk=8)
adc_atom_index = DataColumn.objects.get(pk=6)
adc_pe = DataColumn.objects.get(pk=2)
adc_ke = DataColumn.objects.get(pk=7)

#json_file = '/Users/christian/scratch/afellman/json/0b5-ATZN-void-1-4-15.json'

def read_json(json_file):
    with open(json_file) as fi:
        jd = json.loads(fi.read())
    return jd

json_files = glob.glob('/Users/christian/scratch/afellman/json/*.json')
for i, json_file in enumerate(json_files[1:]):
    print(json_file)
    jd = read_json(json_file)

    # fs -> ps
    jd['simulation-time'] /= 1000

    cdbrecord = CDBRecord(
        attribution = attribution,
        material = material,
        has_surface = jd['has-surface'],
        initially_perfect = jd['initially-perfect'],
        atomic_number = jd['PKA-atomic-number'],
        energy = jd['PKA-energy'],
        recoil = jd['recoil'],
        electronic_stopping = jd['electronic-stopping'],
        electronic_stopping_comment = jd['electronic-stopping-comment'],
        thermostat = jd['thermostat'],
        thermostat_comment = jd['thermostat-comment'],
        input_filename = jd['input-filename'],
        total_simulation_time = jd['simulation-time'],
        initial_temperature = jd['initial-temperature'],
        box_X = jd['simulation-box']['box-x-length'],
        box_Y = jd['simulation-box']['box-y-length'],
        box_Z = jd['simulation-box']['box-z-length'],
        box_X_orientation = jd['simulation-box']['box-X-orientation'],
        box_Y_orientation = jd['simulation-box']['box-Y-orientation'],
        box_Z_orientation = jd['simulation-box']['box-Z-orientation'],
        potential = potential,
        code_name = jd['code']['name'],
        code_version = jd['code']['version'],
        archive_name = jd['archive-name'],
        archive_filesize = jd['archive-filesize'],
        nsim = jd['number-of-simulations'],
        initial_configuration_filename = jd['initial-configuration-filename'],
        initial_configuration_comments = jd['initial-configuration-comments'],
    )

    cdbrecord.save()
    cdbrecord.additional_columns.add(adc_atom_identifier)
    cdbrecord.additional_columns.add(adc_atom_index)
    cdbrecord.additional_columns.add(adc_pe)
    cdbrecord.additional_columns.add(adc_ke)
