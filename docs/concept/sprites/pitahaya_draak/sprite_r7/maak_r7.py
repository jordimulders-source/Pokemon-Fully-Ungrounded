# Pitahaya-draak r7 op sprite_r6/pitahaya_r6.png. Niets getekend: elke pixel uit het natieve model (sprite_r1/natief.py,
# pitch 5,118, factor 3) of een technische opschoning. Aanroep: python3 maak_r7.py [uit.png]
#  1 LIJNEN  : lijnpixels van het model (zwart, of groen/roze lum < LT) natief geskeletteerd; elk skeletpunt
#              geprojecteerd op zijn spritepixel = doorlopende 1-px lijn (spooktrein fase 3, punt 2).
#              Kleur: zwart waar de modellijn >= 3 natieve px dik is (afstandstransform >= DTZ), anders de donkerste tint
#              van het vlak (roze 2, groen 8). Skeletstukjes < MINL natieve px = vlekje, geen lijn.
#  2 GAT     : achtergrond die het model tussen arm en romp insluit -> transparant (>= 3/9).
#  3 VULLING : niet-lijnpixels per kleurgroep (roze/groen, groep uit r6) uit de gladde toonkaart van het model
#              (gauss binnen de groep), 3 tinten; drempels = kwantielen zodat elke tint evenveel px krijgt als
#              het model natief heeft (volume van het model).
#  4 RUIS    : vulvlakjes < 3 px (4-verbonden) -> meest voorkomende 4-buur uit dezelfde groep.
#  5 WIT     : areolen (witte stekeltjes) alleen waar het model ze heeft (>= 2 witte modelpx, niet het gat).
#  6 BUITENLIJN: 1 px; zwart aan de schaduwkant (normaal naar rechts/onder), selout aan de lichtkant
#              (links/boven); slagschaduw onder de kop (model zwart >= 5/9) blijft zwart; losse om-en-om-wissel
#              langs de rand rechtgezet.
# Bevroren (assert): ooggebied x 18-36 / y 22-27 en mond/kin/tandje x 18-34 / y 28-34.
import sys,numpy as np; from PIL import Image; from collections import Counter
from scipy import ndimage as nd; from skimage.morphology import skeletonize
from groepen import laad
UIT=sys.argv[1] if len(sys.argv)>1 else 'pitahaya_r7.png'
LT=70; DTZ=2; MINL=12; SP,SG=1.6,1.6
R6=Image.open('pitahaya_r6.png'); r6=np.asarray(R6).astype(int); pal=R6.getpalette()
a,lum,g=laad(); H,W=g.shape
def blok(Y,X): return slice(3*Y+6,3*Y+9),slice(3*X+4,3*X+7)
def bevr(y,x): return (18<=x<=36 and 22<=y<=27) or (18<=x<=34 and 28<=y<=34)
PINK=(2,3,4,5); GREEN=(8,9,10,11); FILL={2:(3,4,5),4:(9,10,11)}; SEL={2:2,4:8}
o=r6.copy(); log=[]
def zet(y,x,v,stap):
    assert not bevr(y,x),(y,x)
    if o[y,x]!=v: log.append((stap,y,x,o[y,x],v)); o[y,x]=v
# groep per spritepixel (2 roze, 4 groen) uit r6; zwart/wit -> meerderheid van het modelblok
grp=np.zeros((64,64),int)
for y,x in zip(*np.where(r6>0)):
    v=r6[y,x]
    if v in PINK: grp[y,x]=2
    elif v in GREEN: grp[y,x]=4
    else:
        b=g[blok(y,x)]; grp[y,x]=2 if (b==2).sum()+(b==3).sum()>(b==4).sum() else 4
# --- 2 gat
lab,n=nd.label(g==6); gatlab=[i for i in range(1,n+1) if (lab==i).sum()>=10]
GAT=np.isin(lab,gatlab)
for y,x in zip(*np.where(r6>0)):
    if not bevr(y,x) and GAT[blok(y,x)].sum()>=3: zet(y,x,0,'2 gat')
