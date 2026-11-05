"""Silhouet v3b: auto-silhouet (foto 5 bolletje) + met de hand: open bedelbek."""
from PIL import Image; import numpy as np
m=np.asarray(Image.open('silhouet_v3b_1x.png'))<128
m=m.copy()
m[28:33,10:19]=False; m[31,19:21]=False; m[32,19:22]=False
def zet(y,x0,x1): m[y,x0:x1+1]=True
for y,x0,x1 in [(25,13,14),(26,13,16),(27,15,18),(28,17,20),(29,19,26),(30,22,25)]: zet(y,x0,x1)
for y,x0,x1 in [(31,20,22),(32,14,22),(33,13,17)]: zet(y,x0,x1)
Image.fromarray((~m*255).astype('uint8')).save('silhouet_v3b_hand_1x.png')
for y in range(23,36): print('%2d'%y,''.join('#' if v else '.' for v in m[y,10:40]))
