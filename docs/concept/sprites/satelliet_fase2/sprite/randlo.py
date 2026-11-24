# r4: paarse binnenrand links onder aan het grote paneel (rijen 34-44, model #705090 = 7). Per rij vanaf links: na de omlijning
# de eerste pixel naar binnen; als het modelblok daar >= 0,25 randklasse (6/7/8/15) heeft -> 7. Is dat een tweede omlijningspixel,
# dan kost dat 1 omlijningspixel aan de binnenkant (toegestaan door de coordinator).
import numpy as np, sys
from cfg import oudrij, oudkol, TOP
o=np.load(sys.argv[1]).copy(); F=np.load(sys.argv[2]); UIT=sys.argv[3]; ch=[]
from cfg import M, MODEL
from PIL import Image
Z=np.array(Image.open('zones.png'))
OUD=MODEL.endswith('/model.png')
rijen=range(oudrij(35),oudrij(45)) if OUD else [j for j in range(o.shape[0]) if M(0,j+.5)[1]>=650]   # r5: alle rijen onder de lijfonderkant (model y >= 650)
for j in rijen:
    i=oudkol(20)
    while i<oudkol(40) and o[j,i]==0: i+=1
    if i>=oudkol(40) or o[j,i]!=1: continue
    mx,my=M(i+.5,j+.5)
    if not OUD and Z[int(my),int(mx)]!=2: continue
    i+=1
    if o[j,i]==1 and F[j,i][[6,7,8,15]].sum()>=0.25: o[j,i]=7; ch.append((i,j+TOP,'omlijning')); continue
    while o[j,i]==1: i+=1
    if o[j,i] in (9,15) and F[j,i][[6,7,8,15]].sum()>=0.25: ch.append((i,j+TOP,int(o[j,i]))); o[j,i]=7
np.save(UIT,o); print('randlo -> 7:',ch)
