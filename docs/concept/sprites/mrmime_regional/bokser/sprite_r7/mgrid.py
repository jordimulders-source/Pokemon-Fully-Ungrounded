# mgrid.py x0 y0 x1 y1: gemiddelde helderheid van het model per spritecel (zelfde mapping als zoom.py), als tabel /10
import sys,numpy as np; from PIL import Image
x0,y0,x1,y1=map(int,sys.argv[1:5])
m=np.asarray(Image.open('../r12.png').convert('L')).astype(float)
p=10.24; ph=10.25; s=88/63
X=lambda c:ph+(12+(c-10)*s)*p; Y=lambda r:ph+(5+r*s)*p
print('    '+' '.join('%2d'%x for x in range(x0,x1)))
for r in range(y0,y1):
    row=[]
    for c in range(x0,x1):
        a=m[int(Y(r)):int(Y(r+1)),int(X(c)):int(X(c+1))]; row.append('%2d'%min(99,round(a.mean()/2.56/1.01)) if a.size else ' ?')
    print('%2d  '%r+' '.join(row))
