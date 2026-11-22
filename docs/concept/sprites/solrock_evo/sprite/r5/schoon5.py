# Technisch opschonen van het r5-gezicht (alleen binnen de plaat):
# 1. bruine lijnpixels (10/9) die geen lijn vormen (8-component < 3) -> buurplaattint
# 2. barstlijnen in het plaatvlak (niet aan zwart/kern) in P3 = de modelkleur van de barsten (142,89,36); P4 alleen langs zwart/kern en in de ooglidcontour
# 3. losse P1/P2-vlekjes < 3 px (4-component) -> buurtint
import numpy as np, sys; from scipy import ndimage as nd
sys.path.insert(0,'..'); from npy2png import save
o=np.load('gezicht.npy'); o0=o.copy(); r4=np.load('../r4/sprite.npy')
ZONE=np.zeros((64,64),bool); ZONE[21:47,14:37]=True
OOGBLOK=np.zeros_like(ZONE); OOGBLOK[28:37,16:24]=True; OOGBLOK[29:39,25:34]=True
def buur(j,i,ok):
    v=[o[y,x] for y in range(j-1,j+2) for x in range(i-1,i+2) if (y,x)!=(j,i) and o[y,x] in ok]
    return max(set(v),key=v.count) if v else None
lijn=np.isin(o,[9,10])&ZONE
lab,n=nd.label(lijn,structure=np.ones((3,3)))
for k in range(1,n+1):
    m=lab==k
    if m.sum()<3:
        for j,i in zip(*np.where(m)):
            b=buur(j,i,[7,8,13]);
            if b: o[j,i]=b
for j,i in zip(*np.where((o==10)&ZONE&~OOGBLOK)):
    nb=o[j-1:j+2,i-1:i+2]
    if not np.isin(nb,[1,2,3,4]).any(): o[j,i]=9
for _ in range(2):
    for t in (7,8,9,13):
        lab,n=nd.label((o==t)&ZONE)
        for k in range(1,n+1):
            m=lab==k
            if m.sum()<3 and not (m&OOGBLOK).any():
                for j,i in zip(*np.where(m)):
                    b=buur(j,i,[x for x in (7,8,9,13) if x!=t])
                    if b: o[j,i]=b
print('opgeschoond:',int((o!=o0).sum()))
np.save('schoon5.npy',o)
