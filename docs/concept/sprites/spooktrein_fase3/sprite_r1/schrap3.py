# Schrappen (alleen hele rijen/kolommen weg, geen resamplen) met gelijkmatige spreiding:
# de k geschrapte lijnen blijven dicht bij hun gelijkmatige ideaalpositie (verhoudingen van het model blijven),
# maar mogen binnen een venster opschuiven naar de lijn die het minst beschadigt (gewicht x voor ogen/mond/geest).
# Gebruik: python3 schrap3.py WF WG PEN out.png ['[[x0,x1,aantal],...]'] ['[[y0,y1,aantal],...]']  (banden in natieve coordinaten)
from PIL import Image; import numpy as np, sys
WF=float(sys.argv[1]); WG=float(sys.argv[2]); PEN=float(sys.argv[3]); OUT=sys.argv[4]
a=np.asarray(Image.open('../model/natief.png').convert('RGB')).astype(int)
Y0,X0=6,9; a=a[Y0:89,X0:95]
w=np.ones(a.shape[:2])
def zone(x0,x1,y0,y1,v): w[y0-Y0:y1-Y0+1, x0-X0:x1-X0+1]=v
zone(10,42,42,67,WF); zone(29,62,6,22,WG)
BESCH_K=[11,12,13,14,15,16,26,27,28,29,30,34]   # ogen: niet door oogranden/pupil schrappen (natief x)
BESCH_R=list(range(43,51))                        # oogrijen (natief y)
def kies(a,w,k,axis,besch=(),banden=None):
    A=a if axis==0 else a.transpose(1,0,2); W=w if axis==0 else w.T
    n=len(A)
    # kosten om lijn i te schrappen: verschil met beide buren (lijn verdwijnt tussen i-1 en i+1)
    c=np.array([ (np.abs(A[i]-A[max(i-1,0)]).sum(1)*W[i]).sum()+(np.abs(A[i]-A[min(i+1,n-1)]).sum(1)*W[i]).sum() for i in range(n)],float)
    c=c/np.median(c); c[0]=c[-1]=1e9
    for i in besch: c[i]=1e9
    if banden:
        ideal=[]
        for (b0,b1,q) in banden:
            ideal+= [b0+(j+0.5)*(b1-b0+1)/q for j in range(q)] if q else []
        assert len(ideal)==k,(len(ideal),k)
    else: ideal=[(j+0.5)*n/k for j in range(k)]
    INF=1e18; D=np.full((k+1,n+1),INF); P={}
    D[0,:]=0
    for j in range(1,k+1):
        for i in range(n):
            best=INF;arg=None
            for p in range(0,i-1+1):   # vorige keuze p-1 < i-1 (min afstand 2)
                pass
            # vorige index q (kolom q) met q<=i-2; D[j-1] opgeslagen als beste tot en met kolom q
            prev = D[j-1,i-1] if j>1 else 0  # D[j-1,t] = beste met laatste keuze <= t-1
            v=prev + c[i] + PEN*(i-ideal[j-1])**2
            # D[j,i+1] = min(D[j,i], v)
            if v<D[j,i]: D[j,i+1]=v; P[(j,i+1)]=i
            else: D[j,i+1]=D[j,i]; P[(j,i+1)]=P.get((j,i))
    # terugzoeken
    res=[]; t=n; j=k
    while j>0:
        i=P[(j,t)]; res.append(i); t=i-1; j-=1
    return sorted(res)
import json
BK=json.loads(sys.argv[5]) if len(sys.argv)>5 else None
BR=json.loads(sys.argv[6]) if len(sys.argv)>6 else None
cols=kies(a,w,a.shape[1]-64,1,[x-X0 for x in BESCH_K],[(b0-X0,b1-X0,q) for b0,b1,q in BK] if BK else None); b=np.delete(a,cols,1); wb=np.delete(w,cols,1)
rows=kies(b,wb,a.shape[0]-62,0,[y-Y0 for y in BESCH_R],[(b0-Y0,b1-Y0,q) for b0,b1,q in BR] if BR else None); b=np.delete(b,rows,0)
print('kolommen',[c+X0 for c in cols]); print('rijen',[r+Y0 for r in rows])
c=np.full((64,64,3),255,'uint8'); c[64-b.shape[0]:,:]=b
Image.fromarray(c).save(OUT)
