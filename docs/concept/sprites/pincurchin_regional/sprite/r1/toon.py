# npy -> png (geïndexeerd) + 8x op wit; palet hier vast
import numpy as np,sys
from PIL import Image
PAL=[(255,0,255),(16,16,16),(50,36,30),(80,63,55),(110,91,79),(140,116,104),(95,26,28),(140,33,37),(200,65,70),
     (248,240,40),(248,184,40),(72,56,72),(40,32,48),(120,72,24),(208,136,16)]
def save(o,uit):
    p=Image.fromarray((o+1).astype('uint8'),'P'); f=[v for c in PAL for v in c]; p.putpalette(f+[0]*(768-len(f))); p.save(uit,transparency=0)
    q=Image.open(uit).convert('RGBA'); b=Image.new('RGBA',q.size,(255,255,255,255)); b.alpha_composite(q); b.resize((512,512),Image.NEAREST).save(uit.replace('.png','_8x.png'))
if __name__=='__main__': save(np.load(sys.argv[1]),sys.argv[2])
