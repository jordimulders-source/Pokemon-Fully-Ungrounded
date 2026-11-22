# zones_n.py: natief model (natief.png, 100x100) -> familie per pixel + onderdeel (zone). Schrijft natief_fam.npy, natief_zone.npy, print kaart.
# families: 0 achtergrond, 1 lijn (zwart), 2 lav, 3 roze, 4 blauw, 5 creme
# zones: 0 achter, 1 muts, 2 neus, 3 snor L, 4 snor R, 5 lijf (roze), 6 arm L, 7 arm R, 8 broek, 9 been/voet L, 10 been/voet R
import numpy as np; from PIL import Image
a=np.asarray(Image.open('natief.png')).astype(float)
REF={1:[(0,0,0),(84,70,108),(140,105,114),(132,42,60)],2:[(120,100,144),(144,120,168),(186,162,204),(204,180,222)],
     3:[(208,100,120),(240,150,160),(246,180,190)],
     4:[(55,75,135),(90,141,188),(126,180,220),(149,196,229)],5:[(206,198,165),(240,234,216)]}
fam=np.zeros((100,100),int)
for y in range(100):
    for x in range(100):
        c=a[y,x]
        if c.min()>=235: continue
        best=min(((((c-np.array(r))**2).sum(),f) for f,rs in REF.items() for r in rs)); fam[y,x]=best[1]
z=np.zeros((100,100),int)
for y,x in zip(*np.where(fam>1)):
    f=fam[y,x]
    if f==2: z[y,x]=1
    elif f==5: z[y,x]=3 if x<52 else 4
    elif f==4:
        if y>=74 or (y>=71 and x<36+2*(y-71)): z[y,x]=9 if x<50 else 10
        else: z[y,x]=8
    elif f==3:
        if y<=49 and 28<=x<=46: z[y,x]=2
        elif x<=28 and y>=55: z[y,x]=6
        elif x>=66 and y>=56: z[y,x]=7
        else: z[y,x]=5
# lijnpixels (fam 1) -> zone van de voorste buur (2 rondes, voor dubbele lijnen)
PRIO=[1,2,3,4,6,7,9,10,8,5]
for _ in range(3):
    z0=z.copy()
    for y,x in zip(*np.where((fam==1)&(z0==0))):
        b=set(z0[y-1:y+2,x-1:x+2].ravel())-{0}
        for p in PRIO:
            if p in b: z[y,x]=p; break
np.save('natief_fam.npy',fam); np.save('natief_zone.npy',z)
CH='.MNstLlrBvw'
for y in range(14,86): print('%2d '%y+''.join((CH[z[y,x]].lower() if fam[y,x]==1 else CH[z[y,x]]) for x in range(12,92)))
