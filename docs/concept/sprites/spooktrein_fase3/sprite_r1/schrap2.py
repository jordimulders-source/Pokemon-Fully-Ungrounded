# Variant op model/schrap.py: zelfde schrapmethode (alleen hele rijen/kolommen weg, geen resamplen),
# maar met gewicht per zone zodat ogen, mond en kleine geest minder geschrapt worden.
# Gebruik: python3 schrap2.py WF WG out.png   (WF = gewicht gezicht, WG = gewicht kleine geest)
from PIL import Image; import numpy as np, sys
WF=float(sys.argv[1]); WG=float(sys.argv[2]); OUT=sys.argv[3]
a=np.asarray(Image.open('../model/natief.png').convert('RGB')).astype(int)
Y0,X0=6,9; a=a[Y0:89,X0:95]
w=np.ones(a.shape[:2])
def zone(x0,x1,y0,y1,v): w[y0-Y0:y1-Y0+1, x0-X0:x1-X0+1]=v
zone(10,42,42,67,WF)      # ogen + grijns (natieve coordinaten)
zone(29,62,6,22,WG)       # kleine geest
def kies(a,w,n,axis,md=2):
    A=a if axis==0 else a.transpose(1,0,2); W=w if axis==0 else w.T
    cost=[(np.abs(A[i]-A[i+1]).sum(1)*np.maximum(W[i],W[i+1])).sum() for i in range(len(A)-1)]
    gek=[]
    for i in np.argsort(cost,kind='stable'):
        if all(abs(i-j)>=md for j in gek): gek.append(int(i))
        if len(gek)==n: break
    return sorted(gek)
cols=kies(a,w,a.shape[1]-64,1); b=np.delete(a,cols,1); wb=np.delete(w,cols,1)
nr=a.shape[0]-62; rows=kies(b,wb,nr,0); b=np.delete(b,rows,0)
print('kolommen (natief x)',[c+X0 for c in cols]); print('rijen (natief y)',[r+Y0 for r in rows]); print(b.shape)
c=np.full((64,64,3),255,'uint8'); c[64-b.shape[0]:,:]=b
Image.fromarray(c).save(OUT)
