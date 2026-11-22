# Kale verkleining van het r12-lijf op exact de spriteschaal van het r1-hoofd in model_16.
# Spritepixel i,j <-> r5-pixel via het natieve r5-raster (pitch 4,267; r1 = 2/3 per natieve cel, kop_kaal begint
# bij natieve kol 75 / rij 8 en ligt op sprite (4,1)) <-> model_16 (transform.json) <-> r12 (model + 94, -45).
# Per spritepixel: vlakgemiddelde van de r12-pixels in het vak; >=30% donker -> donkerste (lijn); dekking >=50%.
# Dichtstbijzijnde kleur uit zwart + 3 modelgroenen. Niets getekend.
import json, numpy as np; from PIL import Image; from scipy import ndimage; from pal import PAL
T=json.load(open('transform.json')); f=T['f']
import sys
BRON=sys.argv[1] if len(sys.argv)>1 else '../gemini/r12.png'; UIT=sys.argv[2] if len(sys.argv)>2 else 'lijf_kaal.npy'
a=np.asarray(Image.open(BRON).convert('RGB')).astype(float)
nw=a.sum(2)<720
yel=(a[:,:,0]>150)&(a[:,:,1]>120)&(a[:,:,2]<170)&(a[:,:,0]>a[:,:,1]-10); yel[650:]=False
kop12=ndimage.binary_dilation(ndimage.binary_fill_holes(ndimage.binary_closing(yel,iterations=3)),iterations=6)
body=nw&~kop12; body[:560]=False
lum=a@[.3,.59,.11]
def r12x(sx):  # spritekolom (rand) -> r12 x
    x5=4.1+4.267*(75+1.5*(sx-4)); return x5*f+T['ox']-T['r12x']
def r12y(sy):
    y5=4.4+4.267*(8+1.5*(sy-1)); return y5*f+T['oy']-T['r12y']
print('spritepixel = %.2f r12-px (natief 10,24 -> schaal %.3f)'%(r12x(5)-r12x(4),10.24/(r12x(5)-r12x(4))))
P=np.array(PAL,float); cand=[1,11,12,13]
out=np.zeros((64,64),'uint8')
for j in range(64):
    y0,y1=r12y(j),r12y(j+1)
    for i in range(64):
        x0,x1=r12x(i),r12x(i+1)
        Y0,Y1,X0,X1=int(round(y0)),int(round(y1)),int(round(x0)),int(round(x1))
        if Y1<=0 or X1<=0 or Y0>=1024 or X0>=1024: continue
        Y0,X0=max(Y0,0),max(X0,0); m=body[Y0:Y1,X0:X1]
        if m.size==0 or m.mean()<0.5: continue
        c=a[Y0:Y1,X0:X1][m]; l=lum[Y0:Y1,X0:X1][m]; dk=l<70
        col=c[dk].mean(0) if dk.mean()>=0.3 else c[~dk].mean(0)
        out[j,i]=cand[int(np.argmin(((P[cand]-col)**2).sum(1)))]
np.save(UIT,out)
ys,xs=np.where(out); print('lijf rijen',ys.min(),ys.max(),'kol',xs.min(),xs.max())
ch='.123456789abcdef'
for y in range(ys.min(),ys.max()+1): print('%2d'%y,''.join(ch[v] for v in out[y]))
