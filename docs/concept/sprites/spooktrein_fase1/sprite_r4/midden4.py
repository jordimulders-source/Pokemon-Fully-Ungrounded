# Ronde 4, alleen het midden. Jordi: "liever ... met iets grotere vormen netjes gedefinieerd de stapel kan vullen
# dan dat het een brei wordt" / "een bruine brei moet het niet worden".
# Het midden wordt 9 stukken (samengevoegd uit de modelstukken van r2, stuk64.npy):
#   vorm en plek = model; materiaal = model (grijs alleen bijlplaat, klem, onderplaat);
#   per stuk een tintlaag (licht/midden/donker roest, gerangschikt op de modelhelderheid van het stuk), zodat
#   buren verschillen; vulling in vlakken: per kolom bovenste pixel licht, onderste donker, rest midden;
#   gesloten 1px-lijn rondom; bij overlap krijgt het voorste stuk de lijn (diepte volgens het model).
import os,numpy as np, ast; from PIL import Image
ZD=int(os.environ.get('ZD','2'))
r3=np.load('../sprite_r3/sprite.npy'); o=r3.copy(); WZ,SZ,RZ,MZ=np.load('z64.npy'); PC0=np.load('stuk64.npy')
fgS=r3>0; pad=np.pad(fgS,1); edge=fgS&~(pad[:-2,1:-1]&pad[2:,1:-1]&pad[1:-1,:-2]&pad[1:-1,2:])
bout=np.load('bout.npy')!=np.load('midden.npy')
M=MZ&fgS&~edge&~WZ&~bout
GROEP={1:'boven',14:'boven',2:'staven',3:'staven',4:'bijlplaat',6:'links',13:'links',7:'klinkplaat',8:'klem',
       9:'onderplank',12:'onderplank',10:'onderplaat',11:'ketting'}
NAMEN=['klem','klinkplaat','onderplaat','bijlplaat','links','onderplank','ketting','staven','boven']  # voor -> achter
DIEPTE={n:len(NAMEN)-i for i,n in enumerate(NAMEN)}
GRIJS={'bijlplaat','klem','onderplaat'}
P=np.zeros((64,64),int)
for k,g in GROEP.items(): P[(PC0==k)&M]=NAMEN.index(g)+1
# losse middenpixel zonder stuk -> buurstuk
for y,x in zip(*np.where(M&(P==0))):
    nb=[P[y+dy,x+dx] for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)) if P[y+dy,x+dx]>0]
    if nb: P[y,x]=max(set(nb),key=nb.count)
# vormen gladmaken: modusfilter 3x3 over de stukken (2 rondes), alleen binnen M
for it in range(2):
    Q=P.copy()
    for y,x in zip(*np.where(M)):
        nb=[P[y+dy,x+dx] for dy in (-1,0,1) for dx in (-1,0,1) if M[y+dy,x+dx] and P[y+dy,x+dx]>0]
        if not nb: continue
        u,c=np.unique(nb,return_counts=True)
        if c.max()>=5 and u[c.argmax()]!=P[y,x]: Q[y,x]=u[c.argmax()]
    P=Q
# stukken die in delen uiteenvallen: delen < 4 px -> buurstuk
def comps(mask):
    seen=np.zeros((64,64),bool); res=[]
    for y,x in zip(*np.where(mask)):
        if seen[y,x]: continue
        c=[(y,x)]; seen[y,x]=True; i=0
        while i<len(c):
            cy,cx=c[i]; i+=1
            for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
                ny,nx=cy+dy,cx+dx
                if mask[ny,nx] and not seen[ny,nx]: seen[ny,nx]=True; c.append((ny,nx))
        res.append(c)
    return res
for k in range(1,10):
    for c in comps(P==k):
        if len(c)<4:
            nb=[P[cy+dy,cx+dx] for cy,cx in c for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)) if P[cy+dy,cx+dx] not in (0,k)]
            if nb:
                for p in c: P[p]=max(set(nb),key=nb.count)
# modelhelderheid per stuk -> tintlaag
a=np.asarray(Image.open('natief.png').convert('RGB')).astype(float); fg=a.min(2)<225; L=a@[0.299,0.587,0.114]
ys,xs=np.where(fg); cy0,cx0=ys.min()-1,xs.min()-1
r=open('schrap.txt').read().split('\n'); rows=set(ast.literal_eval(r[0])); cols=set(ast.literal_eval(r[1]))
kR=[i for i in range(ys.max()+2-cy0) if i not in rows]; kC=[i for i in range(xs.max()+2-cx0) if i not in cols]
X,Y,ww,hh=map(int,open('plaats.txt').read().split())
def blok(x,y):
    hy,hx=y-Y,x-X; return [(cy0+kR[1+2*hy+i],cx0+kC[2*hx+j]) for i in (0,1) for j in (0,1)]
