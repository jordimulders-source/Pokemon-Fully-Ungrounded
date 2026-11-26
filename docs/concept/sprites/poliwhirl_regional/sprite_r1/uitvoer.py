# Uitvoer r1: vier 64x64-png's (geindexeerd, index 0 transparant), bewijs pixeldiff 0 buiten oog- en spiraalzone,
# afwijking per zone t.o.v. de kale reductie, kleurentelling.
import numpy as np; from PIL import Image
import varianten as V
from palet import PAL
OX,OY=7,12
H,W=V.H,V.W
R={}
for sv in 'ab':
    for ov in '12':
        o=V.maak(sv,ov); R[sv+ov]=o; np.save('r1_%s%s.npy'%(sv,ov),o)
        S=np.zeros((64,64),'uint8'); S[OY:OY+H,OX:OX+W]=o
        im=Image.fromarray(S,'P'); im.putpalette([c for t in PAL for c in t]); im.save('poliwhirl_regional_r1_%s%s.png'%(sv,ov),transparency=0)
# zones
jj,ii=np.mgrid[0:H,0:W]
OOG=((ii>=11)&(ii<=21)|(ii>=24)&(ii<=34))&(jj<=9)
SPI=V.buik&(jj>=17)&(jj<=30)&(ii>=16)&(ii<=30)
print('== bewijs: verschillen tussen de vier varianten')
ks=list(R)
for a in range(4):
    for b in range(a+1,4):
        d=R[ks[a]]!=R[ks[b]]
        print('%s-%s: totaal %3d, in oogzone %3d, in spiraalzone %3d, ERBUITEN %d'%(ks[a],ks[b],d.sum(),(d&OOG).sum(),(d&SPI).sum(),(d&~OOG&~SPI).sum()))
# afwijking t.o.v. de kale reductie
kaal=np.load('kaal.npy'); cls=V.cls
def mat(v): return {0:0,1:4,2:4,3:4,4:4,5:1,6:1,7:1,8:3,9:3,10:3,11:3,15:3,12:2,13:2,14:2}[int(v)]
Z=[('ogen',OOG),('spiraal',SPI),('mond',(jj>=9)&(jj<=12)&(ii>=14)&(ii<=31)),
   ('kristallen',V.crys|((ii==22)&(jj<=2))),('handschoenen',V.glove),('voeten',(jj>=39)),]
print('== afwijking t.o.v. kale reductie (kaal.npy): andere index / ander materiaal')
for k,o in R.items():
    M=np.vectorize(mat)(o); used=np.zeros((H,W),bool); s=[]
    for n,m in Z+[('rest (kop, lijf, armen, benen)',np.ones((H,W),bool))]:
        m=m&~used; used|=m
        t=(m&((o>0)|(kaal>0))).sum(); a=((o!=kaal)&m).sum(); b=((M!=cls)&m).sum()
        s.append('%s %d px: %d / %d'%(n,t,a,b))
    print(k,' | '.join(s))
    sil=((o>0)!=(kaal>0)); print('   silhouetverschil met de reductie: %d px'%sil.sum(), [(int(x),int(y)) for y,x in zip(*np.where(sil))])
    print('   kleuren incl. transparant:',len(np.unique(np.append(o.ravel(),0))))
