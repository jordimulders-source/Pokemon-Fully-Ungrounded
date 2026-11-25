import numpy as np; from PIL import Image
import varianten as V
from palet import PAL
OX,OY=1,2
H,W=V.H,V.W; R={}
for ov in ('O1','O2'):
    for sv in ('S1','S2'):
        o=V.maak(sv,ov); R[ov+sv]=o; np.save('r1_%s%s.npy'%(ov,sv),o)
        S=np.zeros((64,64),'uint8'); S[OY:OY+H,OX:OX+W]=o
        im=Image.fromarray(S,'P'); im.putpalette([c for t in PAL for c in t]); im.save('poliwrath_regional_r1_%s%s.png'%(ov,sv),transparency=0)
jj,ii=V.jj,V.ii
OOG=(jj>=3)&(jj<=11)&(((ii>=14)&(ii<=23))|((ii>=31)&(ii<=42)))
SPI=V.SPZ
ks=list(R); print('== verschillen tussen varianten')
for a in range(4):
    for b in range(a+1,4):
        d=R[ks[a]]!=R[ks[b]]
        print('%s-%s: totaal %3d, oogzone %3d, spiraalzone %3d, ERBUITEN %d'%(ks[a],ks[b],d.sum(),(d&OOG).sum(),(d&SPI).sum(),(d&~OOG&~SPI).sum()))
# afwijking t.o.v. de kale reductie: kaal = per cel modeltint zonder gladstrijken en zonder omlijning
from mat import mat as cls, L as lum
kaal=np.zeros((H,W),'uint8')
K=cls==4;Y=cls==1;I=cls==3;Rd=cls==2
kaal[K]=np.select([lum[K]>=56,lum[K]>=30],[4,3],2); kaal[Y]=np.select([lum[Y]>=196,lum[Y]>=156],[5,6],7)
kaal[I]=np.select([lum[I]>=222,lum[I]>=195,lum[I]>=150],[8,9,10],11); kaal[Rd]=np.select([lum[Rd]>=125,lum[Rd]>=92],[12,13],14)
np.save('kaal.npy',kaal)
def m_(v): return {0:0,1:4,2:4,3:4,4:4,5:1,6:1,7:1,8:3,9:3,10:3,11:3,15:3,12:2,13:2,14:2}[int(v)]
MOND=(jj>=12)&(jj<=17)&(ii>=14)&(ii<=42)
Z=[('ogen',OOG),('spiraal',SPI),('mond',MOND),('rest',np.ones((H,W),bool))]
print('== afwijking t.o.v. kale reductie: andere index / ander materiaal (omlijning telt als ander materiaal bij 1)')
for k,o in R.items():
    M=np.vectorize(m_)(o); used=np.zeros((H,W),bool); s=[]
    for n,m in Z:
        m=m&~used; used|=m
        a=((o!=kaal)&m).sum(); b=((M!=cls)&m).sum(); bo=((M!=cls)&m&(o!=1)).sum()
        s.append('%s: %d / %d (zonder omlijning %d)'%(n,a,b,bo))
    print(k,' | '.join(s))
    sil=((o>0)!=(kaal>0)); print('   silhouetverschil:',sil.sum(),[(int(x),int(y)) for y,x in zip(*np.where(sil))])
    rest=(M!=cls)&(o!=1)&~OOG&~SPI&~MOND; print('   ander materiaal (niet omlijning) buiten ogen/spiraal/mond:',[(int(x),int(y),int(o[y,x])) for y,x in zip(*np.where(rest))])
