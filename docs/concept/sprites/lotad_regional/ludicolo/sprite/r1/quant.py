# Natief model (100x100) -> paletindex per modelpixel (kwant.npy), via de k-means-labels (kmeans.py 18, seed 1).
# Elke cluster gaat naar één paletindex (zie gemeen.py); geen middeling, geen nieuwe tinten. Ingesloten wit -> 15.
import numpy as np
lab=np.load('kmeans_lab.npy'); C=np.load('kmeans_C.npy')
def L(c): return 0.3*c[0]+0.59*c[1]+0.11*c[2]
# toewijzing op modelkleur (robuust tegen clustervolgorde)
REG=[((2,1,1),1),((50,35,23),8),((72,63,42),9),((88,83,53),10),((137,128,79),11),
     ((111,51,38),2),((126,57,43),2),((138,62,45),3),((149,68,47),4),((158,72,51),4),
     ((178,87,61),5),((188,94,67),5),((202,110,82),6),((208,120,90),6),((214,122,91),6),((206,138,102),7),
     ((193,143,41),12),((240,200,73),13)]
m={}
for k,c in enumerate(C):
    d=[sum((c[i]-r[i])**2 for i in range(3)) for r,_ in REG]; m[k]=REG[int(np.argmin(d))][1]
    print(k,tuple(int(v) for v in c),'->',m[k])
q=np.zeros(lab.shape,int)
for k,v in m.items(): q[lab==k]=v
H,W=q.shape; bg=q==0; uit=np.zeros_like(bg); st=[(0,0)]
while st:
    y,x=st.pop()
    if 0<=y<H and 0<=x<W and bg[y,x] and not uit[y,x]: uit[y,x]=1; st+=[(y+1,x),(y-1,x),(y,x+1),(y,x-1)]
gat=bg&~uit; print('ingesloten achtergrond',gat.sum(),list(zip(*np.where(gat))))
q[gat]=15; np.save('kwant.npy',q)
