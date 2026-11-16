# Bouwt de r1-basis: ijs-lijf (platen/naden, slak-indeling) + staart/punten/nevel uit het model.
# Daarna wordt r1.txt met de hand verder opgeschoond.
import numpy as np
from PIL import Image, ImageDraw
from gio import to_txt, CH
m=np.load('mask_v.npy').copy()
# onderkant volgens model (g6): rij 59 x13..26, rij 60 x16..24
m[59,:]=False; m[59,13:27]=True; m[60,:]=False; m[60,16:25]=True
np.save('mask_r1.npy',m)
I={c:k for k,c in enumerate(CH)}
G=np.full((64,64),-1)
# --- ijsgebied
poly=[(14,24),(19,24),(21,25),(22,26),(22,33),(21,34),(21,38),(23,40),(29,40),(31,42),(34,43),(35,45),(35,50),(34,53),(34,55),(32,57),(29,58),(26,59),(24,61),(16,61),(0,61),(0,28),(7,28),(9,27),(11,26),(13,25)]
im=Image.new('L',(64,64),0); ImageDraw.Draw(im).polygon(poly,fill=1,outline=1)
ice=(np.asarray(im)>0)&m
# --- model64 classificatie buiten het ijs
a=np.asarray(Image.open('model64.png')).astype(int); L=a.mean(2)
for y in range(64):
    for x in range(64):
        if not m[y,x] or ice[y,x]: continue
        r,g,b=a[y,x]; l=L[y,x]
        if l<62: c='i'
        elif l<100: c='i' if r<b-50 and l<80 else 'j'
        elif r>g+12 and l<200: c='v' if l>150 else 'n'
        elif l<150: c='D'
        elif l<200: c='M'
        elif b>r+22 and r<215: c='w'
        elif l<238: c='L'
        else: c='W'
        G[y,x]=I[c]
# --- ijs: vul eerst alles L
G[ice]=I['L']
np.save('ice_r1.npy',ice)
to_txt(G,'basis.txt')
