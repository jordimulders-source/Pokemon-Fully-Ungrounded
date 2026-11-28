"""Shuppetto-icoon onderlaag: onderdelen van de front, per groep geschaald, kleur = meest voorkomende (gemapte) kleur.
python3 bouw.py naam s_kop s_kruis  -> icoon/<naam>.png (32x32 pal0) + <naam>_8x.png"""
import sys,numpy as np
from PIL import Image,ImageDraw
D='docs/concept/sprites/banette_evo/'
naam=sys.argv[1]; s_k=float(sys.argv[2]); s_x=float(sys.argv[3])
fr=np.array(Image.open(D+'af/shuppetto.png'))[:64]
IP=np.array([[int(v) for v in l.split()[:3]] for l in open('graphics/pokemon/icon_palettes/pal0.pal').read().split('\n')[3:19]])
# front-index -> pal0-index (grijs 2/3/4 -> 2/1/14, rood 6/7/f -> 6/6/11, mond 8 -> 15, oog 9 -> 5, lijn 1 -> 15)
MAP={1:15,2:2,3:1,4:14,6:6,7:6,15:6,8:15,9:5,5:12,10:12,11:12,12:12,13:2,14:15}
DELEN=[ # naam, polygoon; eerste match wint
 ('shuppet_l',[(0,39),(17,39),(17,63),(0,63)]),
 ('shuppet_r',[(44,45),(63,45),(63,63),(44,63)]),
 ('bel',[(3,32),(11,32),(11,39),(3,39)]),
 ('kruis_l',[(0,15),(13,15),(13,32),(0,32)]),
 ('kruis_r',[(46,14),(63,14),(63,32),(46,32)]),
 ('kop',[(0,0),(63,0),(63,63),(0,63)]),
]
lab=np.full((64,64),-1)
for i,(n,poly) in reversed(list(enumerate(DELEN))):
    m=Image.new('L',(64,64),0); ImageDraw.Draw(m).polygon(poly,fill=1,outline=1); lab[(np.array(m)>0)&(fr>0)&(fr!=13)]=i
names=[d[0] for d in DELEN]
C=np.array([32.0,30.0])  # anker: midden-onder van de kop
def doel_naar_bron(X,Y,s): return C+(np.array([X,Y],float)-np.array([16.0,0.0])-C*0)/1, None
out=np.zeros((48,48),np.uint8)
O=np.array([24.0,40.0])  # anker in uitvoer
for n,s in [('kruis_l',s_x),('kruis_r',s_x),('kop',s_k)]:
    pm=lab==names.index(n)
    for Y in range(48):
        for X in range(48):
            sx,sy=C+(np.array([X,Y])-O)/s; k=1/s
            x0,y0=int(np.floor(sx)),int(np.floor(sy)); x1,y1=int(np.ceil(sx+k)),int(np.ceil(sy+k))
            x0,y0=max(0,x0),max(0,y0); x1,y1=min(64,x1),min(64,y1)
            if x1<=x0 or y1<=y0: continue
            sel=pm[y0:y1,x0:x1]
            if sel.mean()<0.45: continue
            v=np.vectorize(MAP.get)(fr[y0:y1,x0:x1][sel])
            dk=(v==15).mean()
            if dk>0.5: out[Y,X]=15
            else:
                vv,cc=np.unique(v[v!=15],return_counts=True); out[Y,X]=vv[cc.argmax()]
ys,xs=np.nonzero(out); c=out[ys.min():ys.max()+1,xs.min():xs.max()+1]; h,w=c.shape
res=np.zeros((32,32),np.uint8); oy=29-h+1; ox=16-w//2
res[oy:oy+h,ox:ox+w]=c
im=Image.fromarray(res,'P'); im.putpalette(IP.flatten().tolist()+[0]*720); im.save(D+f'icoon/{naam}.png')
rgb=IP[res].astype(np.uint8); rgb[res==0]=(115,197,164)
Image.fromarray(rgb).resize((256,256),Image.NEAREST).save(D+f'icoon/{naam}_8x.png')
print(naam,w,'x',h)
for r in res: print(''.join('.' if v==0 else '%x'%v for v in r))