lum={}
for k in range(1,10):
    v=[L[q,p] for y,x in zip(*np.where(P==k)) for q,p in blok(x,y) if fg[q,p] and L[q,p]>=40]
    lum[NAMEN[k-1]]=np.median(v) if v else 0
bruin=sorted([n for n in NAMEN if n not in GRIJS and n!='ketting'],key=lambda n:-lum[n])
LAAG={}
for i,n in enumerate(bruin): LAAG[n]='licht' if i<len(bruin)/3 else ('midden' if i<2*len(bruin)/3 else 'donker')
# buren mogen niet dezelfde tintlaag hebben (Jordi: "een bruine brei moet het niet worden")
BUUR=set()
for y,x in zip(*np.where(P>0)):
    for dy,dx in ((1,0),(0,1)):
        q=P[y+dy,x+dx]
        if q>0 and q!=P[y,x]: BUUR.add(frozenset((NAMEN[P[y,x]-1],NAMEN[q-1])))
vast=[]
for n in bruin:
    bezet={LAAG.get(m) for m in vast if frozenset((n,m)) in BUUR}; vast.append(n)
    if LAAG[n] in bezet:
        vrij=[t for t in ('licht','midden','donker') if t not in bezet]
        if vrij: LAAG[n]=min(vrij,key=lambda t:abs(['licht','midden','donker'].index(t)-['licht','midden','donker'].index(LAAG[n])))
print('buren',sorted(tuple(sorted(b)) for b in BUUR))
LAAG['ketting']='ketting'
for n in GRIJS: LAAG[n]='grijs'
TINT={'licht':(5,5,4),'midden':(5,4,3),'donker':(4,3,2),'ketting':(3,2,2),'grijs':(10,9,8)}   # (boven, midden, onder)
LIJN={'grijs':7}
print('modelhelderheid',{n:int(lum[n]) for n in NAMEN}); print('tintlaag',LAAG)
# lijnen: grens van een stuk met iets anders. Bij twee stukken: lijn aan de kant van het voorste stuk.
LN=np.zeros((64,64),bool)
for y,x in zip(*np.where(P>0)):
    k=P[y,x]; d=DIEPTE[NAMEN[k-1]]
    for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
        ny,nx=y+dy,x+dx; q=P[ny,nx]
        if q==k: continue
        if q>0:
            if d>DIEPTE[NAMEN[q-1]]: LN[y,x]=True
        else:
            if o[ny,nx] not in (1,2,7) and o[ny,nx]!=0: LN[y,x]=True     # tegen pijp/wiel/rail zonder lijn
# lijndikte: geen 2x2-blokken lijn binnen hetzelfde stuk (dun houden)
for y,x in zip(*np.where(LN)):
    if LN[y+1,x] and LN[y,x+1] and LN[y+1,x+1] and P[y+1,x+1]==P[y,x]: LN[y+1,x+1]=False
# vulling in vlakken
D=np.zeros((64,64),int)
for y,x in zip(*np.where(P>0)): D[y,x]=sum(L[q,p]<40 for q,p in blok(x,y))
for k in range(1,10):
    n=NAMEN[k-1]; T=TINT[LAAG[n]]; inner=(P==k)&~LN
    for x in range(64):
        col=np.where(inner[:,x])[0]
        for y in col:
            top=not inner[y-1,x]; bot=not inner[y+1,x]
            o[y,x]=T[0] if top and not bot else (T[2] if bot and not top else T[1])
    for y,x in zip(*np.where((P==k)&LN)):
        o[y,x]=1 if D[y,x]>=ZD else (LIJN.get(LAAG[n],2) if LAAG[n]!='ketting' else 1)
# tintvlakjes < 3 px binnen een stuk -> middentint
for k in range(1,10):
    T=TINT[LAAG[NAMEN[k-1]]]
    for t in set(T):
        for c in comps((P==k)&~LN&(o==t)):
            if len(c)<3 and t!=T[1]:
                for p in c: o[p]=T[1]
np.save('sprite.npy',o); np.save('stuk_r4.npy',P)
print('zwart %.1f%%'%(100*(o==1).sum()/(o>0).sum()),'buiten midden anders',int(((o!=r3)&~M).sum()))
