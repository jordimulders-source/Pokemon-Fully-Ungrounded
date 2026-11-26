# Kale reductie (SPRITE_KERN): vlakgemiddelde per spritepixel + dichtstbijzijnde paletkleur uit het model.
from bouw import *
af=a.astype(float); m=(~bg).astype(float)
num=np.stack([Wy@(af[:,:,c]*m)@Wx.T for c in range(3)],2)
den=(Wy@m@Wx.T)[:,:,None]
avg=num/np.maximum(den,1e-6)
pal=np.array(kaal.PAL[1:],float)
# kleurafstand met nadruk op helderheid
idx=((avg[:,:,None,:]-pal[None,None])**2).sum(3).argmin(2)+1
idx[~alpha]=0
out=idx.astype(np.uint8)
kaal.save(out,'kaal.png')
with open('kaal.txt','w') as f:
    for y in range(OH): f.write(''.join('.' if out[y,x]==0 else '0123456789abcdef'[out[y,x]] for x in range(OUTW))+'\n')
