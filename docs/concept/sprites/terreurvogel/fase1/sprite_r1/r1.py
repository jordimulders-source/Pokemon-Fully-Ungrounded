# Ronde 1: kale reductie -> technisch opschonen (buitenlijn, ruis) -> oog uit Spearow. Niets hertekend.
import numpy as np; from lib import *
K=np.load('kaal.npy'); Sx=K.copy(); ALPHA=K>0
IDXG={}
for g,ids in GROEPIDX.items():
    for i in ids: IDXG[i]=g
DONKER={'snavel':2,'bruin':5,'creme':5,'poten':11,'oog':1}
def buren(y,x):
    for dy,dx in ((-1,0),(1,0),(0,-1),(0,1)):
        yield dy,dx,(ALPHA[y+dy,x+dx] if 0<=y+dy<64 and 0<=x+dx<64 else False)
# 1. buitenlijn: elke randpixel lijn; zwart aan de schaduwkant, eigen donkerste tint aan de lichtkant (boven/links)
RAND=np.zeros((64,64),bool)
for y in range(64):
    for x in range(64):
        if not ALPHA[y,x]: continue
        leeg=[(dy,dx) for dy,dx,a in buren(y,x) if not a]
        if not leeg: continue
        RAND[y,x]=True
        if Sx[y,x]==1: continue
        licht=all(d in ((-1,0),(0,-1)) for d in leeg)
        Sx[y,x]=DONKER[IDXG[Sx[y,x]]] if licht else 1
# 2. ruis: tintclusters < 3 px binnen een groep -> meest voorkomende tint van dezelfde groep eromheen (rand en zwart overgeslagen)
def clusters(S):
    seen=np.zeros((64,64),bool); out=[]
    for y in range(64):
        for x in range(64):
            if seen[y,x] or S[y,x]<=1: continue
            v=S[y,x]; st=[(y,x)]; seen[y,x]=True; cl=[]
            while st:
                cy,cx=st.pop(); cl.append((cy,cx))
                for dy,dx in ((-1,0),(1,0),(0,-1),(0,1)):
                    ny,nx=cy+dy,cx+dx
                    if 0<=ny<64 and 0<=nx<64 and not seen[ny,nx] and S[ny,nx]==v: seen[ny,nx]=True; st.append((ny,nx))
            out.append((v,cl))
    return out
for it in range(3):
    n=0
    for v,cl in clusters(Sx):
        if len(cl)>=3 or IDXG.get(v)=='oog' or v==4: continue   # snavelglans/kam (4) = modelglans, mag <3 px
        if any(RAND[y,x] for y,x in cl): continue
        g=IDXG[v]; tel={}
        for y,x in cl:
            for dy,dx in ((-1,0),(1,0),(0,-1),(0,1),(-1,-1),(1,1),(-1,1),(1,-1)):
                ny,nx=y+dy,x+dx
                if 0<=ny<64 and 0<=nx<64 and (ny,nx) not in cl and IDXG.get(Sx[ny,nx])==g: tel[Sx[ny,nx]]=tel.get(Sx[ny,nx],0)+1
        if tel:
            w=max(tel,key=tel.get)
            for y,x in cl: Sx[y,x]=w
            n+=1
    print('ruisronde',it,n)
np.save('r1_basis.npy',Sx)
# 3. dubbele buitenlijn dunnen: binnenzwart dat tegen zwarte rand ligt en niet doorloopt naar een binnenlijn -> kleur van de binnenburen
C=set()
for y in range(64):
    for x in range(64):
        if Sx[y,x]==1 and not RAND[y,x] and any(RAND[y+dy,x+dx] and Sx[y+dy,x+dx]==1 for dy,dx in ((-1,0),(1,0),(0,-1),(0,1))): C.add((y,x))
dun=[]
for (y,x) in C:
    diep=[(y+dy,x+dx) for dy in (-1,0,1) for dx in (-1,0,1) if (dy or dx) and Sx[y+dy,x+dx]==1 and not RAND[y+dy,x+dx] and (y+dy,x+dx) not in C]
    if diep: continue
    tel={}
    for dy in (-1,0,1):
        for dx in (-1,0,1):
            v=Sx[y+dy,x+dx]
            if v>1 and not RAND[y+dy,x+dx]: tel[v]=tel.get(v,0)+1
    if tel: dun.append(((y,x),max(tel,key=tel.get)))
for (y,x),v in dun: Sx[y,x]=v
print('gedund',len(dun),[p for p,_ in dun])
np.save('r1_basis.npy',Sx)
# 4. snavelpunt: lichte punt uit de kale reductie terug (model: crème punt binnen de zwarte lijn)
for (x,y) in [(12,37),(12,38),(13,39)]:
    assert K[y,x]==4; Sx[y,x]=4
