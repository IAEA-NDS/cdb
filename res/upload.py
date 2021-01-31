import os
import sys
import hashlib
import subprocess
import fnmatch
from datetime import datetime
import tarfile
import argparse
from conf import www_cdb_path, TRANSFER_DIR
webapp_path = www_cdb_path
sys.path.append(webapp_path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'cdb.settings'


N = 1
cdb_archive_name = os.path.join(TRANSFER_DIR, 'cdb-{}.tar'.format(N))



parser = argparse.ArgumentParser(description='Upload CascadesDB website and'
                                             ' database.')
parser.add_argument('mtime', help='Upload all files more recent than mtime.',
    default=None)
parser.add_argument('-b', '--backup-only', dest='backup_only',
    help='Don\'t upload: only dump MySQL database.',
    default=False, action='store_true')
parser.add_argument('-u', '--upload-only', dest='upload_only',
    help='Only upload MySQL database dump.',
    default=False, action='store_true')
parser.add_argument('-d', '--destination', dest='destination', nargs='?',
                    default='enc')

args = parser.parse_args()

if args.destination == 'enc':
    TRANSFER_DESTINATION = 'ubuntu@ec2-18-220-219-221.us-east-2.compute.amazonaws.com:/srv/www/cdb_static/zipu8634q9t18yqehgj/'
    SSH_PRIVATE_KEY = '/Users/christian/.ssh/cdb.pem'
else:
    print('Allowed destination is "enc" only.')
    print('Instead, I got:', args.destination)
    sys.exit(1)

def usage():
    print('Usage is:\n{} [mtime]'.format(sys.argv[0]))
    print('where [mtime] is the optional modification time: update only files')
    print('which are new or modified since the time YYYYMMDD[HHMM]')

mtime = args.mtime
if mtime is None:
    print('Updating all')
elif len(mtime) == 12:
    mtime = datetime.strptime(mtime, '%Y%m%d%H%M')
elif len(mtime) == 8:
    mtime = datetime.strptime(mtime, '%Y%m%d')
else:
    usage()
    sys.exit(1)

if mtime:
    print('Updating all since', mtime)
    # For comparison with tarinfo.mtime, we need mtime as "number of seconds
    # since the epoch".
    mtime = mtime.timestamp()

print('mtime =', mtime)
print('destination =', args.destination)
print('backup_only =', args.backup_only)
print('upload_only =', args.upload_only)

# Prepare the Django models
import django
django.setup()

from cdb.settings import DATABASES

def upload_transfer_files():
    print('Uploading files to destination', args.destination, '...')
    if args.destination == 'enc':
        f = cdb_archive_name + '.enc'
        cmd = ['scp', os.path.join(TRANSFER_DIR, f), TRANSFER_DESTINATION]
        if SSH_PRIVATE_KEY:
            cmd.insert(1, '-i{}'.format(SSH_PRIVATE_KEY))
        subprocess.run(cmd)

        f = cdb_archive_name + '.md5'
        cmd = ['scp', os.path.join(TRANSFER_DIR, f), TRANSFER_DESTINATION]
        if SSH_PRIVATE_KEY:
            cmd.insert(1, '-i{}'.format(SSH_PRIVATE_KEY))
        subprocess.run(cmd)
        

def make_encrypted_archive():
    with tarfile.open(cdb_archive_name, mode='w') as archive:
        for f in ('cdb.mysql',):
            fp = os.path.join(TRANSFER_DIR, f)
            if not os.path.exists(fp):
                print(fp, 'not found.')
                sys.exit(1)
            archive.add(fp, arcname=f)

    keyfile = os.path.join(TRANSFER_DIR, 'key.bin')
    cmd = ['openssl', 'enc', '-aes-256-cbc', '-pbkdf2', '-iter', '20000',
           '-in', cdb_archive_name,
           '-out', '{}.enc'.format(cdb_archive_name),
           '-pass', 'file:{}'.format(keyfile)]
    print(' '.join(cmd))
    subprocess.call(cmd)


def make_md5_hash_of_encrypted_archive():
    def _file_as_bytes(fi):                                                        
        with fi:                                                                  
            return fi.read()
    f = os.path.join(TRANSFER_DIR, cdb_archive_name + '.enc')
    md5 = hashlib.md5(_file_as_bytes(open(f, 'rb'))).hexdigest()
    f = os.path.join(TRANSFER_DIR, cdb_archive_name + '.md5')
    with open(f, 'w') as fo:
        print(md5, file=fo)

                        
if not args.upload_only:
    ### Dump the database ###
    cmd = ['mysqldump',
           '-u{}'.format(DATABASES['default']['USER']),
           '-p{}'.format( DATABASES['default']['PASSWORD']),
           'cdb'
          ]
    dumpname = 'cdb.mysql'
    print(dumpname)
    with open(os.path.join(TRANSFER_DIR, dumpname), 'w') as fo:
        subprocess.run(cmd, stdout=fo)

    if args.destination == 'enc':
        make_encrypted_archive()
        make_md5_hash_of_encrypted_archive()

if not args.backup_only:
    upload_transfer_files()
