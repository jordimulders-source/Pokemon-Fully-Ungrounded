# Model (natief 74x48) -> <=64 breed door hele kolommen/rijen te schrappen (Gengas-methode).
# Jordi: "als je moet inkorten, gebruik daar zoveel mogelijk het water en de boot voor" en
# "als het water maar een heel klein beetje uit de boot loopt is dat ook niet erg".
# Toegestane kolommen: alleen kanopunt-hals en achterkant (romp + water), NOOIT bladhoop/rand, ogen kano,
# bombilla's of ventje. Toegestane rijen: alleen romp onder het kano-oog.
from PIL import Image; import numpy as np, sys
D='docs/concept/sprites/mate_fase2/sprite/r1/'
a=np.asarray(Image.open(D+'natief.png').convert('RGB')).astype(int)
a=a[29:77,11:85]           # dier: y29-76, x11-84
NC=int(sys.argv[1]) if len(sys.argv)>1 else 10
NR=int(sys.argv[2]) if len(sys.argv)>2 else 4
def kies(A,n,toegestaan,sp=3):
    cost={i:np.abs(A[i]-A[i+1]).sum() for i in toegestaan}
    gekozen=[]
    for i in sorted(cost,key=cost.get):
        if all(abs(i-j)>=sp for j in gekozen): gekozen.append(i)
        if len(gekozen)==n: break
    return sorted(gekozen)
# lokale coordinaten = natief - offset
# 4 kolommen in de hals van de punt (om de andere), 8 in achterkant romp + waterval
# (r1: 12 kolommen -> 62 breed, 1 px marge links en rechts in het 64-vak)
cols=[x-11 for x in (14,16,18,20)]+kies(a.transpose(1,0,2),NC-4,[x-11 for x in range(73,84)],1)
cols=sorted(cols)
rows=kies(a,NR,[y-29 for y in range(66,75)],2)
b=np.delete(np.delete(a,rows,0),cols,1)
print('kolommen (natief x)',[c+11 for c in cols],'rijen (natief y)',[r+29 for r in rows],b.shape)
Image.fromarray(b.astype('uint8')).save(D+'geschrapt.png')
