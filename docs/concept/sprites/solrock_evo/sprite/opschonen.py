# Technisch opschonen van de kale reductie: losse lijnstukjes en tintvlekjes < 3 px nemen de buurtint aan
# (binnen dezelfde kleurgroep). Geen nieuwe vormen. In: kaal.npy  Uit: schoon.npy
import numpy as np; from scipy import ndimage as nd
o=np.load('kaal.npy'); o0=o.copy()
GRP={2:'g',3:'g',4:'g',7:'p',8:'p',9:'p'}
def comps(mask):
    lab,n=nd.label(mask,structure=np.ones((3,3))); return lab,n
def buur(o,j,i,ok):
    vals=[o[y,x] for y in range(j-1,j+2) for x in range(i-1,i+2) if (y,x)!=(j,i) and 0<=y<64 and 0<=x<64 and o[y,x] in ok]
    return max(set(vals),key=vals.count) if vals else None
# 1. bruine plaatlijnen: componenten < 3 px weg (-> plaattint van de buren)
lab,n=comps(o==10)
for k in range(1,n+1):
    m=lab==k
    if m.sum()<3:
        for j,i in zip(*np.where(m)):
            v=buur(o,j,i,[7,8,9]); o[j,i]=v if v else 9
# 2. losse zwarte pixels midden in de kern (alle 8 buren grijs) -> G1
for j in range(1,63):
    for i in range(1,63):
        if o[j,i]==1:
            nb=o[j-1:j+2,i-1:i+2].ravel()
            if all(v in (2,3,4) for k,v in enumerate(nb) if k!=4): o[j,i]=2
# 3. tintvlekjes < 3 px per kleurgroep (2 passes)
for _ in range(2):
    for t in (2,3,4,7,8,9):
        lab,n=nd.label(o==t)   # 4-buren
        for k in range(1,n+1):
            m=lab==k
            if m.sum()<3:
                for j,i in zip(*np.where(m)):
                    ok=[v for v in GRP if GRP[v]==GRP[t] and v!=t]
                    v=buur(o,j,i,ok)
                    if v: o[j,i]=v
# 4. binnenlijnen in de plaat (niet grenzend aan kern/zwart) in de donkere plaattint i.p.v. bijna-zwart bruin (Gen 3: binnenlijn = donkere tint van het vlak)
o2=o.copy()
for j,i in zip(*np.where(o==10)):
    nb=o[max(0,j-1):j+2,max(0,i-1):i+2]
    if not np.isin(nb,[0,1,2,3,4]).any(): o2[j,i]=9
o=o2
np.save('schoon.npy',o)
print('gewijzigd t.o.v. kaal:',(o!=o0).sum())
