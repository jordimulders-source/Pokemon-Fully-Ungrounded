# c7: c6-koppen (a/b/c) + sterkere rots-pass (facetten.py + rots.py). Patroon en posities van voluten/banden blijven.
import numpy as np
from PIL import Image, ImageDraw
import facetten
from basis import bevroren_kop
from rots import rand, rots as belijning
F=bevroren_kop(); P8=np.array(Image.open('../p8/welp_p8.png')); R=rand(P8>0)
def poly(pts):
    im=Image.new('L',(64,64),0); d=ImageDraw.Draw(im)
    if len(pts)==2: d.line(pts,fill=1)
    else: d.polygon(pts,fill=1,outline=1)
    return np.array(im)>0
def maak(v):
    a=np.array(Image.open(f'../c6/welp_c6_{v}.png'))
    G=np.isin(a,[1,2])&~R&~np.isin(P8,[1,2])&~F          # motiefgroeven (lijf + kop)
    teen=(P8==14)
    S=(a>0)&~R&~F&~np.isin(P8,[1,2])&~G&~teen&np.isin(a,[3,4,5,14])   # steenpixels
    # lippen van c6 terugrekenen naar hun vlaktint (meest voorkomende niet-lip-buur)
    lip=np.zeros_like(S)
    for y,x in zip(*np.where(S)):
        if (G[y-1,x] or G[y,x-1]): lip[y,x]=True
    base=a.copy()
    for y,x in zip(*np.where(lip)):
        w=[a[y+dy,x+dx] for dy in (-1,0,1) for dx in (-1,0,1) if S[y+dy,x+dx] and not lip[y+dy,x+dx]]
        base[y,x]=max(set(w),key=w.count) if w else 4
    base[S&(base==14)]=5
    for n,t,pts in facetten.FACETTEN:
        m=poly(pts)&S; base[m]=t
    o=a.copy(); o[S]=base[S]
    for y,x in zip(*np.where(lip)):
        if base[y,x]==2: continue
        boven=G[y-1,x] and not G[min(y+1,63),x]; links=G[y,x-1] and not G[y,min(x+1,63)]
        if boven or links: o[y,x]=14 if base[y,x]==5 else 5
    for x,y in facetten.RANDEN:
        if S[y,x] and not lip[y,x] and base[y,x]==5: o[y,x]=14
    return belijning(o)
def bewaar(a,naam,pal):
    im=Image.fromarray(a.astype(np.uint8),'P'); im.putpalette(pal+[0]*(768-48)); im.save(naam+'.png',transparency=0)
    r=Image.open(naam+'.png').convert('RGBA'); bg=Image.new('RGBA',r.size,(255,255,255,255)); bg.alpha_composite(r)
    bg.resize((512,512),Image.NEAREST).save(naam+'_8x.png')
if __name__=='__main__':
    for v in 'abc':
        a=maak(v)
        bewaar(a,'welp_c7_'+v,Image.open('../c6/welp_c6_c.png').getpalette()[:48])
        bewaar(a,'welp_c7_'+v+'_grijs',Image.open('../c6/welp_c6_c_grijs.png').getpalette()[:48])
