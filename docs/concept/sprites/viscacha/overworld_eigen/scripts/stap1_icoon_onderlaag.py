"""Stap 1: icoon frame 1 -> onderlaag opzij in het frontpalet (kleurmapping, verder niets).
Icoonindex -> OW-index: 15/14 (omlijning) -> 2, 7 (zand) -> 6, 6 (bruin) -> 5, 8 goud -> a, 9 geel -> b, 3 wit -> e."""
import sys,os,numpy as np
from PIL import Image
sys.path.insert(0,os.path.dirname(__file__)); from ow_pal import *
R=os.path.abspath(os.path.join(os.path.dirname(__file__),'../../../../../..'))
a=np.array(Image.open(R+'/docs/concept/sprites/viscacha/icoon/af/icon.png'))[:32]
m={15:2,14:2,7:6,6:5,8:10,9:11,3:14}
b=np.vectorize(lambda v:m.get(int(v),0))(a).astype(np.uint8)
open(os.path.join(os.path.dirname(__file__),'../werk/opzij_onderlaag.txt'),'w').write(totext(b)+'\n')
print(totext(b))
