# tx.py sprite.png [x0 y0 x1 y1]: sprite als tekstraster (index -> teken) voor gerichte reparaties
import sys, numpy as np; from PIL import Image
CH='.#sSb' + 'grR' + 'Bbl' + 'GHJ' + '*'   # 0 . | 1 # | 2 s(schorslijn) 3 S 4 b | 5 g(bladlijn) | 6 r 7 R 8 ? ...
CH='.#sTtgrRPuUWdmlh'
o=np.asarray(Image.open(sys.argv[1])).astype(int)
x0,y0,x1,y1=(map(int,sys.argv[2:6]) if len(sys.argv)>5 else (0,0,64,64))
print('    '+''.join(str(x%10) for x in range(x0,x1)))
for y in range(y0,y1): print('%2d  '%y+''.join(CH[o[y,x]] for x in range(x0,x1)))
