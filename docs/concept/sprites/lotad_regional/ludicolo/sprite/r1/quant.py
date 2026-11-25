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
q[gat]=15
# Context: de donkere olijf-clusters (50,35,23) en (72,63,42) komen ook voor als donkerbruine lijnpixels in het rode lijf/de poncho.
# Is in een 5x5-venster het rood (2-7) duidelijk in de meerderheid (>= 3x olijf 10/11), dan is het een lijn van het rode deel:
# (50,35,23) -> zwart (1), (72,63,42) -> rode lijn (2). Niet in het gezicht (oogmasker).
q0=q.copy(); n=0
for y,x in zip(*np.where(np.isin(q0,[8,9]))):
    if y<=42: continue   # oogmasker (olijf rond de ogen, natief rij 33-42) blijft olijf
    w=q0[max(0,y-2):y+3,max(0,x-2):x+3]; r=np.isin(w,[2,3,4,5,6,7]).sum(); o=np.isin(w,[10,11]).sum()
    if r>=3*max(o,1) and o<=2: q[y,x]=1 if q0[y,x]==8 else 2; n+=1
print('olijf-lijnpixels in rood omgezet',n)
np.save('kwant.npy',q)
