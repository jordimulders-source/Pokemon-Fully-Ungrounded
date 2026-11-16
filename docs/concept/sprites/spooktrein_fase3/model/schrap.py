# Natief model (86x83 in 99x99) -> 64 breed door rijen/kolommen te schrappen die het meest op hun buur lijken (Gengas-methode).
# Elke overgebleven pixel is een echte modelpixel. Gebruik: python3 schrap.py [mindist]
from PIL import Image; import numpy as np, sys
md=int(sys.argv[1]) if len(sys.argv)>1 else 3
a=np.asarray(Image.open('natief.png').convert('RGB')).astype(int)
a=a[6:89,9:95]  # bbox
def kies(a,n,axis):
    A=a if axis==0 else a.transpose(1,0,2)
    cost=[np.abs(A[i]-A[i+1]).sum() for i in range(len(A)-1)]
    gekozen=[]
    for i in np.argsort(cost,kind='stable'):
        if all(abs(i-j)>=md for j in gekozen): gekozen.append(int(i))
        if len(gekozen)==n: break
    return sorted(gekozen)
cols=kies(a,a.shape[1]-64,1); b=np.delete(a,cols,1)
nr=a.shape[0]-round(a.shape[0]*64/a.shape[1]); rows=kies(b,nr,0); b=np.delete(b,rows,0)
print('kolommen',len(cols),cols,'\nrijen',len(rows),rows,b.shape)
c=np.full((64,64,3),255,'uint8'); oy=64-b.shape[0]; c[oy:,:]=b
Image.fromarray(c).save('model_64.png'); Image.fromarray(c).resize((512,512),Image.NEAREST).save('model_64_8x.png')
