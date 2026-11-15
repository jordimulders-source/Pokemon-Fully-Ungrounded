# Hulp: rasters/png's naast elkaar renderen. gebruik: toon.py uit.png schaal [y0 y1 x0 x1] bestand...
import sys
from gemeen import *
from pal import PAL,CH
def laad(f):
    if f.endswith('.txt'):
        rows=[l.rstrip('\n') for l in open(f)][:64]
        a=np.array([[PAL[CH.index(c)] for c in r] for r in rows],np.uint8)
        a[np.array([[c=='.' for c in r] for r in rows])]=255; return a
    im=Image.open(f).convert('RGBA'); bg=Image.new('RGBA',im.size,(255,255,255,255)); bg.alpha_composite(im)
    return np.asarray(bg.convert('RGB'))
if __name__=="__main__":
    out=sys.argv[1]; s=int(sys.argv[2]); rest=sys.argv[3:]
    box=None
    if rest[0].lstrip('-').isdigit(): box=list(map(int,rest[:4])); rest=rest[4:]
    ims=[]
    for f in rest:
        a=laad(f)
        if box: a=a[box[0]:box[1],box[2]:box[3]]
        ims.append(a); ims.append(np.full((a.shape[0],1,3),255,np.uint8))
    row=np.concatenate(ims[:-1],1)
    Image.fromarray(row).resize((row.shape[1]*s,row.shape[0]*s),Image.NEAREST).save(out)
