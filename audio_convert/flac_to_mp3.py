# -*- coding: utf-8 -*-
import os,os.path,getopt,sys
curfilePath = os.path.abspath(__file__)
# this will return current directory in which python file resides.
curDir = os.path.abspath(os.path.join(curfilePath, os.pardir))
# this will return parent directory.
parentDir = os.path.abspath(os.path.join(curDir, os.pardir))

def uprint(*objects, sep=' ', end='\n', file=sys.stdout):
    enc = file.encoding
    if enc == 'UTF-8':
        print(*objects, sep=sep, end=end, file=file)
    else:
        f = lambda obj: str(obj).encode(enc, errors='backslashreplace').decode(enc)
        print(*map(f, objects), sep=sep, end=end, file=file)

cliopts, blah = getopt.getopt(sys.argv[1:], '', \
    ["album=", "artist=", "year=", "title=", "comment="] \
)

files = os.listdir('.')
tracks = []
for file in files:
    if os.path.isfile(file):
        if file.endswith('.flac') or file.endswith('.wav'):
            # tracks.append(file.encode("utf-8"))
            tracks.append(file)

for track in tracks:
    cmd = 'ffmpeg'
    cmd += ' -i "%s"' % track
    cmd += ' -q:a 1'
    cmd += ' ' + ' '.join('-metadata %s="%s"' % (k[2:], v) for (k, v) in cliopts)
    cmd += ' -metadata title="%s"' % os.path.splitext(track)[0]
    cmd += ' "%s.mp3"' % os.path.splitext(track)[0]
    uprint(cmd)