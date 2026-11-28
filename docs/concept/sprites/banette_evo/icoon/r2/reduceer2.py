# Shuppetto-icoon r2, onderlaag: exacte 2x2-reductie van de FRONT, niets getekend.
# Structuur per blok uit de frontindexen (transparant / omlijning / oog / mond / vulling, regels als half2.py);
# vulkleur = gemiddelde RGB van de niet-lijnpixels in het blok -> dichtstbijzijnde kleur van het gekozen icoonpalet.
# Gebruik: python3 reduceer2.py OY OX PAL x0 x1 'schraprijen' UIT
import sys; from PIL import Image; import numpy as np
FR=Image.open('docs/concept/sprites/banette_evo/af/shuppetto.png' if len(sys.argv)<9 else sys.argv[8])
a=np.array(FR).astype(int); fp=np.array(FR.getpalette()[:48]).reshape(16,3)
weg=(a==13)
for (x0,y0,x1,y1) in ((2,40,17,59),(45,42,63,62),(5,33,11,39)): weg[y0:y1,x0:x1]=True   # Shuppets, linkerbel
a=np.where(weg,0,a)
OY,OX,P=int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3])
L=np.array([list(map(int,l.split())) for l in open('graphics/pokemon/icon_palettes/pal%d.pal'%P).read().split('\n')[3:19]])
def near(c):
    r=(c[0]+L[1:,0])/2; d=L[1:]-c
    return 1+int(np.argmin((2+r/256)*d[:,0]**2+4*d[:,1]**2+(2+(255-r)/256)*d[:,2]**2))
LIJN=near(fp[1])
H,W=a.shape; h=(H-OY)//2; w=(W-OX)//2
o=np.zeros((h,w),int); nd=np.zeros((h,w),int)
def vul(b):
    v=[x for x in b.ravel() if x not in (0,1)]
    return near(fp[v].mean(0)) if v else LIJN
for j in range(h):
    for i in range(w):
        b=a[OY+2*j:OY+2*j+2,OX+2*i:OX+2*i+2]
        t=(b==0).sum(); d=(b==1).sum(); nd[j,i]=d
        if t>=3: continue
        if (b==9).sum()>=1: o[j,i]=near(fp[9]); continue
        if (b==8).sum()>=2: o[j,i]=near(fp[8]); continue
        if d>=3: o[j,i]=LIJN; continue
        if t==2: o[j,i]=LIJN if d>=1 else vul(b); continue
        if d==2: o[j,i]=-1; continue
        o[j,i]=vul(b)
for j in range(h):
    for i in range(w):
        if o[j,i]!=-1: continue
        b=a[OY+2*j:OY+2*j+2,OX+2*i:OX+2*i+2]; dd=(b==1)
        nb=[(j-1,i),(j+1,i),(j,i-1),(j,i+1)]
        edge=any(not(0<=y<h and 0<=x<w) or o[y,x]==0 for y,x in nb)
        vert=dd[:,0].all() or dd[:,1].all(); hor=dd[0,:].all() or dd[1,:].all()
        thick=False
        if vert: thick=any(0<=x<w and nd[j,x]>=3 for x in (i-1,i+1))
        if hor: thick=thick or any(0<=y<h and nd[y,i]>=3 for y in (j-1,j+1))
        o[j,i]=LIJN if (edge or not thick) else vul(b)
x0,x1=int(sys.argv[4]),int(sys.argv[5]); schrap=[int(v) for v in sys.argv[6].split(',') if v]
o=np.delete(o[:,x0:x1+1],schrap,axis=0)
ys,xs=np.where(o>0); q=o[ys.min():ys.max()+1,xs.min():xs.max()+1]; hh,ww=q.shape
f=np.zeros((32,32),int); X=16-(ww+1)//2; f[29-hh:29,X:X+ww]=q
UIT=sys.argv[7]; np.save(UIT+'.npy',f)
im=Image.fromarray(f.astype('uint8'),'P'); im.putpalette(list(L.ravel())+[0]*(768-48)); im.save(UIT+'.png',transparency=0)
print(UIT,'b',ww,'h',hh)
