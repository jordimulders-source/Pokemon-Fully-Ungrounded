# palet + raster->png (index 0 = transparant)
import numpy as np, sys, os
from PIL import Image
PAL=[('.',(152,208,160)),('o',(20,18,28)),
 ('w',(252,252,252)),('a',(228,228,236)),('b',(196,196,208)),('c',(156,154,174)),('d',(116,108,146)),('e',(78,70,104)),
 ('k',(34,32,46)),('m',(54,52,72)),('n',(84,82,108)),('p',(126,124,152)),
 ('t',(248,112,104)),('r',(208,48,56)),('s',(128,24,40))]
CH={c:i for i,(c,_) in enumerate(PAL)}
def load(fn): return [l.rstrip('\n') for l in open(fn)][:64]
def topng(rows,fn):
    a=np.array([[CH[ch] for ch in r.ljust(64,'.')[:64]] for r in rows],'uint8')
    im=Image.fromarray(a,'P'); flat=[v for _,c in PAL for v in c]; im.putpalette(flat+[0]*(768-len(flat)))
    im.info['transparency']=0; im.save(fn,transparency=0); return im
if __name__=='__main__':
    im=topng(load(sys.argv[1]),sys.argv[2])
    if len(sys.argv)>3: im.convert('RGB').resize((512,512),Image.NEAREST).save(sys.argv[3])
