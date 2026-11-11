import sys
from PIL import Image
import numpy as np
src,dst,gridf=sys.argv[1],sys.argv[2],sys.argv[3]
im=Image.open(src).convert('RGB'); a=np.asarray(im).copy()
P=14.6; I0,J0=54,20
def cell(i,j):
    x0,y0=int(i*P),int(j*P); b=a[y0+3:y0+int(P)-3,x0+3:x0+int(P)-3].reshape(-1,3); return np.median(b,0)
# kleuren uit het model zelf
C={'.':(255,255,255),'o':(20,18,26)}
C['a']=(206,204,218)
C['b']=tuple(int(v) for v in cell(60,28))
C['c']=tuple(int(v) for v in cell(61,30))
C['d']=tuple(int(v) for v in cell(62,30))
C['k']=None  # laten staan
C['w']=(236,236,242)
rows=[l.rstrip('\n') for l in open(gridf) if l.strip() and not l.startswith('#')]
for dj,r in enumerate(rows):
    for di,ch in enumerate(r):
        if ch in 'k=': continue
        i,j=I0+di,J0+dj; x0,y0=int(round(i*P)),int(round(j*P)); x1,y1=int(round((i+1)*P)),int(round((j+1)*P))
        a[y0:y1,x0:x1]=C[ch]
Image.fromarray(a).save(dst)
print(C)
