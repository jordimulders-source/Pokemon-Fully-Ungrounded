# verre poten 3' en 4' (optie A): KOPIE van de nabije poot 3 en 4 (kabel, ring, klauwtjes) in schaduwtint,
# verschoven, alleen op lege pixels en niet tussen de klauwtjes van de nabije poot (geen dambord) (dus achter lijf en nabije poten). python3 verre.py NAAM dx3 dy3 dx4 dy4
import numpy as np, sys; from PIL import Image
from reduce_pal import PAL
naam=sys.argv[1]; dx3,dy3,dx4,dy4=map(int,sys.argv[2:6])
f=np.loadtxt('r5_basis_vol.txt',dtype=int); base=f.copy()
POOT={7,8,9,10,11,12,14,15}; S={7:7,8:7,9:8,10:11,11:12,12:12,14:15,15:15,1:1}
def masker(x0,x1,y0,y1):
    m=np.zeros_like(f,bool)
    for y in range(y0,y1+1):
        for x in range(x0,x1+1):
            v=base[y,x]
            if v in POOT: m[y,x]=True
            elif v==1 and any(base[y+a,x+b] in POOT for a,b in((1,0),(-1,0),(0,1),(0,-1))): m[y,x]=True
    return m
n=0
for (x0,x1,y0,y1),(dx,dy) in (((26,39,41,61),(dx3,dy3)),((39,50,43,60),(dx4,dy4))):
    m=masker(x0,x1,y0,y1)
    for y,x in zip(*np.where(m)):
        Y,X=y+dy,x+dx
        vlak=[base[Y+a,X+b] for a in (-1,0,1) for b in (-1,0,1) if 0<=Y+a<64 and 0<=X+b<64]
        if 0<=Y<64 and 0<=X<64 and base[Y,X]==0 and f[Y,X]==0 and not (14 in vlak or 15 in vlak): f[Y,X]=S[base[y,x]]; n+=1
np.savetxt(f'vlieg_r5_{naam}.txt',f,fmt='%2d')
im=Image.fromarray(f.astype('uint8'),'P'); im.putpalette([v for c in PAL for v in c]+[0]*(768-3*len(PAL)))
im.save(f'vlieg_r5_{naam}.png',transparency=0)
Image.fromarray(np.array(PAL)[f].astype('uint8')).resize((512,512),Image.NEAREST).save(f'vlieg_r5_{naam}_8x.png')
ys,xs=np.where(f>0); print(naam,(dx3,dy3,dx4,dy4),'zichtbare verre-pootpixels',n,'breed',xs.max()-xs.min()+1,'onderste rij',ys.max(),'kleuren',len(set(f.ravel()))-1)
