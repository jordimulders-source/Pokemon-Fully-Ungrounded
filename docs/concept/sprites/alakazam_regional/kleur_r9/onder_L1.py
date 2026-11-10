# onder_L1.py: linkerhand L1 = gekwantiseerde modelonderlaag in de zone x3-20, y34-46 (meet5.npz, geometrie silhouet/geo.py)
# regels: o waar fo>=0.3 of L<60 (lijnen, schoppen, kaartindex); kaart (L>=185) w/a; hand b/c/d; silhouetrand o (kaart lichtkant d)
# de onderarm (zwart in het model, grijs volgens SPEC) blijft zoals r8
import numpy as np,pal
d=np.load('meet5.npz'); fo,sil=d['fo'],d['sil']; L=d['med'].mean(2)
B=[list(r) for r in pal.load('basis_r8.txt')]
pad=np.pad(sil,1); edge=sil&~(pad[:-2,1:-1]&pad[2:,1:-1]&pad[1:-1,:-2]&pad[1:-1,2:])
def onderarm(x,y): return (y<=37 and x>=11) or (38<=y<=40 and x>=15 and L[y,x]<60) or (y==38 and x>=15)
R=[r[:] for r in B]
for y in range(34,47):
    for x in range(3,21):
        if not sil[y,x] or onderarm(x,y): continue
        l=L[y,x]
        if fo[y,x]>=.3 or l<60: c='o'
        elif l>=185: c='w' if l>=215 else 'a'
        elif l>=150: c='b'
        elif l>=115: c='c'
        else: c='d'
        if edge[y,x] and c not in 'od': c='d' if (l>=185 and x<=8) else 'o'
        R[y][x]=c
open('onderlaag_L1.txt','w').write('\n'.join(''.join(r) for r in R)+'\n')
for y in range(33,47): print(y,' '.join(R[y][3:21]))
# --- technisch opschonen (zie NOTITIES): randen kaart lichtkant d, kaartindex -> a, lijn (15,39) volgens fo, benen buiten de hand terug naar r8
FIX={(7,34):'d',(6,35):'d',(5,36):'d',(5,38):'w',(6,39):'w',(6,40):'d',(5,39):'d',(11,38):'b',(15,39):'o',(14,39):'c',
     (16,40):'o',(20,39):'o',(19,40):'o',(11,43):'d',(12,43):'d',(13,44):'d'}
for (x,y),c in FIX.items(): R[y][x]=c
for y in range(44,47):
    for x in range(18,21): R[y][x]=B[y][x]
open('onderlaag_L1.txt','w').write('\n'.join(''.join(r) for r in R)+'\n')
print('na opschonen')
for y in range(33,47): print(y,' '.join(R[y][3:21]))