m=o>0
# --- 1 lijnen
NL=(g==1)|(((g==4)|(g==2))&(lum<LT))
sk=skeletonize(NL)
sl,ns=nd.label(sk,structure=np.ones((3,3)))
gr=nd.sum(sk,sl,range(1,ns+1)); klein=np.isin(sl,[i+1 for i,s in enumerate(gr) if s<MINL]); sk=sk&~klein
DT=nd.distance_transform_edt(g==1)     # halve dikte van de zwarte modellijn
LIJN=np.zeros((64,64),bool); ZWART=np.zeros((64,64),bool)
for y,x in zip(*np.where(m)):
    b=blok(y,x)
    if sk[b].any():
        LIJN[y,x]=True; ZWART[y,x]=DT[b][sk[b]].max()>=DTZ   # zwart alleen waar de modellijn >= 3 natieve px dik is
pad=np.pad(m,1); rand=m&~(pad[:-2,1:-1]&pad[2:,1:-1]&pad[1:-1,:-2]&pad[1:-1,2:])
# 1a kop over lijf: een modellijn met zwart die roze (kop) van groen (lijf) scheidt = onderrand van de kop,
#    schaduwkant -> zwart (zoals de buitenlijn aan de schaduwkant)
for y,x in zip(*np.where(LIJN)):
    b=blok(y,x); gb=g[b]
    if (gb==1).any() and ((gb==2)|(gb==3)).any()+((gb==4).any()) and 33<=y<=38:
        omg=grp[max(0,y-1):y+2,max(0,x-1):x+2]
        if (omg==2).any() and (omg==4).any(): ZWART[y,x]=True
# 1b dunnen: waar de projectie 2 px dik wordt (diagonaal over een blokgrens) -> skelet op spriteniveau, 1 px.
#    De buitenlijn telt mee als lijn (een binnenlijn die erop aansluit blijft eraan vast), het bevroren gebied ook.
#    Dikke modellijnen (>= 5/9 zwart: slagschaduw onder de kop, kontour arm) worden niet gedund.
NZ=np.zeros((64,64),int)
for y,x in zip(*np.where(m)): NZ[y,x]=(g[blok(y,x)]==1).sum()
DIK=LIJN&ZWART
BIN=LIJN&~rand
VAST=rand|DIK|np.array([[bevr(y,x) for x in range(64)] for y in range(64)])&(r6==1)
dun=skeletonize(BIN|VAST)
LIJN=(BIN&(dun|DIK))|(LIJN&rand)
WIT_OK=np.zeros((64,64),bool)
for y,x in zip(*np.where(m)):
    b=blok(y,x); WIT_OK[y,x]=((g[b]==6)&~GAT[b]).sum()>=2
# --- 3 vulling: toonkaart
def gauss(x,s): return nd.gaussian_filter(x,s,mode='constant')
TK={}
for G_,s in ((2,SP),(4,SG)):
    mg=((g==G_)|((G_==2)&(g==3))).astype(float) if G_==2 else (g==4).astype(float)
    mg=(g==G_).astype(float); TK[G_]=gauss(lum*mg,s)/np.maximum(gauss(mg,s),1e-6)
# modeltinten (groepen.tonen): roze 62/90/133/168, groen 73/99/123/159; vulling 3 tinten, donkerste valt in de schaduwtint
ML={2:np.array([62,90,133,168]),4:np.array([73,99,123,159])}
kand={}
for y,x in zip(*np.where(m)):
    if bevr(y,x) or rand[y,x] or LIJN[y,x] or o[y,x] in (6,12,13,14): continue
    G_=grp[y,x]; b=blok(y,x); gm=g[b]==G_
    if not gm.any(): gm=(g[b]==2)|(g[b]==4)|(g[b]==3)
    if not gm.any(): continue
    zone='kop' if y<=35 else 'lijf'
    kand.setdefault((G_,zone),[]).append((TK[G_][b][gm].mean() if (g[b]==G_).any() else lum[b][gm].mean(),y,x))
for (G_,zone),L in kand.items():
    # aandeel per tint in het model zelf: natieve vulpixels van deze groep in de blokken van deze kandidaten
    zm=np.zeros((H,W),bool)
    for _,y,x in L: zm[blok(y,x)]=True
    zm&=(g==G_)&(lum>=LT)
    t=np.abs(lum[zm][:,None]-ML[G_][None]).argmin(1); t[t==0]=1
    frac=np.array([(t==k).sum() for k in (1,2,3)],float); frac/=frac.sum()
    L.sort(); N=len(L); grens=np.round(np.cumsum(frac)*N).astype(int)
    for i,(_,y,x) in enumerate(L):
        k=int(i>=grens[0])+int(i>=grens[1]); zet(y,x,FILL[G_][k],'3 toonkaart')
    print('vulling',G_,zone,N,'aandeel model',frac.round(2))
