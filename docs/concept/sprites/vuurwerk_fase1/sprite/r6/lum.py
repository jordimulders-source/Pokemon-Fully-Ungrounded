# Meting: gemiddelde modelhelderheid (0-99) per spritepixel, alleen dekkende pixels; '..' = leeg
import sys,numpy as np; from PIL import Image
F,OX,OY=2.4,76.6,14.6
M=np.asarray(Image.open('../../referenties/model.png').convert('RGB')).astype(float)
L=0.3*M[...,0]+0.59*M[...,1]+0.11*M[...,2]
fx=lambda v:(OX+F*v)*5.12-0.42
r0,r1,c0,c1=map(int,sys.argv[1:5])
print('    '+''.join('%3d'%c for c in range(c0,c1)))
for j in range(r0,r1):
    s=''
    for i in range(c0,c1):
        b=L[round(fx(j)-0.0+ (OY-OX)*5.12):,:][:1] if False else L[round((OY+F*j)*5.12):round((OY+F*(j+1))*5.12), round(fx(i)):round(fx(i+1))]
        s+='%3d'%min(99,int(b.mean()/2.56))
    print('%3d '%j+s)
