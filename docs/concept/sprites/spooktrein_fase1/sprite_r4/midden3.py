# Ronde 3, alleen het midden (r2 elders bevroren). Uit het model:
#  - materiaal per spritepixel = grijs/bruin-verhouding van de niet-lijn modelpixels in een venster van 3x3 spritepx
#    (6x6 modelpx); grijs alleen binnen de echte grijze stukken (bijlplaat, klem, onderplaat), anders roest;
#  - lange vormen: tint = modelhelderheid, gemiddeld LANGS de plankrichting (lokale richting uit de modellijnen),
#    daarna 3 vultinten per materiaal (lichtste ~30% licht, donkerste ~25% donker, binnen het midden);
#  - scheidingslijnen alleen langs de lange kanten: lijnstukjes uit het model (>=2 donkere modelpx in het blok) die
#    met de plankrichting meelopen en samen >= LMIN px lang zijn; dwarse lijntjes vervallen. Lijntint = donkerste
#    tint van het materiaal (#433425 / #36332b), geen zwart.
import os,numpy as np, ast; from PIL import Image
AMIN=float(os.environ.get('AMIN','-25')); AMAX=float(os.environ.get('AMAX','70'))
ZD=int(os.environ.get('ZD','4'))
LMIN=int(os.environ.get('LMIN','3')); FD=float(os.environ.get('FD','0.25')); FL=float(os.environ.get('FL','0.30')); TH=float(os.environ.get('TH','0.5'))
r2=np.load('../sprite_r2/sprite.npy'); o=r2.copy(); WZ,SZ,RZ,MZ=np.load('z64.npy')
a=np.asarray(Image.open('natief.png').convert('RGB')).astype(float); fg=a.min(2)<225; L=a@[0.299,0.587,0.114]
line=fg&(L<40); grey=fg&~line&((a[...,0]-a[...,2])<=22)
ys,xs=np.where(fg); cy0,cx0=ys.min()-1,xs.min()-1
r=open('schrap.txt').read().split('\n'); rows=set(ast.literal_eval(r[0])); cols=set(ast.literal_eval(r[1]))
kR=[i for i in range(ys.max()+2-cy0) if i not in rows]; kC=[i for i in range(xs.max()+2-cx0) if i not in cols]
X,Y,ww,hh=map(int,open('plaats.txt').read().split())
def blok(x,y):
    hy,hx=y-Y,x-X; rr=[cy0+kR[1+2*hy+k] for k in (0,1) if 0<=1+2*hy+k<len(kR)]; cc=[cx0+kC[2*hx+k] for k in (0,1) if 0<=2*hx+k<len(kC)]
    return [(q,p) for q in rr for p in cc]
fgS=r2>0; pad=np.pad(fgS,1); edge=fgS&~(pad[:-2,1:-1]&pad[2:,1:-1]&pad[1:-1,:-2]&pad[1:-1,2:])
bout=np.load('bout.npy')!=np.load('midden.npy')
M=MZ&fgS&~edge&~WZ&~bout
PC=np.load('stuk64.npy'); GREYP={4,8,10}   # bijlplaat, klem, onderplaat
NB=lambda y,x:[(q,p) for yy in (y-1,y,y+1) for xx in (x-1,x,x+1) for q,p in blok(xx,yy)]
# materiaal
MAT=np.zeros((64,64),int); LU=np.full((64,64),np.nan); D=np.zeros((64,64),int)
for y,x in zip(*np.where(M)):
    w=[(q,p) for q,p in NB(y,x) if fg[q,p] and not line[q,p]]
    g=np.mean([grey[q,p] for q,p in w]) if w else 0
    MAT[y,x]=2 if (g>TH and PC[y,x] in GREYP) else 1
    b=blok(x,y); l=[L[q,p] for q,p in b if fg[q,p] and not line[q,p]]
    if l: LU[y,x]=np.median(l)
    D[y,x]=sum(line[q,p] for q,p in b)
# lokale plankrichting: hoofdas van de donkere modelpixels in een venster van 5x5 spritepx (structuurtensor op L)
gy,gx=np.gradient(L)
def richting(y,x):
    pts=[(q,p) for yy in range(y-2,y+3) for xx in range(x-2,x+3) for q,p in blok(xx,yy)]
    Jxx=sum(gx[q,p]**2 for q,p in pts); Jyy=sum(gy[q,p]**2 for q,p in pts); Jxy=sum(gx[q,p]*gy[q,p] for q,p in pts)
    th=0.5*np.arctan2(2*Jxy,Jxx-Jyy)+np.pi/2          # richting LANGS de randen
    return np.cos(th),np.sin(th)