# 4b. poten: tint per pixel uit het model (fractie oranje / donker in de cel, poten_meet.py), randpixels blijven lijn
import poten_meet as PM
nP=[]
for y in range(64):
    for x in range(64):
        if IDXG.get(Sx[y,x])!='poten' or RAND[y,x]: continue
        v=13 if PM.fO[y,x]>=0.45 else (11 if (PM.covD[y,x]/max(PM.cel[y,x],1))>=0.35 else 12)
        if v!=Sx[y,x]: nP.append((x,y,Sx[y,x],v)); Sx[y,x]=v
print('poten per pixel',nP)
# 5. oog: Spearow-oog 1-op-1 (graphics/pokemon/spearow/anim_front_gba.png), verschoven (+5,+4) naar het modeloog
OUD=[(x,y) for y in range(25,30) for x in range(28,33) if K[y,x] in (1,15) or Sx[y,x] in (1,15)]
SP={(25,22):'K',(26,22):'W',(22,23):'m',(23,23):'m',(24,23):'K',(25,23):'W',(26,23):'W',(23,24):'m',(24,24):'W',(25,24):'K',(26,24):'W',(24,25):'K',(25,25):'K'}
DX,DY=5,4
NIEUW={(x+DX,y+DY):c for (x,y),c in SP.items()}
def oog(S,glans):
    S=S.copy()
    for (x,y) in OUD:
        if (x,y) in NIEUW: continue
        tel={}
        for dy in (-1,0,1):
            for dx in (-1,0,1):
                q=(x+dx,y+dy)
                if q in OUD or q in NIEUW: continue
                v=S[y+dy,x+dx]
                if v>1: tel[v]=tel.get(v,0)+1
        S[y,x]=max(tel,key=tel.get) if tel else 6
    for (x,y),c in NIEUW.items():
        S[y,x]={'K':1,'W':15,'m':5}[c]
    if glans: S[28,29]=14
    return S
# 6. losse vlekjes (<3 px, geen lijnzak, geen rand/oog/poten/snavelglans): groeien naar 3 px op de modelplek als het model daar die groep heeft (dekking >=0.25), anders opgaan in de buurtint
cov,col,lum,cel=reductie(); ML=np.load('ml.npy')
GNR={'snavel':2,'bruin':3,'creme':5,'poten':6}
def tintvoor(g,y,x):
    gi=GNR[g]; c=col[y,x,gi]/max(cov[y,x,gi],1); return dichtst(gi,c)
groei=[]; weg=[]
for v,cl in clusters(Sx):
    g=IDXG.get(v)
    if len(cl)>=3 or g in ('oog','poten') or v==4 or any(RAND[y,x] for y,x in cl): continue
    zak=all(sum(Sx[y+dy,x+dx]==1 for dy,dx in ((-1,0),(1,0),(0,-1),(0,1)))>=2 for y,x in cl)
    if zak: continue
    gi=GNR[g]; kand=[]
    for y,x in cl:
        for dy,dx in ((-1,0),(1,0),(0,-1),(0,1)):
            ny,nx=y+dy,x+dx
            if (ny,nx) in cl or RAND[ny,nx] or Sx[ny,nx] in (1,14,15,4): continue
            f=cov[ny,nx,gi]/max(cel[ny,nx],1)
            if f>=0.25: kand.append((f,ny,nx))
    kand=sorted(set(kand),reverse=True)
    if len(cl)+len(kand)>=3:
        for f,ny,nx in kand[:3-len(cl)]: groei.append((nx,ny,int(Sx[ny,nx]),int(v))); Sx[ny,nx]=v
    else:
        tel={}
        for y,x in cl:
            for dy,dx in ((-1,0),(1,0),(0,-1),(0,1),(-1,-1),(1,1),(-1,1),(1,-1)):
                ny,nx=y+dy,x+dx
                if (ny,nx) not in cl and Sx[ny,nx]>1 and Sx[ny,nx] not in (14,15): tel[Sx[ny,nx]]=tel.get(Sx[ny,nx],0)+1
        w=max(tel,key=tel.get)
        for y,x in cl: weg.append((x,y,int(v),int(w))); Sx[y,x]=w
print('vlekjes gegroeid (x,y,oud,nieuw)',groei); print('vlekjes opgegaan',weg)
np.save('r1_basis.npy',Sx)   # basis zonder oog (ogen.py bouwt de oogvarianten hierop)
A=oog(Sx,False); Bv=oog(Sx,True)
assert ((A>0)==ALPHA).all() and ((Bv>0)==ALPHA).all()
opslaan(A,'kuiken_r1_oogA.png'); opslaan(Bv,'kuiken_r1.png'); np.save('r1.npy',Bv)
print('oude oogpixels gevuld',[p for p in OUD if p not in NIEUW])
