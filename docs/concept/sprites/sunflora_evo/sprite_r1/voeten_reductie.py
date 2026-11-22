# Hangende blad-voeten uit r5 (Jordi: "ik wil ze hangend"): natief r5 rijen 101-120, kol 107-138,
# vlakgemiddelde op lijfschaal (2/3)/2.6 = 0.256 spritepx per natieve cel; donkere lijn wint bij >=30%.
# Kleur: dichtstbijzijnde van zwart + Sunflora-groen (helderheid van het model -> groene tint). Niets getekend.
import numpy as np; from PIL import Image; from pal import PAL
a=np.asarray(Image.open('natief.png').convert('RGB')).astype(float)[101:121,107:139]
lum=a@[0.3,0.59,0.11]; g=(a[:,:,1]>a[:,:,0]+15); dk=lum<60; m=g|dk
R,D=10,39
F=np.repeat(np.repeat(lum,R,0),R,1); M=np.repeat(np.repeat(m,R,0),R,1); K=np.repeat(np.repeat(dk,R,0),R,1)
H,W=-(-F.shape[0]//D),-(-F.shape[1]//D)
pad=lambda z,v: np.pad(z,((0,H*D-z.shape[0]),(0,W*D-z.shape[1])),constant_values=v)
F,M,K=pad(F,255),pad(M,False),pad(K,False)
# modelgroen-helderheden -> Sunflora d/e/f (mediaan-gebaseerde drempels)
gl=lum[g&~dk]; t1,t2=np.percentile(gl,[30,75])
out=np.zeros((H,W),'uint8')
for j in range(H):
    for i in range(W):
        mm=M[j*D:(j+1)*D,i*D:(i+1)*D]
        if mm.mean()<0.4: continue
        kk=K[j*D:(j+1)*D,i*D:(i+1)*D][mm]
        if kk.mean()>=0.3: out[j,i]=1; continue
        l=F[j*D:(j+1)*D,i*D:(i+1)*D][mm&~K[j*D:(j+1)*D,i*D:(i+1)*D]].mean()
        out[j,i]=12 if l<t1 else (13 if l<t2 else 14)
np.save('voeten_kaal.npy',out)
ch='.123456789abcdef'; [print(''.join(ch[v] for v in r)) for r in out]
