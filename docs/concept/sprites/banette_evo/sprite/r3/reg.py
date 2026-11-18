# Registratietest: modeldekking (niet-wit) en modelzwart per spritepixel bij verschuiving (dx,dy); vergelijk met sprite
import numpy as np; from PIL import Image
a=np.asarray(Image.open('../../model/model.png').convert('RGB')).astype(float); L=a.sum(2)/3
fg=(a.min(2)<235).astype(float); blk=(L<60).astype(float)
g=np.load('r2.npy'); S=968/62
def grid(M,dx,dy):
    o=np.zeros((64,64))
    for j in range(64):
        for i in range(64):
            xa,ya=24+(i-1+dx)*S,1+(j-4+dy)*S
            b=M[max(0,int(round(ya))):max(0,int(round(ya+S))),max(0,int(round(xa))):max(0,int(round(xa+S)))]
            o[j,i]=b.mean() if b.size else 0
    return o
f=(g>0).astype(float); k=(g==1).astype(float)
for dy in np.arange(-1,1.01,0.25):
  for dx in (-0.25,0,0.25):
    F=grid(fg,dx,dy); B=grid(blk,dx,dy)
    print('dx %5.2f dy %5.2f  silhouet-IoU %.3f  zwart-corr %.3f'%(dx,dy,((F>=.5)&(f>0)).sum()/((F>=.5)|(f>0)).sum(),np.corrcoef(B.ravel(),k.ravel())[0,1]))
print('per zone (beste dy voor zwart-corr):')
for nm,(x0,y0,x1,y1) in {'ogen':(14,22,38,32),'bel L':(4,32,12,40),'bel R':(48,16,56,24),'kruis L':(0,15,12,28),'kruis R':(48,12,64,28),'Shuppet R':(46,42,62,62)}.items():
    res=[]
    for dy in np.arange(-1,1.01,0.1):
        F=grid(fg,0,dy)[y0:y1,x0:x1]; f2=f[y0:y1,x0:x1]
        res.append((((F>=.5)&(f2>0)).sum()/((F>=.5)|(f2>0)).sum(),round(dy,1)))
    print(nm,sorted(res)[-3:])
