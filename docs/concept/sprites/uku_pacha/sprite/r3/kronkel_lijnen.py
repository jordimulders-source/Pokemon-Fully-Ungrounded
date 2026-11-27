# Uku Pacha r3: lijnen in de kronkels opnieuw uit het model geprojecteerd, in twee lagen:
#  spiraal = zwarte/bijna-zwarte modellijnen (klasse 0-1) in samenhangende stukken >= MIN cellen
#            -> doorlopende 1 px K (eerst los gedund, zodat segmentlijnen de spiraal niet opeten)
#  segment = de overige modellijnen (klasse 0-4) -> n, gedund met de spiraal vast
# Alleen binnen de kronkelzone (rij >= Y0, geen geest, vleugel, kop of buitenrand). Niets weggelaten:
# elke modellijncel wordt geprojecteerd; dunnen haalt alleen dubbele dikte weg.
import numpy as np, geom, sys
cls=np.load('cls.npy'); GH=np.load('GH.npy')
R=[list(l.rstrip('\n')) for l in open('raster.txt')][:64]
Y0=int(sys.argv[1]) if len(sys.argv)>1 else 41; MIN=8
def ins(x,y): return 0<=x<64 and 0<=y<64 and R[y][x]!='.'
def rand(x,y): return any(not ins(x+a,y+b) for a,b in ((0,1),(0,-1),(1,0),(-1,0)))
Z=np.zeros((64,64),bool)
for y in range(Y0,64):
  for x in range(64):
    if ins(x,y) and not GH[y,x] and R[y][x] not in 'DBhYPW' and not rand(x,y): Z[y,x]=True
# natieve spiraalcellen
dark=np.isin(cls,[0,1]); comp=np.full((100,100),-1); sizes=[]
for y in range(100):
  for x in range(100):
    if dark[y,x] and comp[y,x]<0:
      st=[(x,y)]; n=0; c=len(sizes)
      while st:
        a,b=st.pop()
        if 0<=a<100 and 0<=b<100 and dark[b,a] and comp[b,a]<0:
          comp[b,a]=c; n+=1; st+=[(a+dx,b+dy) for dx in (-1,0,1) for dy in (-1,0,1) if dx or dy]
      sizes.append(n)
sizes=np.array(sizes)
SP=dark&(comp>=0)&(sizes[np.maximum(comp,0)]>=MIN)
SEG=np.isin(cls,[0,1,2,3,4])&~SP
def proj(x,y):
    sx,sy=geom.n2s(x+0.5,y+0.5); return int(np.floor(sx)),int(np.floor(sy))
def teken(mask,verbind_met=None):
    out=np.zeros((64,64),bool)
    for y in range(100):
      for x in range(100):
        if not mask[y,x]: continue
        i0,j0=proj(x,y)
        if 0<=i0<64 and 0<=j0<64: out[j0,i0]=True
        for dy,dx in ((0,1),(1,0),(1,1),(1,-1),(0,-1),(-1,0),(-1,-1),(-1,1)):
          yy,xx=y+dy,x+dx
          if not(0<=yy<100 and 0<=xx<100): continue
          if mask[yy,xx] or (verbind_met is not None and verbind_met[yy,xx]):
            i1,j1=proj(xx,yy); n=max(abs(i1-i0),abs(j1-j0))
            for t in range(1,n+1):
              a,b=round(i0+(i1-i0)*t/n),round(j0+(j1-j0)*t/n)
              if 0<=a<64 and 0<=b<64: out[b,a]=True
    return out&Z
def dun(B,vast):
    def nb(j,i):
        o=[(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1)]
        return [bool(B[j+a,i+b]) if 0<=j+a<64 and 0<=i+b<64 else False for a,b in o]
    ch=True
    while ch:
        ch=False
        for stap in (0,1):
            weg=[]
            for j,i in zip(*np.where(B)):
                if vast[j,i]: continue
                p=nb(j,i); n=sum(p)
                if not 2<=n<=6: continue
                if sum((not p[k]) and p[(k+1)%8] for k in range(8))!=1: continue
                P2,P3,P4,P5,P6,P7,P8,P9=p
                if stap==0 and (P2 and P4 and P6 or P4 and P6 and P8): continue
                if stap==1 and (P2 and P4 and P8 or P2 and P6 and P8): continue
                weg.append((j,i))
            for j,i in weg: B[j,i]=False
            ch|=bool(weg)
    return B
RANDM=np.zeros((64,64),bool)
for y in range(64):
  for x in range(64):
    if ins(x,y) and not Z[y,x]: RANDM[y,x]=True   # alles buiten de zone telt als vaste wand
sp=dun(teken(SP)|RANDM,RANDM)&Z
seg=dun(teken(SEG,SP)|sp|RANDM,sp|RANDM)&Z&~sp
# oude lijnen in de zone weg, nieuwe erin (vlakpixels krijgen hun toon in banden.py)
for y in range(64):
  for x in range(64):
    if not Z[y,x]: continue
    if sp[y,x]: R[y][x]='K'
    elif seg[y,x]: R[y][x]='n'
    elif R[y][x] in 'Kn': R[y][x]='s'
print('spiraal px',sp.sum(),'segment px',seg.sum())
open('raster.txt','w').write('\n'.join(''.join(r) for r in R)+'\n')