DIR={}
mid_n=np.load('zones.npy')[3]
Jxx=(gx[mid_n]**2).sum(); Jyy=(gy[mid_n]**2).sum(); Jxy=(gx[mid_n]*gy[mid_n]).sum()
thg=0.5*np.arctan2(2*Jxy,Jxx-Jyy)+np.pi/2; G0=(np.cos(thg),np.sin(thg)); print('hoofdrichting planken (graden, + = rechtsboven)',round(-np.degrees(np.arctan2(G0[1],G0[0])),1))
for y,x in zip(*np.where(M)):
    c,s_=richting(y,x)
    DIR[(y,x)]=(c,s_) if abs(c*G0[0]+s_*G0[1])>=np.cos(np.radians(45)) else G0   # te steil t.o.v. de bundel: bundelrichting
# tint: helderheid gemiddeld langs de plank (+-2 stappen in de richting)
SM=np.full((64,64),np.nan)
for (y,x),(c,s) in DIR.items():
    vals=[]
    for t in (-2,-1,0,1,2):
        yy,xx=int(round(y+t*s)),int(round(x+t*c))
        if 0<=yy<64 and 0<=xx<64 and M[yy,xx] and MAT[yy,xx]==MAT[y,x] and np.isfinite(LU[yy,xx]): vals.append(LU[yy,xx])
    if vals: SM[y,x]=np.mean(vals)
# lijnen langs de plank
cand=np.zeros((64,64),bool)
for (y,x),(c,s) in DIR.items():
    if D[y,x]<2: continue
    # lijn loopt mee met de plank als een buur in de plankrichting ook donker is in het model
    ok=False
    for t in (-1,1):
        yy,xx=int(round(y+t*s)),int(round(x+t*c))
        if (yy,xx)!=(y,x) and 0<=yy<64 and 0<=xx<64 and M[yy,xx] and D[yy,xx]>=1: ok=True
    cand[y,x]=ok
# alleen stukken >= LMIN (8-samenhang)
LN=np.zeros((64,64),bool); seen=np.zeros((64,64),bool)
for y,x in zip(*np.where(cand)):
    if seen[y,x]: continue
    comp=[(y,x)]; seen[y,x]=True; i=0
    while i<len(comp):
        cy,cx=comp[i]; i+=1
        for dy in (-1,0,1):
            for dx in (-1,0,1):
                ny,nx=cy+dy,cx+dx
                if cand[ny,nx] and not seen[ny,nx]: seen[ny,nx]=True; comp.append((ny,nx))
    if len(comp)>=LMIN:
        P_=np.array(comp,float); P_-=P_.mean(0)
        if len(comp)>=2:
            w,v=np.linalg.eigh(P_.T@P_); dy_,dx_=v[:,-1]
            if dx_<0: dy_,dx_=-dy_,-dx_
            ang=np.degrees(np.arctan2(-dy_,dx_))      # 0 = horizontaal, + = naar rechtsboven
            if not (AMIN<=ang<=AMAX): continue       # dwars op de planken: vervalt
        for p in comp: LN[p]=True
SETS={1:[3,4,5],2:[8,9,10]}; DARK={1:2,2:7}
for m in (1,2):
    sel=M&(MAT==m)&~LN&np.isfinite(SM)
    if not sel.any(): continue
    q1,q2=np.quantile(SM[sel],FD),np.quantile(SM[sel],1-FL)
    for y,x in zip(*np.where(M&(MAT==m))):
        if LN[y,x]: o[y,x]=1 if D[y,x]>=ZD else DARK[m]; continue
        l=SM[y,x] if np.isfinite(SM[y,x]) else np.nanmean(SM[sel])
        S=SETS[m]; o[y,x]=S[0] if l<q1 else (S[1] if l<q2 else S[2])
# ontkorrelen: tinteilandjes < MINC px (zelfde materiaal) -> buurtint
MINC=int(os.environ.get('MINC','4'))
for it in range(2):
    seen=np.zeros((64,64),bool)
    for y,x in zip(*np.where(M&~LN)):
        if seen[y,x]: continue
        v=o[y,x]; comp=[(y,x)]; seen[y,x]=True; i=0
        while i<len(comp):
            cy,cx=comp[i]; i+=1
            for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
                ny,nx=cy+dy,cx+dx
                if M[ny,nx] and not LN[ny,nx] and o[ny,nx]==v and not seen[ny,nx]: seen[ny,nx]=True; comp.append((ny,nx))
        if len(comp)<MINC:
            nb=[o[cy+dy,cx+dx] for cy,cx in comp for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)) if M[cy+dy,cx+dx] and not LN[cy+dy,cx+dx] and MAT[cy+dy,cx+dx]==MAT[cy,cx] and o[cy+dy,cx+dx]!=v]
            if nb:
                u,c=np.unique(nb,return_counts=True)
                for p in comp: o[p]=u[c.argmax()]
np.save('sprite.npy',o)
gr=(M&(MAT==2)).sum(); print('midden',M.sum(),'grijs',gr,'lijn',LN.sum(),'zwart totaal %.1f%%'%(100*(o==1).sum()/(o>0).sum()),'anders dan r2',int((o!=r2).sum()))
