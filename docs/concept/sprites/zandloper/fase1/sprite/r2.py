# r2: kale reductie -> gezicht per cel uit het model (raster.py) + zand rond de ogen opgeruimd
#     -> handen per cel uit het model (diagonaal, 1-px trapjes) -> randreparaties uit r1.
from gemeen import *
S=np.load('kaal.npy').copy(); K0=S.copy()
ZAND=[2,3,4,5,6]; Z=(27,47,23,35)   # gezichtszone x0,x1,y0,y1
def buren(S,x,y,ok):
    nb=[S[y+a,x+b] for a,b in ((0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1))]
    z=[n for n in nb if n in ok]; return max(set(z),key=z.count) if z else None
# 1. oogresten van de reductie wissen (binnen het zand)
for _ in range(3):
    for y in range(Z[2],Z[3]):
        for x in range(Z[0],Z[1]):
            v=S[y,x]
            if v in (1,14,15,7) and sum(S[y+a,x+b] in ZAND+[1,14,15] for a,b in ((0,1),(0,-1),(1,0),(-1,0)))>=3:
                n=buren(S,x,y,ZAND)
                if n: S[y,x]=n
# 2. ogen per cel uit het model
L={(29,25):1,(30,26):1,(31,26):1,(29,27):14,(30,27):14,(31,27):1,(29,28):14,(30,28):14,(31,28):1,(32,28):1,
   (28,27):3,(28,28):3,(29,26):3}
R={**{(x,29):1 for x in range(36,43)},(43,29):2,
   (36,30):3,(37,30):14,(38,30):7,(39,30):1,(40,30):14,(41,30):14,(42,30):1,
   (37,31):3,(38,31):14,(39,31):14,(40,31):14,(41,31):3,(39,32):3,(40,32):3}
OOG={**L,**R}
# 3. losse bruine plekjes (zand-donker/-lijn, <=2 px, 8-buren) in de zone opruimen
vast=set(OOG)
for c in (2,3):
    lab,n=nd.label(S==c,structure=np.ones((3,3)))
    for k in range(1,n+1):
        ys,xs=np.where(lab==k)
        if len(ys)<=2 and all(Z[0]<=x<Z[1] and Z[2]<=y<Z[3] for x,y in zip(xs,ys)):
            for x,y in zip(xs,ys):
                if (x,y) in vast: continue
                if any(S[y+a,x+b] in (7,8,9,10,0) for a,b in ((0,1),(0,-1),(1,0),(-1,0))): continue  # zandrand tegen glas blijft
                nb=buren(S,x,y,[4,5,6]);
                if nb: S[y,x]=nb
for (x,y),v in OOG.items(): S[y,x]=v
# 4. handen per cel uit het model
for x0,y0,x1,y1 in [(8,28,21,40),(43,36,56,47)]:
    blk=S[y0:y1,x0:x1]; blk[np.isin(blk,[1,11,12,13])]=0
HL={30:{12:'c',13:'c',14:'c'},
    31:{10:'K',11:'c',12:'C',13:'c',14:'C',15:'c'},
    32:{10:'K',11:'k',12:'k',13:'c',14:'c',15:'C',16:'c'},
    33:{10:'K',11:'k',12:'k',13:'k',14:'k',15:'C',16:'C',17:'c'},
    34:{11:'K',12:'K',13:'k',14:'c',15:'k',16:'C',17:'C',18:'K'},
    35:{13:'K',14:'k',15:'c',16:'C',17:'C',18:'K'},
    36:{13:'K',14:'k',15:'C',16:'C',17:'K'},
    37:{14:'K',15:'K',16:'K'}}
HR={38:{49:'c',50:'c',51:'c'},
    39:{48:'c',49:'C',50:'C',51:'C',52:'c'},
    40:{47:'c',48:'C',49:'C',50:'c',51:'C',52:'C',53:'c'},
    41:{46:'K',47:'k',48:'C',49:'c',50:'K',51:'C',52:'C',53:'K'},
    42:{46:'K',47:'k',48:'C',49:'K',50:'c',51:'C',52:'C',53:'K'},
    43:{46:'K',47:'k',48:'K',49:'c',50:'k',51:'k',52:'C',53:'K'},
    44:{47:'K',48:'c',49:'k',50:'K',51:'K',52:'K'},
    45:{48:'K',49:'K',50:'K'}}
M={'K':1,'c':11,'k':12,'C':13}
for H in (HL,HR):
    for y,r in H.items():
        for x,v in r.items(): S[y,x]=M[v]
# 5. randreparaties uit r1 (kappen/glas)
for x,y,a,b in [(32,14,12,11),(33,14,12,11),(39,16,12,11),(40,16,12,11),(16,46,12,11),(19,42,10,8),(42,36,8,7)]:
    assert S[y,x]==a,(x,y,S[y,x]); S[y,x]=b
np.save('r2/zandloper_fase1_r2.npy',S); opslaan(S,'r2/zandloper_fase1_r2.png')
P=np.pad(S,1); fout=[(x,y,NAAM[S[y,x]]) for y in range(64) for x in range(64) if S[y,x] and S[y,x] not in (1,7,8,11) and 0 in (P[y,x+1],P[y+2,x+1],P[y+1,x],P[y+1,x+2])]
print('buitenrand-fouten',fout,'kleuren',len(np.unique(S)),'gevuld',(S>0).sum())
d=(S!=K0); print('diff t.o.v. kaal',d.sum(),'gezicht',d[Z[2]:Z[3],Z[0]:Z[1]].sum(),'handen',d[28:40,8:21].sum()+d[36:47,43:56].sum())
for y in range(22,35): print('%2d '%y+''.join(CH[S[y,x]] for x in range(25,48)))
