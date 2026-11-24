# Natief raster -> r4-palet (dichtstbijzijnde kleur; iris apart op roodverzadiging). Niets getekend.
import numpy as np; from PIL import Image
N=np.load('natief.npy'); bg=np.load('natief_bg.npy')
PAL=np.array([(0,0,0),(24,16,16),(60,22,28),(88,32,34),(138,56,50),(182,86,76),(204,108,92),(214,122,102),
              (168,20,24),(222,50,44),(236,128,112)],float)
q=np.zeros((64,64),int)
for j,i in zip(*np.where(~bg)):
    c=N[j,i]; r,g,b=c
    ids=[8,9,10] if (r-g>120) else [1,2,3,4,5,7]
    q[j,i]=ids[int(np.argmin([((PAL[k]-c)**2).sum() for k in ids]))]
# oog: alles binnen de zwarte oogring met de irispaletkleuren (hooglicht en donkere iris zijn rood, geen steen)
from scipy import ndimage
b=np.zeros((64,64),bool); b[20:37,27:42]=True
ring=(q==1)&b; inside=ndimage.binary_fill_holes(ring)&~ring
for j,i in zip(*np.where(inside)):
    c=N[j,i]; q[j,i]=[8,9,10][int(np.argmin([((PAL[k]-c)**2).sum() for k in [8,9,10]]))]
np.save('oog_natief.npy',inside)
np.save('q.npy',q)

