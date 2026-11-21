# afwijking per zone t.o.v. de kale reductie (kaal_r3.txt = model met geschrapte rijen/kolommen) + verschilkaart
import numpy as np; from PIL import Image
from reduce_pal import PAL
k=np.loadtxt('kaal_r3.txt',dtype=int); s1=np.loadtxt('r3_stap1.txt',dtype=int)
f=np.loadtxt('vlieg_r3.txt',dtype=int)[16:62,6:56]
H,W=k.shape; Z={}
for r in range(H):
    for c in range(W):
        if f[r,c]==k[r,c]: continue
        if s1[r,c]!=f[r,c]: z='extra verre poten (kopie)' if r>=26 else 'vleugelruis'
        elif r<8 and c<17: z='voelsprieten'
        elif r<=22 and c<=18: z='kop (incl. ogen)'
        elif r<=12 and c>=19: z='vleugels'
        elif r>=23 or (r>=21 and 21<=c<=24): z='poten + klauwtjes'
        else: z='borststuk/achterlijf'
        Z[z]=Z.get(z,0)+1
tot=(f>0).sum()
for z,n in sorted(Z.items()): print(f'{z:28s} {n:4d}')
print('totaal afwijkend',sum(Z.values()),'van',tot,'px')
a=np.array([(255,255,255)]+PAL[1:])[f].astype('uint8'); a=(a*0.35+165).astype('uint8')
m=(f!=k); a[m]=(255,0,0); a[m&(s1!=f)]=(0,160,255)
Image.fromarray(a).resize((W*8,H*8),Image.NEAREST).save('verschil.png')
