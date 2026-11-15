# Verkleint het gekozen model (74x74 natief) naar 64x64 ZONDER resamplen: er worden 10 rijen en 10 kolommen
# geschrapt waar dat het minst zichtbaar is (rij/kolom die het meest op zijn buur lijkt), gespreid.
# Elke overgebleven pixel is een echte modelpixel.
from PIL import Image; import numpy as np, sys
D='docs/concept/sprites/gengas/model/'
a=np.asarray(Image.open(D+'gekozen_v3_natief.png').convert('RGB')).astype(int)
def kies(a,n,axis,verboden=()):
    A=a if axis==0 else a.transpose(1,0,2)
    cost=[np.abs(A[i]-A[i+1]).sum() for i in range(len(A)-1)]
    order=np.argsort(cost); gekozen=[]
    for i in order:
        if i in verboden: continue
        if all(abs(i-j)>=4 for j in gekozen): gekozen.append(int(i))
        if len(gekozen)==n: break
    return sorted(gekozen)
n=a.shape[0]-64
rows=kies(a,n,0); cols=kies(a,n,1)
b=np.delete(np.delete(a,rows,0),cols,1)
print('rijen',rows,'kolommen',cols,b.shape)
Image.fromarray(b.astype('uint8')).save(D+'model_64_geschrapt.png')
