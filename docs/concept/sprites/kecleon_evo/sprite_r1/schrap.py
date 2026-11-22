# Verkleinen zonder hertekenen (Gengas/Mightyena-methode): figuur 78x78 (combi_kop, bbox x14-91, y12-89)
# -> 63x63 door 15 rijen en 15 kolommen te schrappen; één schrapping per gelijk stuk, binnen het stuk
# de rij/kolom die het meest op zijn buur lijkt (lijnpixels wegen 10x). Oog/pupil/kaak nooit geschrapt.
import numpy as np
from PIL import Image
K=np.load('klassen78.npy')
c=np.asarray(Image.open('../model/combi_kop.png').convert('RGB'))[12:90,14:92]
def kosten(A):
    w=np.where(A=='#',10,1)
    return np.array([((A[i]!=A[i+1])*np.maximum(w[i],w[i+1])).sum() for i in range(len(A)-1)])
def kies(A,n,verboden):
    k=kosten(A); N=len(A); gr=np.linspace(0,N,n+1); gek=[]
    for s in range(n):
        lo,hi=int(np.ceil(gr[s])),int(np.floor(gr[s+1])); r=0
        while True:
            kand=[i for i in range(max(1,lo-r),min(hi+r,N-1)) if i not in verboden and all(abs(i-j)>=3 for j in gek)]
            if kand: break
            r+=1
        gek.append(min(kand,key=lambda i:(k[i],abs(i-(lo+hi)/2))))
    return sorted(gek)
VR=set(range(14,25)); VK=set(range(12,26))
rows=kies(K,15,VR); cols=kies(K.T,15,VK)
print('rijen weg',rows); print('kolommen weg',cols)
R=np.delete(np.delete(K,rows,0),cols,1); C=np.delete(np.delete(c,rows,0),cols,1)
np.save('klassen63.npy',R)
a=np.zeros((63,63,4),'uint8'); a[...,:3]=C; a[...,3]=np.where(R!='.',255,0)
Image.fromarray(a).save('model_verkleind63.png')
print('\n'.join('%2d '%i+''.join(r) for i,r in enumerate(R)))
