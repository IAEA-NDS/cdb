import sys
filename = sys.argv[1]

HEADERS_ONLY = False

print(filename)
with open(filename) as fi:
    first_line = fi.readline().rstrip()
    for line in fi:
        line = line.rstrip()
        if 'Frame' in line:
            second_line = line
            this_frame = []
            continue
        this_frame.append(line)

outname = filename + '.xyz'
if HEADERS_ONLY:
    outname += '.header'
with open(outname, 'w') as fo:
    print(first_line, file=fo)
    print(second_line, file=fo)
    if not HEADERS_ONLY:
        for line in this_frame:
            fields = line.split()
            print('{:>2}{:>13}{:>13}{:>13}'.format(*fields[:4]), file=fo)
