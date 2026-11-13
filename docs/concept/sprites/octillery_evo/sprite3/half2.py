# natief (127x115) -> 2x2-reductie met regels + vast palet. Gebruik: python3 half2.py IN UIT [oy ox]
# Niets wordt getekend: elke spritepixel komt uit zijn 2x2-blok modelpixels.
import sys; from PIL import Image; import numpy as np
IN,UIT=sys.argv[1],sys.argv[2]; OY=int(sys.argv[3]) if len(sys.argv)>3 else 1; OX=int(sys.argv[4]) if len(sys.argv)>4 else 0
a=np.asarray(Image.open(IN).convert('RGB')).astype(int); H,W=a.shape[:2]
R,G,B=a[...,0],a[...,1],a[...,2]; lum=(0.299*R+0.587*G+0.114*B)
bg=a.min(axis=2)>=215
yel=(R>165)&(G>120)&(R-B>60)&(G-B>35)&~bg
drk=(lum<50)&~bg; blk=(lum<24)&~bg
# palet: index 1 omlijning, 2 lijnrood, 3-7 rood (donker->licht), 8-9 mondroze, 10-12 geel
PAL=[(255,0,255),(24,10,12),(80,22,30),(106,34,45),(124,44,56),(148,52,66),(164,66,78),(184,100,108),(140,74,84),(180,112,116),(170,128,52),(228,196,112),(244,226,156)]
def cls(px):   # px: Nx3 niet-donker, niet-geel -> index
    r,g,b=px.mean(0); l=0.299*r+0.587*g+0.114*b; sat=(max(r,g,b)-min(r,g,b))/max(r,g,b,1)
    pass
    for i,t in ((3,60),(4,73),(5,89),(6,108)):
        if l<t: return i
    return 7
h=(H-OY)//2; w=(W-OX)//2; o=np.zeros((h,w),int); nd=np.zeros((h,w),int)
for j in range(h):
    for i in range(w):
        sl=(slice(OY+2*j,OY+2*j+2),slice(OX+2*i,OX+2*i+2))
        if bg[sl].sum()>=3: continue
        m=~bg[sl]; d=drk[sl]&m; y=yel[sl]&m; nd[j,i]=d.sum()
        if y.sum()>=1 and d.sum()>=1:
            # pupil: donkere modelpixel met geel links en rechts ervan
            pup=False
            for yy in range(OY+2*j,OY+2*j+2):
                for xx in range(OX+2*i,OX+2*i+2):
                    if drk[yy,xx] and yel[yy,max(xx-3,0):xx].any() and yel[yy,xx+1:xx+4].any(): pup=True
            if pup: o[j,i]=1; continue
        if y.sum()>=2:
            l=lum[sl][y].mean(); o[j,i]=10 if l<150 else (11 if l<195 else 12); continue
        rest=m&~d
        if d.sum()>=3 or rest.sum()==0: o[j,i]=1 if (blk[sl]&m).sum()*2>=d.sum() else 2; continue
        o[j,i]=cls(a[sl][rest]) if d.sum()<2 else -1
# blokken met precies 2 donkere pixels: lijn alleen houden als hij anders zou breken of op de rand ligt
for j in range(h):
    for i in range(w):
        if o[j,i]!=-1: continue
        sl=(slice(OY+2*j,OY+2*j+2),slice(OX+2*i,OX+2*i+2)); d=drk[sl]
        nb=[(j-1,i),(j+1,i),(j,i-1),(j,i+1)]
        edge=any(not(0<=y<h and 0<=x<w) or (o[y,x]==0) for y,x in nb)
        vert=d[:,0].all() or d[:,1].all(); hor=d[0,:].all() or d[1,:].all()
        # dikte: als een buur loodrecht op de lijn al volledig donker is, is deze rij/kolom de tweede helft van dezelfde lijn
        thick=False
        if vert: thick=any(0<=x<w and nd[j,x]>=3 for x in (i-1,i+1))
        if hor: thick=thick or any(0<=y<h and nd[y,i]>=3 for y in (j-1,j+1))
        if edge or not thick: o[j,i]=1 if (blk[sl].sum()>=1 or edge) else 2
        else: o[j,i]=-2
for j in range(h):
    for i in range(w):
        if o[j,i]==-2:
            sl=(slice(OY+2*j,OY+2*j+2),slice(OX+2*i,OX+2*i+2)); rest=~bg[sl]&~drk[sl]
            o[j,i]=cls(a[sl][rest]) if rest.any() else 2
ys,xs=np.where(o>0); o2=o[ys.min():ys.max()+1,xs.min():xs.max()+1]; hh,ww=o2.shape
full=np.zeros((64,64),int); x0=(64-ww)//2; full[63-hh:63,x0:x0+ww]=o2
p=Image.fromarray(full.astype('uint8'),'P'); pal=[v for c in PAL for v in c]; p.putpalette(pal+[0]*(768-len(pal))); p.save(UIT,transparency=0)
tot=(full>0).sum(); print(UIT,ww,hh,tot,'zwart %.1f%% lijnrood %.1f%%'%(100*(full==1).sum()/tot,100*(full==2).sum()/tot),'kleuren',len(set(full.ravel()))-1)
