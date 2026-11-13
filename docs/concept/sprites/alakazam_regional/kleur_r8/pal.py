# palet + raster->png (index 0 = transparant)
import numpy as np, sys
from PIL import Image
PAL=[('.',(152,208,160)),('o',(16,14,22)),
 ('k',(34,32,46)),('m',(54,52,70)),('n',(88,86,112)),('p',(130,128,156)),   # zwart materiaal (k schaduw, m basis, n licht, p glans)
 ('w',(252,252,252)),('a',(224,224,232)),('b',(184,184,196)),('c',(146,140,170)),('d',(106,96,136)),  # wit / grijs (c,d violet in de schaduw)
 ('t',(248,112,104)),('r',(208,48,56)),('s',(128,24,40))]
CH={c:i for i,(c,_) in enumerate(PAL)}
RGB={c:v for c,v in PAL}
def load(fn): return [l.rstrip('\n').ljust(64,'.')[:64] for l in open(fn)][:64]
def topng(rows,fn):
    a=np.array([[CH[ch] for ch in r] for r in rows],'uint8')
    im=Image.fromarray(a,'P'); flat=[v for _,c in PAL for v in c]; im.putpalette(flat+[0]*(768-len(flat)))
    im.save(fn,transparency=0); return im
def rgb(rows,bg=(152,208,160)):
    a=np.array([[RGB[ch] if ch!='.' else bg for ch in r] for r in rows],'uint8'); return Image.fromarray(a)
if __name__=='__main__':
    im=topng(load(sys.argv[1]),sys.argv[2])
    if len(sys.argv)>3: rgb(load(sys.argv[1])).resize((512,512),Image.NEAREST).save(sys.argv[3])
