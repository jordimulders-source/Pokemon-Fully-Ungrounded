# Oogvarianten op r3: alleen het ooggebied, elke pixel uit het model (natief raster) met een andere/strengere regel.
# Gebruik: python3 ogen.py UIT.png REGEL [dy dx]   REGEL: A (streng: zwart bij >= 5/9 zwarte modelpx, omtrek waar
#   het model >= 2 zwarte px heeft en aan iris grenst, glans op de modelplek) | B (A-regel op een verschoven fase dy,dx natieve px)
import sys,numpy as np; from PIL import Image
from groepen import laad, tonen
UIT=sys.argv[1]; R=sys.argv[2]; DY=int(sys.argv[3]) if len(sys.argv)>3 else 0; DX=int(sys.argv[4]) if len(sys.argv)>4 else 0
R3=Image.open('pitahaya_r3.png'); r3=np.asarray(R3).astype(int); pal=R3.getpalette()
OY,OX,ymin,xmin,y0,x0=np.load('kaal_info.npz')['geo']
a,lum,g=laad(); TA=tonen(a,lum,g,5,2); TR=tonen(a,lum,g,2,4)
P=np.array(pal[:48]).reshape(16,3)
# ooggebied (spritecoordinaten): verre oog x 18-23, nabije oog x 28-36, y 22-27; zonder randpixels (silhouet/buitenlijn bevroren)
m=r3>0; pad=np.pad(m,1); rand=m&~(pad[:-2,1:-1]&pad[2:,1:-1]&pad[1:-1,:-2]&pad[1:-1,2:])
ZONE=np.zeros((64,64),bool); ZONE[22:28,18:24]=1; ZONE[22:28,28:37]=1; ZONE&=m&~rand
def blok(Y,X):
    ny=OY+DY+3*(Y-y0+ymin); nx=OX+DX+3*(X-x0+xmin); return slice(ny,ny+3),slice(nx,nx+3)
o=r3.copy(); Z={}; A={}; W={}
for Y,X in zip(*np.where(ZONE)):
    gb=g[blok(Y,X)]; Z[Y,X]=(gb==1).sum(); A[Y,X]=(gb==5).sum(); W[Y,X]=(gb==6).sum()
def roze(Y,X):
    if r3[Y,X] not in (1,12,13,14): return r3[Y,X]       # roze/groen/mauve uit r3 blijft
    sl=blok(Y,X); gb=g[sl]; px=a[sl][gb==2]
    if not len(px): return 4
    c=px.mean(0); return [2,3,4,5][((P[[2,3,4,5]]-c)**2).sum(1).argmin()]
for (Y,X) in Z:
    if Z[Y,X]>=5: o[Y,X]=1
    elif A[Y,X]>=3:
        sl=blok(Y,X); c=a[sl][g[sl]==5].mean(0); o[Y,X]=12+((P[[12,13]]-c)**2).sum(1).argmin()
    else: o[Y,X]=roze(Y,X)
# omtrek: roze cel naast iris waar het model >= 2 zwarte px heeft -> zwart (doorlopende 1-px lijn)
for (Y,X) in Z:
    if o[Y,X] in (2,3,4,5) and Z[Y,X]>=2 and any(o[Y+dy,X+dx] in (12,13) for dy,dx in ((1,0),(-1,0),(0,1),(0,-1))): o[Y,X]=1
# glans: per oog de cel met de meeste witte modelpx (bij gelijk: de cel met de meeste amber)
for xs in ((18,24),(28,37)):
    c=[(W[k],A[k],k) for k in W if xs[0]<=k[1]<xs[1] and W[k]>0]
    if c: o[max(c)[2]]=14
p=Image.fromarray(o.astype('uint8'),'P'); p.putpalette(pal); p.save(UIT,transparency=0)
d=(o!=r3); assert not (d&~ZONE).any(); print(UIT,'gewijzigd',d.sum(),'buiten zone',(d&~ZONE).sum())
for Y in range(21,29): print(Y,''.join('.123456789ABCDEF'[v] if v else '.' for v in r3[Y,16:39]),'  ',''.join('.123456789ABCDEF'[v] if v else '.' for v in o[Y,16:39]))
