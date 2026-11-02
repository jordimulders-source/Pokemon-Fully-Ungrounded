"""Silhouet v3a: auto-silhouet (foto 1, korter lijf, kop 1,45x) + met de hand: open bedelbek, pootjes 2 px."""
from PIL import Image; import numpy as np
m=np.asarray(Image.open('silhouet_v3a_1x.png'))<128
m=m.copy()
m[22:31,8:19]=False   # oude bek weg (alles links van de kop)
def zet(y,x0,x1): m[y,x0:x1+1]=True
# bovensnavel schuin omhoog-links, 2 dik
for y,x0,x1 in [(23,11,12),(24,11,14),(25,13,16),(26,15,18),(27,17,19)]: zet(y,x0,x1)
# ondersnavel, bijna horizontaal, open gaap
for y,x0,x1 in [(28,18,19),(29,13,19),(30,12,16)]: zet(y,x0,x1)
# pootjes 2 px breed
for y in (52,53): m[y,31:33]=True; m[y,36:38]=True
m[53,36]=True
Image.fromarray((~m*255).astype('uint8')).save('silhouet_v3a_hand_1x.png')
for y in range(20,58): print('%2d'%y,''.join('#' if v else '.' for v in m[y,8:52]))
print(m.sum())
