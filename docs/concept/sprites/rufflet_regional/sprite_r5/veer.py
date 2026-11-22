# r5: Rufflets kuifveer (frame 1, rijen 10-24, x26-38) pixel voor pixel in onze kop; r4A bevroren buiten de veerzone.
# Plek: Rufflets veervoet (24,28) ligt vlak boven de snavel tussen de ogen -> bij ons boven de washuid (10,9); veer loopt schuin naar rechtsboven uit de kuif.
import numpy as np; from PIL import Image; import pal
from pal import *
R=np.asarray(Image.open('../referenties/rufflet_anim_front.png'))[:64].astype(int)
win=(slice(10,25),slice(26,39)); r=R[win]
fill=np.isin(r,[4,8,9])
# alleen het samenhangende veervlak (4-buren) vanaf de top
seen=np.zeros_like(fill); st=[(0,10)] if fill[0,10] else [tuple(np.argwhere(fill)[0])]
while st:
    y,x=st.pop()
    if 0<=y<r.shape[0] and 0<=x<r.shape[1] and fill[y,x] and not seen[y,x]: seen[y,x]=1; st+=[(y+1,x),(y-1,x),(y,x+1),(y,x-1)]
fill=seen.astype(bool)
rand=np.zeros_like(fill)
for y,x in zip(*np.where(fill)):
    for dy,dx in ((1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)):
        q=(y+dy,x+dx)
        if 0<=q[0]<r.shape[0] and 0<=q[1]<r.shape[1] and r[q] in (1,2,10) and not fill[q]: rand[q]=1
veer=fill|rand
print('Rufflet-veer:',int(fill.sum()),'vlak +',int(rand.sum()),'rand')
for y in range(r.shape[0]): print('   '+''.join(('0123456789ABCDEF'[r[y,x]] if veer[y,x] else '.') for x in range(r.shape[1])))
PAD=5
base=lees('rufflet_r4A.txt'); base=np.vstack([np.full((PAD,base.shape[1]),'.'),base])
def plaats(kleur,schrap=()):
    g=base.copy(); rows=[y for y in range(r.shape[0]) if y not in schrap]
    k=len(schrap); oy=10-24+PAD; ox=9-28
    for i,y in enumerate(rows):
        sh=k if y<min(schrap,default=99) else 0   # bovenstuk zakt k rijen
        for x in range(r.shape[1]):
            if veer[y,x]:
                Y=y+10+oy+sh; X=x+26+ox-(1 if sh else 0)
                g[Y,X]=kleur[r[y,x]]
    return g
V={'V1':plaats({4:'W',9:'r',8:'s',2:'K',1:'a',10:'n'}),
   'V2':plaats({4:'W',9:'w',8:'v',2:'K',1:'u',10:'n'}),
   'V3':plaats({4:'W',9:'r',8:'s',2:'K',1:'a',10:'n'},schrap=(4,5,6))}
pal.PAL+= [('r',(216,88,88)),('s',(160,64,64))]; pal.L={c:i for i,(c,_) in enumerate(pal.PAL)}; pal.RGB=np.array([c for _,c in pal.PAL])
for k,g in V.items():
    z=np.zeros(g.shape,bool)
    # veerzone = alle pixels waar een veerpixel kan landen (bounding box van de veer, alle varianten)
    z[PAD-5:PAD+11,9-2:9+11]=True
    d=(g!=base)&~z
    ys,xs=np.where(g!='.')
    print(k,'diff buiten veerzone (rij -5..10, x7-19):',int(d.sum()),'| px gewijzigd:',int((g!=base).sum()),'| hoogte',ys.max()-ys.min()+1,'| kleuren',len(set(g.ravel())-{'.'}))
    g=g[ys.min():]; schrijf(f'rufflet_r5{k}.txt',g)
    s=np.full((64,64),'.'); h,w=g.shape; x0=(64-w)//2; s[64-h:64,x0:x0+w]=g
    idx=np.vectorize(pal.L.get)(s).astype('uint8'); p=Image.fromarray(idx,'P'); pl=[v for _,c in pal.PAL for v in c]
    p.putpalette(pl+[0]*(768-len(pl))); p.save(f'rufflet_r5{k}.png',transparency=0)
    Image.fromarray(pal.rgb(s,(255,255,255))).resize((512,512),Image.NEAREST).save(f'rufflet_r5{k}_8x.png')
    print('\n'.join(''.join(row[4:24]) for row in g[:16]))
