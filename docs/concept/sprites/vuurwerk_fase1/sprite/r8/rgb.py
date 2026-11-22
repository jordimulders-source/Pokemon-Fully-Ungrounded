# Meting: mediaan model-RGB per spritepixel (hex)
import sys,numpy as np; from PIL import Image
F,OX,OY=2.4,76.6,14.6
M=np.asarray(Image.open('../../referenties/model.png').convert('RGB'))
fx=lambda v:(OX+F*v)*5.12-0.42; fy=lambda v:(OY+F*v)*5.12-0.42
r0,r1,c0,c1=map(int,sys.argv[1:5])
for j in range(r0,r1):
    s=[]
    for i in range(c0,c1):
        b=M[round(fy(j)):round(fy(j+1)),round(fx(i)):round(fx(i+1))].reshape(-1,3)
        s.append('%02x%02x%02x'%tuple(np.median(b,0).astype(int)))
    print('%3d '%j+' '.join(s))
