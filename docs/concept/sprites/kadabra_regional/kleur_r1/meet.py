# meet.py: model (100x100 cellen) -> meting per spritepixel (meet.npz).
# Geometrie: cel x 3..96 -> sprite x 1..62, cel y 10..91 -> sprite y 9..62 (schaal 31/47 = 0,66; 1 spritepixel = 1,516 cel).
import numpy as np
from collections import deque
C=np.load('cellen.npy'); L=C.mean(2)
CX0,CY0,SX0,SY0,SUB,BLK=3,10,1,9,31,47
def s2c(x,y): return CX0+(x-SX0)*BLK/SUB, CY0+(y-SY0)*BLK/SUB   # linkerbovenhoek van spritepixel in celcoordinaten
# achtergrond = wit (L>240) dat 4-verbonden is met de rand; wit binnenin (kaart, borst, buik, klauwen) hoort bij de figuur
bg=np.zeros((100,100),bool); q=deque([(0,0)]); bg[0,0]=1
while q:
    y,x=q.popleft()
    for dy,dx in((1,0),(-1,0),(0,1),(0,-1)):
        yy,xx=y+dy,x+dx
        if 0<=yy<100 and 0<=xx<100 and not bg[yy,xx] and L[yy,xx]>240: bg[yy,xx]=1; q.append((yy,xx))
fig=~bg
# gaten: ingesloten wit dat in het model achtergrond is (onder de duim van de open hand; tussen kaart en gebogen vingers)
fig[38:42,68:76]&=~(L[38:42,68:76]>222); fig[37,9:12]=False
if __name__=='__main__':
    def up(a):
        a=a[CY0:92,CX0:97]; a=np.repeat(np.repeat(a,SUB,0),SUB,1)
        pad=[(0,55*BLK-a.shape[0]),(0,0)]+[(0,0)]*(a.ndim-2); return np.pad(a,pad)
    def blk(a): return a.reshape(55,BLK,62,BLK).mean((1,3))
    F=up(fig.astype(float)); Lu=up(L); Cu=up(C.astype(float))
    neutral=up((C[...,2]-C[...,0]<14).astype(float))
    cov=blk(F); fo=blk(F*(Lu<20)); fk=blk(F*(Lu>=20)*(Lu<95)*neutral); fw=blk(F*(Lu>240)); fd=blk(F*(Lu>=20)*(Lu<118)*(1-neutral))
    red=up(((C[...,0]>C[...,2]+40)).astype(float)); fr=blk(F*red)
    med=np.zeros((55,62,3)); Fb=F.reshape(55,BLK,62,BLK).transpose(0,2,1,3).reshape(55,62,-1)
    Lb=Lu.reshape(55,BLK,62,BLK).transpose(0,2,1,3).reshape(55,62,-1)
    Cb=Cu.reshape(55,BLK,62,BLK,3).transpose(0,2,1,3,4).reshape(55,62,-1,3)
    for y in range(55):
        for x in range(62):
            m=(Fb[y,x]>0)&(Lb[y,x]>=20)
            if m.sum(): med[y,x]=np.median(Cb[y,x][m],0)
    def full(a):
        o=np.zeros((64,64)+a.shape[2:]); o[SY0:SY0+55,SX0:SX0+62]=a; return o
    np.savez('meet.npz',cov=full(cov),fo=full(fo),fk=full(fk),fw=full(fw),fr=full(fr),fd=full(fd),med=full(med),sil=full(cov)>=0.5)
    s=full(cov)>=0.5; ys,xs=np.where(s); print('box',xs.min(),xs.max(),ys.min(),ys.max(),xs.max()-xs.min()+1,ys.max()-ys.min()+1,'px',s.sum())
