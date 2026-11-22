# Verkleint het natieve raster 75->61 door hele kolommen/rijen te schrappen die (bijna) gelijk zijn aan hun buur
# (Gengas-methode: niets hertekenen). Kiest per stap de goedkoopste, niet naast een al geschrapte.
import numpy as np, sys; from PIL import Image
a=np.asarray(Image.open('natief.png').convert('RGB')).astype(int)
a=a[16:91,12:87]   # bbox 75x75
BESCHERM={1:range(0,13),0:range(22,35)}  # gezicht (oog, snavel) niet schrappen
N=int(sys.argv[1]) if len(sys.argv)>1 else 14
def kost(arr,axis):
    # kosten om lijn k te schrappen = verschil met lijn k-1 of k+1 (minimum), op aantal pixels die echt anders zijn
    b=arr if axis==1 else arr.transpose(1,0,2)
    n=b.shape[1]; c=[]
    for k in range(n):
        d=[]
        for m in (k-1,k+1):
            if 0<=m<n: d.append((np.abs(b[:,k]-b[:,m]).sum(1)>60).sum())
        c.append(min(d))
    return np.array(c)
def kies(arr,axis,N):
    c=kost(arr,axis).astype(float); n=len(c); weg=[]
    # spreiding: straf als dichtbij een al geschrapte
    for _ in range(N):
        s=c.copy()
        for w in weg:
            for m in range(max(0,w-2),min(n,w+3)): s[m]+=1000
        s[0]=s[-1]=1e9
        for m in BESCHERM[axis]: s[m]+=500
        k=int(np.argmin(s)); weg.append(k)
    return sorted(weg),c
wk,ck=kies(a,1,N); wr,cr=kies(a,0,N)
print('kolommen weg',wk,[int(ck[k]) for k in wk]); print('rijen weg',wr,[int(cr[k]) for k in wr])
b=np.delete(np.delete(a,wk,axis=1),wr,axis=0)
Image.fromarray(b.astype('uint8')).save('geschrapt.png')
Image.fromarray(b.astype('uint8')).resize((b.shape[1]*8,b.shape[0]*8),Image.NEAREST).save('geschrapt_8x.png')
np.save('weg.npy',np.array([wk,wr]))
print(b.shape)
