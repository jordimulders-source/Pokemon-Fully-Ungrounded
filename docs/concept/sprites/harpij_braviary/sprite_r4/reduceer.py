# r4 stap 1: kale reductie van model_natief (bbox x24-81,y3-94) met factor 0,66, vlakgemiddelde + dichtstbijzijnde modelkleur.
# Twee varianten: puur gemiddelde (puur.npy) en met lijnregel (donker wint bij >=34% donker in het vak, zoals r1/kaal).
import numpy as np; from PIL import Image
a=np.asarray(Image.open('../model/model_natief.png').convert('RGB')).astype(float)
o=np.load('../sprite_r1/model_idx.npy'); pal=np.load('../sprite_r1/model_pal.npy')
o=o.copy()
# fout in r1-masker: de ingesloten witte achtergrond tussen de poten (78 px, y73-86 x47-56, min(rgb)>=248) telde als lijf
enc=np.zeros_like(o,bool); enc[73:87,47:57]=(a[73:87,47:57].min(2)>=248); o[enc]=0
np.save('model_idx_r4.npy',o)
A=a[3:95,24:82]; M=(o[3:95,24:82]>0).astype(float)
dark=(A.mean(2)<36).astype(float)*M
def wm(n,N):
    m=np.zeros((N,n)); s=n/N
    for j in range(N):
        a0,a1=j*s,(j+1)*s
        for i in range(int(a0),min(n,int(np.ceil(a1)))): m[j,i]=max(0,min(a1,i+1)-max(a0,i))
    return m
h,w=M.shape; H,W=int(round(h*.66)),int(round(w*.66)); Ry,Rx=wm(h,H),wm(w,W)
red=lambda im: np.einsum('yi,ijc,xj->yxc',Ry,im,Rx) if im.ndim==3 else Ry@im@Rx.T
area=Ry.sum(1)[:,None]*Rx.sum(1)[None]; cov=red(M)/area; dk=red(dark)/area
avg=red(A*M[:,:,None])/np.maximum(red(M),1e-6)[:,:,None]
C=np.vstack([pal,[[121,96,64],[151,131,88]]])
idx=((avg[:,:,None]-C[None,None])**2).sum(-1).argmin(-1)+1; idx[cov<.5]=0
puur=idx.copy(); lijn=idx.copy(); lijn[(dk>=.34)&(cov>=.5)]=1
np.save('puur.npy',puur); np.save('lijn.npy',lijn); np.save('avg.npy',avg); np.save('cov.npy',cov); np.save('pal18.npy',C)
k=np.load('../sprite_r1/kaal.npy'); print(H,W,'kaal==lijn:',(k!=lijn).sum(),'kaal vs puur:',(k!=puur).sum())
