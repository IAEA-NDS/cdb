def read_requirements_lines(fi):
    req_list = []
    for line in fi.readlines():
        line = line.strip()
        if line:
            req_list.append(line)
    return req_list

def write_requirements_lines(req, fo):
    for line in req:
        print(line, file=fo)

with open('requirements-devel.txt') as fi:
    old_req_dev = read_requirements_lines(fi)
with open('requirements.txt') as fi:
    old_req = read_requirements_lines(fi)

devel_reqs = ['django-chunked-upload', 'django-debug-toolbar']

import subprocess
reqs = subprocess.run(['pip', 'freeze'],
                      stdout=subprocess.PIPE).stdout.decode('utf-8')
reqs = reqs.split('\n')
new_req_dev, new_req = [], []
for req in reqs:
    req = req.strip()
    if not req:
        continue
    name, version = req.split('==')
    if name in devel_reqs:
        new_req_dev.append(req)
    else:
        new_req.append(req)

with open('requirements-devel.txt', 'w') as fo:
    write_requirements_lines(new_req_dev, fo)
with open('requirements.txt', 'w') as fo:
    write_requirements_lines(new_req, fo)

def print_changes(new, old):
    changes = list(set(new) ^ set(old))
    for req in changes:
        print(req)

print('Changes in requirements-devel.txt:')
print_changes(new_req_dev, old_req_dev)
print('Changes in requirements.txt:')
print_changes(new_req, old_req)
