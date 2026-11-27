"""Raster van een icoon als tekst (index in hex, kolomliniaal). python3 toon.py icon.png [y0 y1]"""
import sys,numpy as np
from PIL import Image
a=np.array(Image.open(sys.argv[1])); y0,y1=(int(sys.argv[2]),int(sys.argv[3])) if len(sys.argv)>3 else (0,a.shape[0])
print('   '+''.join(str(x//10) for x in range(32))); print('   '+''.join(str(x%10) for x in range(32)))
for y in range(y0,y1): print('%2d|'%y+''.join('0123456789ABCDEF'[v] if v else '.' for v in a[y]))
