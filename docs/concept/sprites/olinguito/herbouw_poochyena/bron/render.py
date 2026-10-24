# Leest raster_f1.txt (64x64, tekens 0-f, '.'=transparant) en maakt een PNG op schaal.
import sys
from PIL import Image
PAL=None
def loadpal(p):
    global PAL
    PAL=[tuple(map(int,l.split())) for l in open(p).read().split('\n')[3:19]]
def load(p):
    rows=[l.rstrip('\n') for l in open(p)]
    rows=[r.ljust(64,'.')[:64] for r in rows][:64]
    while len(rows)<64: rows.append('.'*64)
    return rows
def toimg(rows):
    im=Image.new('P',(64,64),0); im.putpalette([c for t in PAL for c in t])
    for y,r in enumerate(rows):
        for x,ch in enumerate(r):
            if ch!='.': im.putpixel((x,y),int(ch,16))
    return im
if __name__=='__main__':
    loadpal(sys.argv[1])
    rows=load(sys.argv[2]); im=toimg(rows); sc=int(sys.argv[4]) if len(sys.argv)>4 else 8
    im.convert('RGB').resize((64*sc,64*sc),Image.NEAREST).save(sys.argv[3])
