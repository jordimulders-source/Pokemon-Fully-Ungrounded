# Lijnkaart op het natieve model: scheidingslijnen (donkerder dan de omgeving) en lichte strepen in vleugels/lijf
import numpy as np; from PIL import Image
N=np.asarray(Image.open('natief.png').convert('RGB')).astype(float); L=N.mean(2)
Z=np.load('zones_nat.npy'); fg=Z!='.'; H,W=L.shape
def boxmean(a,m,r):
    P=np.pad(a*m,r); Q=np.pad(m.astype(float),r); s=np.zeros_like(a); c=np.zeros_like(a)
    for dy in range(-r,r+1):
        for dx in range(-r,r+1):
            s+=P[r+dy:r+dy+H,r+dx:r+dx+W]; c+=Q[r+dy:r+dy+H,r+dx:r+dx+W]
    return s/np.maximum(c,1e-6)
veer=np.isin(Z,['M','W','D','K'])
loc=boxmean(L,veer,3)
lijn=veer&(L<loc-14)&(L<loc*0.72)
# rand van het silhouet hoort niet bij de binnenlijnen (buitenlijn komt later)
bg=~fg; rand=np.zeros_like(fg)
for dy in (-2,-1,0,1,2):
    for dx in (-2,-1,0,1,2): rand|=np.roll(np.roll(bg,dy,0),dx,1)
lijn&=~rand
streep=np.isin(Z,['W','M'])&(L>loc+30)&(L>=140)
np.save('lijn_nat.npy',lijn); np.save('streep_nat.npy',streep); np.save('loc_nat.npy',loc)
im=N.copy(); im[lijn]=(255,0,0); im[streep]=(0,255,255)
Image.fromarray(im.astype('uint8')).resize((800,800),Image.NEAREST).save('lijnkaart.png')
print(lijn.sum(),streep.sum())
