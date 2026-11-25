# Natief model (100x100) -> paletindex per modelpixel (kwant.npy). Elke pixel krijgt de dichtstbijzijnde modelkleur uit het palet.
# Snavel (alle geel/oranje, k2/k3/k15) binnen het snavelvak x30-48, y38-48 -> 16 (wordt vervangen door de Lombre-mond);
# hetzelfde geel buiten het snavelvak (nagels in de vuisten) -> Lotad-snaveltinten 13 (licht) / 12 (donkerder).
# Oogwit: crème pixels in het oogvak -> 11; door de figuur ingesloten witte pixels (nabij oog 12 px, ver oog 1 px) -> 15 wit.
import numpy as np; from PIL import Image
from gemeen import PAL
a=np.asarray(Image.open('natief.png')).astype(float); H,W,_=a.shape
fig=a.min(2)<232
# kandidaten: modelclusters (incl. de geel/oranje snaveltinten), elk met de paletindex waar ze heen gaan
CL=[((1,1,0),1),((4,3,2),1),((41,30,19),6),((50,41,24),6),((72,42,24),2),((106,43,27),2),((134,56,37),2),((159,69,46),3),
    ((201,111,77),4),((211,125,90),5),((80,69,45),7),((100,87,50),7),((118,99,65),8),((145,130,78),9),((174,157,100),10),
    ((149,106,34),16),((205,156,59),16),((236,198,103),16)]
C=np.array([c for c,_ in CL],float); IX=np.array([k for _,k in CL])
d=((a[:,:,None,:]-C[None,None])**2).sum(3); q=IX[d.argmin(2)]; q[~fig]=0
# oogwit: crème pixels (L>170, weinig verzadiging) in het oogvak x44-52, y36-41
L=0.3*a[...,0]+0.59*a[...,1]+0.11*a[...,2]; sat=a.max(2)-a.min(2)
yy,xx=np.mgrid[0:H,0:W]; ogw=fig&(L>170)&(sat<80)&(xx>=44)&(xx<=52)&(yy>=36)&(yy<=41); q[ogw]=11
snv=(xx>=30)&(xx<=48)&(yy>=38)&(yy<=48)
geel=q==16; q[geel&~snv&(L>=170)]=13; q[geel&~snv&(L<170)]=12
bg=q==0; uit=np.zeros_like(bg); st=[(0,0)]
while st:
    y,x=st.pop()
    if 0<=y<H and 0<=x<W and bg[y,x] and not uit[y,x]: uit[y,x]=1; st+=[(y+1,x),(y-1,x),(y,x+1),(y,x-1)]
gat=bg&~uit; q[gat]=15; print('ingesloten wit',gat.sum(),'nagels',(geel&~snv).sum())
np.save('kwant.npy',q); print('oogwit px',ogw.sum(),'snavel px',(q==15).sum())
