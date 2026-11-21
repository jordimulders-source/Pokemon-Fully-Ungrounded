# bewijs + telling: (1) pixeldiff t.o.v. r3 buiten het potengebied (moet 0 zijn);
# (2) afwijking t.o.v. de kale reductie binnen het potengebied, per poot; (3) verschilkaart
import numpy as np; from PIL import Image
from reduce_pal import PAL
r3=np.loadtxt('vlieg_r3.txt',dtype=int); r4=np.loadtxt('vlieg_r4.txt',dtype=int)
kaal=np.loadtxt('kaal_r3.txt',dtype=int); s1=np.loadtxt('r4_stap1.txt',dtype=int)
H,W=kaal.shape; zone=np.zeros((64,64),bool); z=np.zeros((H,W),bool); z[23:,:39]=True; z[30:,:]=True
zone[16:16+H,6:6+W]=z; zone[:, :6]|=False
d=(r3!=r4)
print('pixels anders dan r3 BUITEN potengebied:',int((d&~zone).sum()))
print('pixels anders dan r3 binnen potengebied:',int((d&zone).sum()))
c4=r4[16:62,6:56]; ext=(c4!=s1)
def pt(r,c):
    if c<=11 and r<=41: return 'poot 1'
    if c<=17: return 'poot 2'
    if c<=31 and r>=27 or (c<=25): return 'poot 3'
    return 'poot 4 (+ boog over achterlijf)'
T={}
for r in range(H):
    for c in range(W):
        if z[r,c] and s1[r,c]!=kaal[r,c]: T[pt(r,c)]=T.get(pt(r,c),0)+1
for k in sorted(T): print(f'{k:32s} {T[k]:4d} px anders dan de kale reductie')
print('extra verre poten (kopie, schaduwtint):',int(ext.sum()),'px zichtbaar')
a=np.array([(255,255,255)]+PAL[1:])[c4].astype('uint8'); a=(a*0.35+165).astype('uint8')
m=(s1!=kaal)&z; a[m]=(255,0,0); a[ext]=(0,160,255); a[(r3!=r4)[16:62,6:56]&~z]=(0,200,0)
Image.fromarray(a).resize((W*8,H*8),Image.NEAREST).save('verschil.png')