if 'DBG' in sys.argv: np.save('dbg3.npy',o)
# lijnen zetten (binnen, niet bevroren)
for y,x in zip(*np.where(LIJN&~rand)):
    if bevr(y,x) or o[y,x] in (12,13): continue
    if WIT_OK[y,x] and o[y,x]==14: continue
    zet(y,x,1 if ZWART[y,x] else SEL[grp[y,x]],'1 lijn')
# --- 4 ruis
for it in range(4):
    nfix=0
    for v in (3,4,5,9,10,11):
        lab2,n2=nd.label(o==v)
        for i in range(1,n2+1):
            ys,xs=np.where(lab2==i)
            if len(ys)>=3: continue
            for y,x in zip(ys,xs):
                if bevr(y,x): continue
                G_=grp[y,x]; nb=[o[y+dy,x+dx] for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)) if o[y+dy,x+dx] in FILL[G_] and o[y+dy,x+dx]!=v]
                if nb: zet(y,x,Counter(nb).most_common(1)[0][0],'4 ruis'); nfix+=1
    if not nfix: break
# --- 5 wit
for y,x in zip(*np.where(m&~rand)):
    if bevr(y,x): continue
    if WIT_OK[y,x] and not ZWART[y,x] and o[y,x]!=14: zet(y,x,14,'5 wit')
    elif o[y,x]==14 and not WIT_OK[y,x]: zet(y,x,FILL[grp[y,x]][1],'5 wit')
# --- 6 buitenlijn
m=o>0; NB8=[(dy,dx) for dy in (-1,0,1) for dx in (-1,0,1) if dy or dx]
pad=np.pad(m,1); rand=m&~(pad[:-2,1:-1]&pad[2:,1:-1]&pad[1:-1,:-2]&pad[1:-1,2:])
kant={}
for y,x in zip(*np.where(rand)):
    ny=sum(dy for dy,dx in NB8 if not m[y+dy,x+dx]); nx=sum(dx for dy,dx in NB8 if not m[y+dy,x+dx])
    d=-(nx+ny)
    licht=d>0 or (d==0 and ny<0)
    b=blok(y,x)
    if y>=35 and (g[b]==1).sum()>=5 and r6[y,x]==1 and y<=38: licht=False   # slagschaduw onder de kop
    kant[(y,x)]=licht
# om-en-om: een randpixel waarvan beide randburen de andere kant hebben -> mee
for (y,x),l in list(kant.items()):
    nb=[kant[(y+dy,x+dx)] for dy,dx in NB8 if (y+dy,x+dx) in kant]
    if len(nb)>=2 and all(v!=l for v in nb): kant[(y,x)]=not l
for (y,x),l in kant.items():
    if bevr(y,x): continue
    zet(y,x,SEL[grp[y,x]] if l else 1,'6 buitenlijn')
p=Image.fromarray(o.astype('uint8'),'P'); p.putpalette(pal); p.save(UIT,transparency=0)
# bewijs bevroren
F=np.array([[bevr(y,x) for x in range(64)] for y in range(64)])
assert (o[F]==r6[F]).all(); print('bevroren diff 0 (oog + mond):',F.sum(),'px')
def zone(y,x):
    if y<=36: return 'kop'
    if 35<=x<=46 and 37<=y<=48: return 'rechterarm'
    if x<=24 and 37<=y<=47: return 'linkerarm'
    if y>=48: return 'poten'
    return 'romp'
last={}
for s,y,x,a_,b in log: last[(y,x)]=(s,last.get((y,x),(None,a_))[1] if (y,x) in last else a_,b)
fin={k:v for k,v in last.items() if r6[k]!=o[k]}
cnt=Counter((s,zone(*k)) for k,(s,_,_) in fin.items())
for k,v in sorted(cnt.items()): print(k,v)
print('totaal t.o.v. r6',(o!=r6).sum(),'silhouet-diff',((o>0)!=(r6>0)).sum())
open(UIT.replace('.png','_afwijkingen.txt'),'w').write('\n'.join(f'{s}\t({x},{y})\t{r6[y,x]}->{o[y,x]}\t{zone(y,x)}' for (y,x),(s,_,_) in sorted(fin.items(),key=lambda t:(t[0][0],t[0][1])))+'\n')
