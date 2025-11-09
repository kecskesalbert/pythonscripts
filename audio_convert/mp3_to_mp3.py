
import os,os.path,getopt,sys
curfilePath = os.path.abspath(__file__)
# this will return current directory in which python file resides.
curDir = os.path.abspath(os.path.join(curfilePath, os.pardir))
# this will return parent directory.
parentDir = os.path.abspath(os.path.join(curDir, os.pardir))


cliopts, blah = getopt.getopt(sys.argv[1:], '', \
    ["album=", "artist=", "year=", "title=", "comment="] \
)

files = os.listdir('.')
tracks = []
for file in files:
    if os.path.isfile(file):
        if file.endswith('.mp3'):
            tracks.append(file)

try:
    os.mkdir('out')
except OSError as error:
    if 1 < 0:
        print(error)

for track in tracks:
    cmd = 'ffmpeg'
    cmd += ' -i "%s"' % track
    cmd += ' -acodec copy'
    cmd += ' ' + ' '.join('-metadata %s="%s"' % (k[2:], v) for (k, v) in cliopts)
    cmd += ' -metadata title="%s"' % os.path.splitext(track)[0]
    cmd += ' "out/%s.mp3"' % os.path.splitext(track)[0]
    print(cmd)