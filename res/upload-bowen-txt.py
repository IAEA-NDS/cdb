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
                            CDBRecord, Person, LatticeParameters)

# XXX Huiqiu Deng's data XXX

s_dir, s_energy = sys.argv[1:]

root_dir = '/Users/christian/scratch/huiqiu'
dir_name = 'Dir_{}/{}kev'.format(s_dir, s_energy)
sim_dirs = glob.glob(os.path.join(root_dir, dir_name, 'Calc_*'))
nsim = len(sim_dirs)
print('nsim =', nsim)
assert nsim > 0

metadata_txt_filename = os.path.join(root_dir, dir_name, 'metadata.dat')
with open(metadata_txt_filename) as fi:
    lines = fi.readlines()
nlines = len(lines)
i = -1
while i < nlines-1:
    i += 1
    line = lines[i].strip()
    if not line:
        continue
    if line.startswith('CDB Record'):
        continue
    if line.startswith('===') or line.startswith('---'):
        continue
    if line.startswith('Attribution'):
        continue
    if line.startswith('Contributor:'):
        acknowledgements = line.replace('Contributor', 'Contributors') + '\n'
        continue
    if line.startswith('Acknowledgements'):
        i += 1
        while not lines[i].startswith('Material'):
            if lines[i].startswith('---'):
                i += 1
                continue
            acknowledgements += lines[i] + '\n'
            i += 1
        continue
    if line.startswith('Formula'):
        chemical_formula = line.split(':')[1].strip()
        continue
    if line.startswith('Structure'):
        structure = line.split(':')[1].strip()
        continue

    if line.startswith('Lattice Parameters'):
        i += 1
        a = float(lines[i].split('=')[1].strip('\n Å,.'))
        i += 1
        b = float(lines[i].split('=')[1].strip('\n Å,.'))
        i += 1
        c = float(lines[i].split('=')[1].strip('\n Å,.'))
        i += 1
        alpha = float(lines[i].split('=')[1].strip('\n °,.'))
        i += 1
        beta = float(lines[i].split('=')[1].strip('\n °,.'))
        i += 1
        gamma = float(lines[i].split('=')[1].strip('\n °,.'))
        continue

    if line.startswith('Simulation includes surface'):
        has_surface = line.split('?')[1].strip()
        assert has_surface in ('true', 'false')
        has_surface = has_surface == 'true'
        continue

    if line.startswith('Initially perfect crystal configuration'):
        initially_perfect = line.split('?')[1].strip()
        assert initially_perfect in ('true', 'false')
        initially_perfect = initially_perfect == 'true'
        continue

    if line == 'PKA':
        continue

    if line.startswith('PKA direction'):
        comments = line
        continue

    if line.startswith('PKA atomic number'):
        if chemical_formula == 'W':
            atomic_number = 74
            continue
        else:
            print("I don't know what to do about PKA atomic number!")
            sys.exit(1)
    if line.startswith('PKA energy'):
        energy = line.split(':')[1].strip()
        assert energy[-3:] == 'keV'
        energy = float(energy[:-3])
        assert int(energy) == int(s_energy)
        continue

    if line.startswith('PKA by recoil'):
        recoil = line.split('?')[1].strip()
        assert recoil in ('true', 'false')
        recoil = recoil == 'true'
        continue

    if line == 'Simulation Details':
        continue

    if line.startswith('Electronic stopping included'):
        electronic_stopping = line.split('?')[1].strip()
        assert electronic_stopping in ('true', 'false')
        electronic_stopping = electronic_stopping == 'true'
        assert electronic_stopping is False
        continue

    if line.startswith('Thermostat comments'):
        thermostat_comment = line.split(':')[1].strip()
        continue

    if line.startswith('Thermostat'):
        thermostat = line.split('?')[1].strip()
        assert thermostat in ('true', 'false')
        thermostat = thermostat == 'true'
        continue

    if line.startswith('Input filename'):
        continue
    input_filename = 'lammpsinput.in'

    if line.startswith('Simulation time'):
        total_simulation_time = line.split(':')[1].strip()
        assert total_simulation_time[-2:] == 'ps'
        total_simulation_time = float(total_simulation_time[:-2])
        continue

    if line.startswith('Initial temperature'):
        initial_temperature = line.split(':')[1].strip()
        assert initial_temperature[-1] == 'K'
        initial_temperature = float(initial_temperature[:-1])
        continue

    if line.startswith('Box dimensions (Å)'):
        xyz = line.split(':')[1].strip()
        box_X, box_Y, box_Z = [float(e) for e in xyz.split(',')]
        continue

    if line.startswith('Box orientation'):
        orientation = line.split(':')[1].strip()
        box_X_orientation, box_Y_orientation, box_Z_orientation = (
                orientation.split(', ') )
        continue

    if line.startswith('Interatomic potential URI'):
        continue

    if line.startswith('Interatomic potential doi'):
        pot_doi = line.split(':')[1].strip()
        assert pot_doi == '10.1016/j.jnucmat.2018.01.059'
        continue

    if line.startswith('Interatomic potential comment'):
        pot_comment = line.split(': ')[1].strip()
        assert pot_comment == 'https://doi.org/10.1016/j.jnucmat.2018.01.059'
        continue

    if line.startswith('Interatomic potential filename'):
        potential_filename = line.split(':')[1].strip()
        assert potential_filename == 'WRe_YC1.eam.fs'
        continue

    if line.startswith('Code'):
        code_name = line.split(':')[1].strip()
        assert code_name == 'LAMMPS'
        code_version = 'Mar 31, 2017'
        continue

    if line == 'Data':
        continue

    if line.startswith('Data archive name'):
        archive_name = line.split(':')[1].strip()
        assert initial_temperature == float(archive_name.split('K')[0])
        archive_name += '.tar.bz2'
        continue

    if line == 'Columns':
        continue
    if line in ('Position | Name | Units', '1 | Element Symbol |',
        '2 | x | Å', '3 | y | Å', '4 | z | Å'):
        continue

    if line == 'Comments':
        continue
    if line == 'This data set is provided as part of *******.':
        continue

    print('I failed to parse the line:')
    print(line)
    sys.exit(1)

# Huiqiu Deng
#person = Person.objects.get(pk=10)
attribution = Attribution.objects.get(pk=15)

lattice_parameters = LatticeParameters.objects.get(a=a, b=b, c=c, alpha=alpha,
                                beta=beta, gamma=gamma)
material = Material.objects.get(chemical_formula=chemical_formula,
            structure=structure, lattice_parameters=lattice_parameters)

potential = Potential.objects.get(pk=16)

#cdbrecord = CDBRecord(
cdbrecord = CDBRecord.objects.get_or_create(
    attribution = attribution,
    material = material,
    has_surface = has_surface,
    initially_perfect = initially_perfect,
    atomic_number = atomic_number,
    energy = energy,
    recoil = recoil,
    electronic_stopping = electronic_stopping,
    thermostat = thermostat,
    thermostat_comment = thermostat_comment,
    input_filename = input_filename,
    total_simulation_time = total_simulation_time,
    initial_temperature = initial_temperature,
    box_X = box_X,
    box_Y = box_Y,
    box_Z = box_Z,
    box_X_orientation = box_X_orientation,
    box_Y_orientation = box_Y_orientation,
    box_Z_orientation = box_Z_orientation,
    potential = potential,
    code_name = code_name,
    code_version = code_version,
    archive_name = archive_name,
    nsim = nsim
)

