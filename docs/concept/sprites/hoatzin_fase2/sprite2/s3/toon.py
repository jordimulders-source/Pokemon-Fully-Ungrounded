# toon.py: tekstkaart van onderlaag (zone-letters; kleine letter alpha>=0.45, punt = laag aandeel)
import numpy as np, sys
from klassen import ZONE
k=np.load('onderlaag.npy'); a=np.load('alpha.npy'); fr=np.load('frac.npy')
Z={'vleugel':'v','creme':'c','krop':'p','kuif':'k','blauw':'b','oog':'o','grijs':'g','lijn':'#'}
y0,y1,x0,x1=[int(v) for v in sys.argv[1:5]] if len(sys.argv)>4 else (0,64,0,64)
for j in range(y0,y1):
  r=''
  for i in range(x0,x1):
    if a[j,i]<0.12: r+=' '; continue
    ch=Z[ZONE[k[j,i]]]
    r+= ch if a[j,i]>=0.45 else ch.upper()
  print('%2d'%j,r)
