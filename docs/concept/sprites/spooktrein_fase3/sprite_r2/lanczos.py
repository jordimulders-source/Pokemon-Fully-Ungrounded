# Onderlaag r2: het model zelf (model.webp, 1024) met LANCZOS naar 64 breed (= de bron van het paneel "model verkleind"),
# daarna elke pixel naar de dichtstbijzijnde kleur van het r1-palet (modeltinten). Silhouet: niet-wit (min kanaal < WT).
# Gebruik: python3 lanczos.py [WT] [out] [filter] [LK zwartdrempel] [LKO in oogzone] [LG donkergroendrempel]
import sys; from PIL import Image; import numpy as np
WT=int(sys.argv[1]) if len(sys.argv)>1 else 0xe0; OUT=sys.argv[2] if len(sys.argv)>2 else 'lanczos.png'
F={'lan':Image.LANCZOS,'bic':Image.BICUBIC,'box':Image.BOX}[sys.argv[3] if len(sys.argv)>3 else 'lan']
m=Image.open('../model/model.webp').convert('RGB')
a=np.asarray(m).astype(int); wit=a.min(2)>=0xe0
ys,xs=np.where(~wit); print('model bbox',xs.min(),xs.max(),ys.min(),ys.max())
c=m.crop((xs.min(),ys.min(),xs.max()+1,ys.max()+1)); W=64; H=round(W*c.size[1]/c.size[0])
r=np.asarray(c.resize((W,H),F)).astype(float)
# zones met fijne roest-/wolktextuur: zelfde model, eerst licht vervaagd (Gauss) en dan verkleind, zodat de grote vormen
# (spijlen, wolklobben) blijven en de spikkels verdwijnen. Zones in spritecoordinaten (x0,x1,y0,y1), straal in 1024-px.
from PIL import ImageFilter
ZONES=[((0,26,47,63),float(sys.argv[7]) if len(sys.argv)>7 else 0,'koeienvanger'),
       ((24,63,14,55),float(sys.argv[8]) if len(sys.argv)>8 else 0,'wolken')]
OYc=64-H
for (zx0,zx1,zy0,zy1),rad,nm in ZONES:
    if rad<=0: continue
    rb=np.asarray(c.filter(ImageFilter.GaussianBlur(rad)).resize((W,H),F)).astype(float)
    for y in range(max(0,zy0-OYc),min(H,zy1-OYc+1)):
        for x in range(zx0,zx1+1):
            if nm=='wolken':
                q=r[y,x]
                if not (q[1]>q[0]+15 and q.min()<0xe0 and q[1]<225): continue   # alleen bleke wolkpixels, niet de felle wielen
            r[y,x]=rb[y,x]
pal=Image.open('../sprite_r1/sprite.png').getpalette()[:3*13]; P=np.array(pal).reshape(-1,3)[1:].astype(float)
# lijnbehoud: dekking van zwarte en donkergroene modellijnen per spritepixel (oppervlak-middeling uit 1024)
ca=np.asarray(c).astype(int)
def dek(mask): return np.asarray(Image.fromarray((mask*255).astype('uint8')).resize((W,H),Image.BOX)).astype(float)/255
DK=dek(ca.sum(2)<150); DG=dek((ca[...,1]>ca[...,0]+20)&(ca.sum(2)<330)&(ca.sum(2)>=150))
LK=float(sys.argv[4]) if len(sys.argv)>4 else 9; LKO=float(sys.argv[5]) if len(sys.argv)>5 else LK; LG=float(sys.argv[6]) if len(sys.argv)>6 else 9
OOG=(1,27,26,37)
LKC=float(sys.argv[9]) if len(sys.argv)>9 else LK  # oogzone in spritecoordinaten (x0,x1,y0,y1), lagere zwartdrempel voor ooglid en pupil
out=np.zeros((64,64),'uint8'); oy=64-H
for y in range(H):
    for x in range(W):
        if r[y,x].min()>=WT: continue
        out[oy+y,x]=1+((P-r[y,x])**2).sum(1).argmin()
        if oy+y<=13 and x>=12 and DK[y,x]<0.2:   # kleine geest: het model heeft daar geen zwart (LANCZOS-overshoot), dichtstbijzijnde groen
            out[oy+y,x]=1+[i for i in np.argsort(((P-r[y,x])**2).sum(1)) if i in (1,2,3,4,5)][0]
        lk=LKO if (OOG[0]<=x<=OOG[1] and OOG[2]<=oy+y<=OOG[3]) else LK
        if 0<=x<=26 and 47<=oy+y<=63: lk=LKC   # koeienvanger: alleen de echte spleten zwart
        if DK[y,x]>=lk: out[oy+y,x]=1
        elif DG[y,x]>=LG and out[oy+y,x] in (2,3,4,5): out[oy+y,x]=6
# koeienvanger: spikkels in de vlakken weg met een meerderheidsfilter (zwart = lijn, blijft staan; alleen roest/ijzer-tinten)
for _ in range(int(sys.argv[10]) if len(sys.argv)>10 else 0):
    n=out.copy()
    for y in range(47,64):
        for x in range(0,27):
            if out[y,x] in (7,8,9,10,11,12):
                c=[int(out[y+dy,x+dx]) for dy in (-1,0,1) for dx in (-1,0,1) if 0<=y+dy<64 and 0<=x+dx<64 and out[y+dy,x+dx] in (7,8,9,10,11,12)]
                m=max(set(c),key=c.count)
                if c.count(m)>c.count(int(out[y,x])): n[y,x]=m
    out=n
im=Image.fromarray(out,'P'); im.putpalette(pal+[0]*(768-len(pal))); im.save(OUT,transparency=0); print('maat',W,H)
