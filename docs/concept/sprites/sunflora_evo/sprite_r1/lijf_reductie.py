# Kale reductie van het Gen 3-Sunflora-lijf (frame 1, rijen 32-55: armen, lijfje, voeten) naar schaal R/D.
# Vlakgemiddelde; omlijning (zwart / donkergroen c): donkerste wint bij >=35% dekking. Niets getekend.
import sys, numpy as np; from PIL import Image; from pal import PAL
from scipy import ndimage
R,D=int(sys.argv[1]),int(sys.argv[2])
s=Image.open('sunflora_f1.png'); sp=s.getpalette(); a=np.array(s)
green={12,13,14,15}
g=np.isin(a,list(green)); bl=(a==1)&ndimage.binary_dilation(g,iterations=1)
m=(g|bl); m[:32]=False
# losse zwarte kop-onderrand (grenst niet aan groen buiten de kop) weg: alleen component met groen
lab,n=ndimage.label(m); keep=np.isin(lab,[l for l in range(1,n+1) if (g&(lab==l)).any()]); m=keep
ys,xs=np.where(m); y0,x0=ys.min(),xs.min(); a=a[y0:ys.max()+1,x0:xs.max()+1]; m=m[y0:ys.max()+1,x0:xs.max()+1]
print('Sunflora-lijf origineel',a.shape[1],'x',a.shape[0],'rij',y0,'kol',x0)
rgb=np.array([sp[3*i:3*i+3] for i in range(16)],float)[a]
F=np.repeat(np.repeat(rgb,R,0),R,1); M=np.repeat(np.repeat(m,R,0),R,1); A=np.repeat(np.repeat(a,R,0),R,1)
H,W=-(-F.shape[0]//D), -(-F.shape[1]//D)
pad=lambda z,v: np.pad(z,((0,H*D-z.shape[0]),(0,W*D-z.shape[1]))+((0,0),)*(z.ndim-2),constant_values=v)
F,M,A=pad(F,0),pad(M,False),pad(A,0)
P=np.array(PAL[1:15],float); out=np.zeros((H,W),'uint8')
for j in range(H):
    for i in range(W):
        mm=M[j*D:(j+1)*D,i*D:(i+1)*D]
        if mm.mean()<0.4: continue
        c=F[j*D:(j+1)*D,i*D:(i+1)*D][mm]; ai=A[j*D:(j+1)*D,i*D:(i+1)*D][mm]
        dk=(ai==1)|(ai==12)
        col=c[dk].mean(0) if dk.mean()>=0.35 else c[~dk].mean(0)
        cand=[0]+list(range(10,14))   # zwart + groen
        out[j,i]=1+cand[int(np.argmin([((P[k]-col)**2).sum() for k in cand]))]
np.save('lijf_kaal.npy',out); print('lijf sprite',W,'x',H)
im=Image.fromarray(out,'P'); im.putpalette([v for c in PAL for v in c]); im.save('lijf_kaal.png',transparency=0)
Image.open('lijf_kaal.png').convert('RGBA').resize((W*16,H*16),Image.NEAREST).save('lijf_kaal_16x.png')
