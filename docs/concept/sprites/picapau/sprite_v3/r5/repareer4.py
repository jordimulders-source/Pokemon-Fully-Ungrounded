# r4: 4 reparaties van de keurder (KEURING.md r3). Keurder-coordinaten = deze + (-5,+10).
import numpy as np
o=np.load('r3.npy').copy(); R=[]
def zet(z,l):
    for x,y,v in l: R.append((z,x,y,int(o[y,x]),v)); o[y,x]=v
zet('1 poot linkerrand (model: donkergrijze lijn links van de poot)',[(33,46,11),(33,47,11)])
zet('2 achterkuif onderste punt',[(40,17,1)])
zet('3 voet 1 rij omhoog (model: grijs r48.7-49.3, zwart r49.3-49.7, r50 leeg)',
    [(32,48,10),(33,48,10),(31,49,1),(32,49,1),(33,49,1),(34,49,1),(35,49,1)]+[(x,50,0) for x in range(31,37)])
zet('4 staartpunt',[(51,51,9),(50,50,8)])
np.save('r4.npy',o)
for r in R: print(r)
print('totaal',len(R))
