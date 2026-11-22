# controle.py: alpha-diff t.o.v. r5, indexdiff in de ogen, lijnpixels (#) die van plek veranderden
import numpy as np; from PIL import Image
a=np.array(Image.open('vuurduivel_r6.png')); b=np.array(Image.open('../sprite_r5/vuurduivel_r5.png'))
print('alpha-diff', int(((a>0)!=(b>0)).sum()))
ogen=[(15,30,20,35),(23,28,29,35)]  # x0,y0,x1,y1 (excl.): lid, oogwit, pupil, glimpjes
print('ogen-diff', sum(int((a[y0:y1,x0:x1]!=b[y0:y1,x0:x1]).sum()) for x0,y0,x1,y1 in ogen))
weg=[(x,y) for y,x in zip(*np.where((b==1)&(a!=1)))]; bij=[(x,y) for y,x in zip(*np.where((a==1)&(b!=1)))]
print('lijn weg',weg,'lijn bij',bij)
print('kleuren',len(set(a.flatten())),'(incl. transparant)')
