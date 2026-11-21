# r3: alleen het oog, pixel voor pixel uit Rufflet (Gen 5, frame 1) overgenomen in ons grijze masker.
# Rufflet-index -> ons palet: 4 wit->W, 2 zwart->K, 1 blauwgrijs masker->b, B donkerblauw->n, A blauw donker->a, 7 schaduwcreme->w
# Rufflets nabije oog: x30-33, rijen 26-30 (64x64-frame). Ons oog (model natief x41-46,y26-33) = sprite x11-14, rijen 10/11-14.
import numpy as np; from PIL import Image; from pal import *
R=np.asarray(Image.open('../referenties/rufflet_anim_front.png'))[:64]
M={4:'W',2:'K',1:'b',11:'n',10:'a',7:'w'}
def ruf(y0,y1,x0,x1): return np.vectorize(lambda v:M[int(v)])(R[y0:y1,x0:x1])
base=lees('rufflet_r2.txt'); ZONE=(slice(10,15),slice(11,15))
var={}
A=base.copy(); A[11:15,11:15]=ruf(27,31,30,34); var['A']=A                    # 4x4: Rufflet rijen 27-30 (zonder bovenste witte rij)
B=base.copy(); B[10:15,11:15]=ruf(26,31,30,34); var['B']=B                    # 4x5: het hele Rufflet-oog, ook de witte bovenrij
C=base.copy(); C[12:15,11:15]=ruf(28,31,30,34); C[11,11:15]=base[11,11:15]    # Rufflet rijen 28-30 onder de zwarte modelbovenlijn van r2 (rij 11)
C[11,11]='K'
var['C']=C
for k,g in var.items():
    d=(g!=base); d[ZONE]=False
    print(k,'diff buiten oogzone (rij 10-14, x11-14):',int(d.sum()),'| px gewijzigd in zone:',int((g!=base)[ZONE].sum()))
    schrijf(f'rufflet_r3{k}.txt',g)
    s=np.full((64,64),'.'); h,w=g.shape; x0=(64-w)//2; s[64-h:64,x0:x0+w]=g
    idx=np.vectorize(L.get)(s).astype('uint8'); p=Image.fromarray(idx,'P'); pal=[v for _,c in PAL for v in c]
    p.putpalette(pal+[0]*(768-len(pal))); p.save(f'rufflet_r3{k}.png',transparency=0)
    Image.fromarray(rgb(s,(255,255,255))).resize((512,512),Image.NEAREST).save(f'rufflet_r3{k}_8x.png')
    print('\n'.join(''.join(r[9:17]) for r in g[9:16]))
