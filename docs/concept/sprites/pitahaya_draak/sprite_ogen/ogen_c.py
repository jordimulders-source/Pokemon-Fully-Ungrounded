# Variant C: Gen 3-oog overgenomen uit Shiftry (graphics/pokemon/shiftry/anim_front.png, frame 1, x 21-27, y 24-28),
#   pixel voor pixel; lid (96,64,40) en zwart -> onze zwart (1), geel iris (240,224,128) -> ons licht amber (13).
#   Nabije oog: hele Shiftry-oog op de plek van het modeloog (verschuiving +8, -1). Verre oog: hetzelfde oog met
#   geschrapte kolommen (perspectief smaller, gengas/schrap-methode), op de plek van het verre modeloog.
#   Oogpixels van r3 die buiten het nieuwe oog vallen -> roze huid uit het model (blokgemiddelde -> dichtstbijzijnde roze).
import sys,numpy as np; from PIL import Image
from groepen import laad
UIT=sys.argv[1]; KOL=[int(c) for c in sys.argv[2].split(',')] if len(sys.argv)>2 else [1,3,4,6]
VX,VY=int(sys.argv[3]) if len(sys.argv)>3 else 19, int(sys.argv[4]) if len(sys.argv)>4 else 23
R3=Image.open('pitahaya_r3.png'); r3=np.asarray(R3).astype(int); pal=R3.getpalette(); P=np.array(pal[:48]).reshape(16,3)
OY,OX,ymin,xmin,y0,x0=np.load('kaal_info.npz')['geo']; a,lum,g=laad()
S=np.asarray(Image.open('../../../../../graphics/pokemon/shiftry/anim_front.png'))[24:29,21:28].astype(int)
MAP={1:1,4:1,13:13}            # Shiftry-index -> onze index; rest (vacht) = geen oog
oog=np.vectorize(lambda v: MAP.get(v,0))(S)
m=r3>0; pad=np.pad(m,1); rand=m&~(pad[:-2,1:-1]&pad[2:,1:-1]&pad[1:-1,:-2]&pad[1:-1,2:])
ZONE=np.zeros((64,64),bool); ZONE[22:28,18:24]=1; ZONE[22:28,28:37]=1; ZONE&=m&~rand
def roze(Y,X):
    ny=OY+3*(Y-y0+ymin); nx=OX+3*(X-x0+xmin); sl=(slice(ny,ny+3),slice(nx,nx+3)); px=a[sl][g[sl]==2]
    c=px.mean(0) if len(px) else P[4]; return [2,3,4,5][((P[[2,3,4,5]]-c)**2).sum(1).argmin()]
o=r3.copy()
for Y,X in zip(*np.where(ZONE)):
    if r3[Y,X] in (1,12,13,14): o[Y,X]=roze(Y,X)
def plak(pat,X0,Y0):
    for j in range(pat.shape[0]):
        for i in range(pat.shape[1]):
            if pat[j,i]:
                Y,X=Y0+j,X0+i; assert ZONE[Y,X],(Y,X); o[Y,X]=pat[j,i]
plak(oog,29,23); plak(oog[:,KOL],VX,VY)
pp=Image.fromarray(o.astype('uint8'),'P'); pp.putpalette(pal); pp.save(UIT,transparency=0)
d=o!=r3; assert not (d&~ZONE).any(); print(UIT,'gewijzigd',d.sum(),'buiten zone 0')
print(oog)
