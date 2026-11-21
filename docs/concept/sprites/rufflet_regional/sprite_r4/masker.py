# r4: masker van het model groter (dilatatie 1 of 2 px in de witte kop; buitenlijn, snavel en silhouet blijven), daarin Rufflets oog pixel voor pixel.
import numpy as np; from PIL import Image; from pal import *
R=np.asarray(Image.open('../referenties/rufflet_anim_front.png'))[:64]
M={4:'W',2:'K',1:'b',11:'n',10:'a',7:'w'}
ruf=lambda y0,y1,x0,x1: np.vectorize(lambda v:M[int(v)])(R[y0:y1,x0:x1])
base=lees('rufflet_r2.txt'); H,W=base.shape
ZY,ZX=slice(5,18),slice(5,21)   # kop/maskerzone
def masker(n):
    g=base.copy(); m=np.zeros((H,W),bool)
    m[7:16,7:17]=np.isin(base[7:16,7:17],list('ab')); m[10:15,11:15]=True   # modelmasker + oogplek
    kop=np.isin(base,list('Wwv')); kop[:5]=False; kop[15:]=False; kop[:,:7]=False
    for _ in range(n):
        d=m.copy()
        for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)): d|=np.roll(np.roll(m,dy,0),dx,1)
        m|=d&kop
    nieuw=m&kop
    g[nieuw]='b'
    # rand: maskerpixels die aan de witte kop grenzen aan de bovenkant (licht) of achterkant krijgen a, zoals het model (a langs de bovenrand en punten)
    for y in range(H):
        for x in range(W):
            if m[y,x] and g[y,x] in 'ab' and not (10<=y<=14 and 11<=x<=14):
                up=y>0 and g[y-1,x] in 'Wwvu'
                g[y,x]='a' if up else 'b'
    return g
def oog(g,rows):
    g=g.copy()
    if rows=='5': g[10:15,11:15]=ruf(26,31,30,34)
    else: g[11:15,11:15]=ruf(27,31,30,34); g[10,11:15]='b'
    return g
var={'A':oog(masker(1),'5'),'B':oog(masker(2),'5'),'C':oog(masker(2),'4')}
for k,g in var.items():
    d=(g!=base); d[ZY,ZX]=False
    print(k,'diff buiten kop/maskerzone (rij 5-17, x5-20):',int(d.sum()),'| px gewijzigd:',int((g!=base).sum()),'| silhouet:',int(((g!='.')!=(base!='.')).sum()))
    schrijf(f'rufflet_r4{k}.txt',g)
    s=np.full((64,64),'.'); h,w=g.shape; x0=(64-w)//2; s[64-h:64,x0:x0+w]=g
    idx=np.vectorize(L.get)(s).astype('uint8'); p=Image.fromarray(idx,'P'); pal=[v for _,c in PAL for v in c]
    p.putpalette(pal+[0]*(768-len(pal))); p.save(f'rufflet_r4{k}.png',transparency=0)
    Image.fromarray(rgb(s,(255,255,255))).resize((512,512),Image.NEAREST).save(f'rufflet_r4{k}_8x.png')
    print('\n'.join('%2d '%(y)+''.join(g[y,5:21]) for y in range(6,18)))
