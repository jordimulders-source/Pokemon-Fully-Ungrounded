"""Stap 2: onderlaag naar overworldmaat. Icoon is 22 hoog (y8-29); doel 21 (0,43 x front 49).
Alles boven de poten (icoonrij <=24) 1 rij omlaag; de middelste pootrij (icoonrij 27) vervalt, dus de poten worden 1 px korter
(OW-viervoeters hebben korte pootjes, 2-4 rijen). Onderkant blijft y29."""
import sys,os,numpy as np
sys.path.insert(0,os.path.dirname(__file__)); from ow_pal import *
W=os.path.join(os.path.dirname(__file__),'../werk/')
a=parse(open(W+'opzij_onderlaag.txt').read())
b=np.zeros_like(a)
for y in range(32):
    if y<=24: b[y+1]=a[y]
b[26]=a[25]; b[27]=a[26]; b[28]=a[28]; b[29]=a[29]
open(W+'opzij_geschoven.txt','w').write(totext(b)+'\n'); print(totext(b))
