# r4: paarse binnenrand links onder aan het grote paneel (rijen 34-44, model #705090 = 7). Per rij vanaf links: na de omlijning
# de eerste pixel naar binnen; als het modelblok daar >= 0,25 randklasse (6/7/8/15) heeft -> 7. Is dat een tweede omlijningspixel,
# dan kost dat 1 omlijningspixel aan de binnenkant (toegestaan door de coordinator).
import numpy as np, sys
o=np.load(sys.argv[1]).copy(); F=np.load(sys.argv[2]); UIT=sys.argv[3]; ch=[]
for j in range(35,45):
    i=20
    while i<40 and o[j,i]==0: i+=1
    if i>=40 or o[j,i]!=1: continue
    i+=1
    if o[j,i]==1 and F[j,i][[6,7,8,15]].sum()>=0.25: o[j,i]=7; ch.append((i,j+7,'omlijning')); continue
    while o[j,i]==1: i+=1
    if o[j,i] in (9,15) and F[j,i][[6,7,8,15]].sum()>=0.25: ch.append((i,j+7,int(o[j,i]))); o[j,i]=7
np.save(UIT,o); print('randlo -> 7:',ch)
