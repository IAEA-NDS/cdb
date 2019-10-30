import sys
filename = sys.argv[1]
print(filename)

HEADERS_ONLY = False

if HEADERS_ONLY:
    with open(filename) as fi:
        first_line = fi.readline().rstrip()
        second_line = fi.readline().rstrip()
        outname = filename + '.xyz.header'
        with open(outname, 'w') as fo:
            print(first_line, file=fo)
            print(second_line, file=fo)
        sys.exit()


with open(filename) as fi:
    first_line = fi.readline().rstrip()
    for line in fi:
        line = line.rstrip()
        if 'Frame' in line:
            second_line = line
            this_frame = []
            continue
        this_frame.append(line)

header_name = filename + '.xyz.header'
with open(header_name, 'w') as fo:
    print(first_line, file=fo)
    print(second_line, file=fo)

outname = filename + '.xyz'
with open(outname, 'w') as fo:
    print(first_line, file=fo)
    print(second_line, file=fo)
    for line in this_frame:
        fields = line.split()
        print('{:>2}{:>13}{:>13}{:>13}'.format(*fields[:4]), file=fo)
