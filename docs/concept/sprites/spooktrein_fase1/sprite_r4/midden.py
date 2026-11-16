# Reparatie 1, 2, 5 (r2): het midden opnieuw opgebouwd uit de stukken (stukken.py). Per spritepixel:
#  - stuk = meerderheid van de 4 modelpixels in zijn blok (zelfde schrap + 2x-afbeelding als r1);
#  - lijn alleen op de grens tussen twee stukken, en alleen waar het model daar donkere pixels heeft
#    (de kant met de meeste donkere modelpixels wordt de lijn, zodat hij 1 px dik blijft);
#  - tint = modelhelderheid van het blok (zonder lijnpixels), 3x3 gemiddeld binnen het stuk, naar de 3 vultinten
#    van het materiaal (roest #5f4b3a #765a43 #9f7e65, staal #4e4a44 #7b7975 #a39b93; ketting: donkere roest
#    #433425 #5f4b3a #765a43). Buitenrand (silhouet) en alles buiten het midden: r1 ongewijzigd.
import numpy as np, ast; from PIL import Image
IN='wiel.npy'
o=np.load(IN).copy(); r1=np.load('../sprite_r1/sprite.npy')
WZ,SZ,RZ,MZ=np.load('z64.npy')
a=np.asarray(Image.open('natief.png').convert('RGB')).astype(float); fg=a.min(2)<225; L=a@[0.299,0.587,0.114]; line=fg&(L<40)
lab=np.load('stuk_nat.npy'); mat=np.load('stuk_mat.npy'); KET=[i for i in range(len(mat)) if i==11]
ys,xs=np.where(fg); cy0,cx0=ys.min()-1,xs.min()-1
r=open('schrap.txt').read().split('\n'); rows=set(ast.literal_eval(r[0])); cols=set(ast.literal_eval(r[1]))
kR=[i for i in range(ys.max()+2-cy0) if i not in rows]; kC=[i for i in range(xs.max()+2-cx0) if i not in cols]
X,Y,ww,hh=map(int,open('plaats.txt').read().split())
def blok(x,y):
    hy,hx=y-Y,x-X; rr=[cy0+kR[1+2*hy+k] for k in (0,1) if 1+2*hy+k<len(kR)]; cc=[cx0+kC[2*hx+k] for k in (0,1) if 2*hx+k<len(kC)]
    return [(q,p) for q in rr for p in cc]
fgS=r1>0; pad=np.pad(fgS,1); edge=fgS&~(pad[:-2,1:-1]&pad[2:,1:-1]&pad[1:-1,:-2]&pad[1:-1,2:])
M=MZ&fgS&~edge&~WZ
PC=np.zeros((64,64),int); D=np.zeros((64,64),int); LU=np.full((64,64),np.nan)
for y,x in zip(*np.where(M)):
    b=blok(x,y); ids=[lab[q,p] for q,p in b if lab[q,p]>0]
    if not ids: continue
    u,c=np.unique(ids,return_counts=True); PC[y,x]=u[c.argmax()]
    D[y,x]=sum(line[q,p] for q,p in b)
    l=[L[q,p] for q,p in b if fg[q,p] and not line[q,p]]
    if l: LU[y,x]=np.median(l)
# grenslijnen
LN=np.zeros((64,64),bool)
for y,x in zip(*np.where(PC>0)):
    for dy,dx in ((1,0),(0,1),(-1,0),(0,-1)):
        ny,nx=y+dy,x+dx
        other=PC[ny,nx]
        if other==PC[y,x]: continue
        if other==0 and not fgS[ny,nx]: continue          # buitenrand regelt r1
        dn=D[ny,nx] if other>0 else (1 if r1[ny,nx] in (1,2,7) else 0)
        if D[y,x]>=1 and (D[y,x]>dn or (D[y,x]==dn and (dy,dx) in ((1,0),(0,1)))): LN[y,x]=True
# tint
hx_=lambda c:[int(c[i:i+2],16) for i in (1,3,5)]
PAL=['#1e170e','#433425','#5f4b3a','#765a43','#9f7e65','#b39b87','#36332b','#4e4a44','#7b7975','#a39b93','#d8c8b0']
P=np.array([hx_(c) for c in PAL],float); PL=P@[0.299,0.587,0.114]
SETS={1:[3,4,5],2:[8,9,10],'k':[2,3,4]}
import os; REL=os.environ.get('REL','1')=='1'; FD=float(os.environ.get('FD','0.25')); FL=float(os.environ.get('FL','0.30'))
SM=np.full((64,64),np.nan); RR=range(-int(os.environ.get('R','1')),int(os.environ.get('R','1'))+1)
for y,x in zip(*np.where((PC>0)&~LN)):
    k=PC[y,x]; vals=[LU[y+dy,x+dx] for dy in RR for dx in RR if 0<=y+dy<64 and 0<=x+dx<64 and PC[y+dy,x+dx]==k and not LN[y+dy,x+dx] and not np.isnan(LU[y+dy,x+dx])]
    if vals: SM[y,x]=np.mean(vals)
QS={k:(np.nanquantile(SM[PC==k],FD),np.nanquantile(SM[PC==k],1-FL)) for k in np.unique(PC[PC>0]) if np.isfinite(SM[PC==k]).any()}
n=0
for y,x in zip(*np.where(PC>0)):
    k=PC[y,x]
    if LN[y,x]: v=1
    else:
        l=SM[y,x] if np.isfinite(SM[y,x]) else np.nanmean(SM[PC==k]); S=SETS['k'] if k==11 else SETS[mat[k]]
        if REL:   # binnen het stuk: lichtste deel van het model -> lichte tint, donkerste -> donkere tint
            q1,q2=QS[k]; v=S[0] if l<q1 else (S[1] if l<q2 else S[2])
        else: v=S[int(np.argmin([abs(PL[i-1]-l) for i in S]))]
    if o[y,x]!=v: n+=1
    o[y,x]=v
np.save('midden.npy',o); np.save('stuk64.npy',PC); print('middenpixels veranderd t.o.v. r1(+wiel)',n,'grenslijn',LN.sum())
# ontkorrelen binnen elk stuk: tinteilandjes < MINC px nemen de meest voorkomende buurtint van hetzelfde stuk aan
MINC=int(os.environ.get('MINC','3')); ch=0
for it in range(2):
    seen=np.zeros((64,64),bool)
    for y,x in zip(*np.where((PC>0)&~LN)):
        if seen[y,x]: continue
        v=o[y,x]; k=PC[y,x]; comp=[(y,x)]; seen[y,x]=True; i=0
        while i<len(comp):
            cy,cx=comp[i]; i+=1
            for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
                ny,nx=cy+dy,cx+dx
                if PC[ny,nx]==k and o[ny,nx]==v and not seen[ny,nx] and not LN[ny,nx]: seen[ny,nx]=True; comp.append((ny,nx))
        if len(comp)<MINC:
            nb=[o[cy+dy,cx+dx] for cy,cx in comp for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)) if PC[cy+dy,cx+dx]==k and not LN[cy+dy,cx+dx] and o[cy+dy,cx+dx]!=v]
            if nb:
                u,c=np.unique(nb,return_counts=True)
                for p in comp: o[p]=u[c.argmax()]; ch+=1
np.save('midden.npy',o); print('ontkorreld',ch)
