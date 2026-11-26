import numpy as np; from PIL import Image
import maak4 as M4
M3=M4.M3; from palet import PAL
H,W=M3.H,M3.W; OX,OY=7,12
o=M4.maak(); np.save('r4.npy',o); r3=np.load('r3_E6.npy')
S=np.zeros((64,64),'uint8'); S[OY:OY+H,OX:OX+W]=o
im=Image.fromarray(S,'P'); im.putpalette([c for t in PAL for c in t]); im.save('poliwhirl_regional_r4.png',transparency=0)
d=o!=r3; Z=M3.M.OOGZ
print('diff r3_E6->r4: %d px, oogzone %d, ERBUITEN %d; kleuren %d'%(d.sum(),(d&Z).sum(),(d&~Z).sum(),len(np.unique(np.append(o,0)))))
for i in M3.INFO: print(i[0],i[1],'->',i[2],'px, plek x %d-%d y %d-%d'%i[4])
sil=(o>0)!=(r3>0); print('silhouetverschil',[(int(x),int(y)) for y,x in zip(*np.where(sil))])
# metingen sprite: oogmiddens, afstand, hoogte t.o.v. neusgaten (rij 8) en mond (rij 10), kopranden
def meet(a,boxes):
    out=[]
    for x0,x1,y0,y1 in boxes: out.append(((x0+x1+1)/2,(y0+y1+1)/2,x0,x1))   # celcoordinaten (pixel i = cel i..i+1)
    (lx,ly,l0,l1),(rx,ry,r0,r1)=out
    def span(y):
        row=a[y]; l=22
        while l-1>=0 and row[l-1]!=0 and not M3.V.crys[y,l-1]: l-=1
        r=22
        while r+1<W and row[r+1]!=0 and not M3.V.crys[y,r+1]: r+=1
        return l,r
    return dict(midden_l=(lx,ly),midden_r=(rx,ry),afstand=rx-lx,oogmidden_tot_neusgat=8.5-(ly+ry)/2,oogmidden_tot_mond=10.5-(ly+ry)/2,
                links_buiten_koprand_r8=span(8)[0]-l0,rechts_tot_rechterrand=span(int(round(ry)))[1]-r1)
print('r3_E6',meet(r3,[(14,19,3,8),(27,32,2,7)]))
print('r4   ',meet(o,[(13,18,2,7),(26,31,2,7)]))
