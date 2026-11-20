# Hoatzin r7 op r6 (silhouet bevroren, niets getekend: lijnen/vlakken uit modelmetingen, oog uit Latios Gen 3)
# Gedeeld (alle varianten gelijk): B5/B6 vleugelwaaier (pengrens + schacht uit het model), B7 donkere onderkant
# (diagonale lijnen uit het model), C buiklicht, A1 oog, A2 blauw gezicht, A4 snavel.
# Kopvarianten (alleen kuifzone verschilt): A ±7 dunne strengen, B 5 strengen van 2 px, C donkere strengen + kuifmassa.
import os, sys, json, numpy as np; from PIL import Image
from frac import *
from lijnen import lijnen, FS, FG, box
SRC=Image.open('r6.png'); S0=np.array(SRC).astype(int)
PAL=[tuple(SRC.getpalette()[3*i:3*i+3]) for i in range(16)]
Zt=np.load('../r4/zone_t.npy'); Z=np.full((64,64),'.',dtype='<U1'); Z[1:,6:57]=Zt
fg=S0!=0; pad=np.pad(fg,1); rand=fg&~(pad[:-2,1:-1]&pad[2:,1:-1]&pad[1:-1,:-2]&pad[1:-1,2:])
yy,xx=np.mgrid[:64,:64]
N4=((-1,0),(1,0),(0,-1),(0,1)); N8=[(i,j) for i in (-1,0,1) for j in (-1,0,1) if i or j]
ok=lambda y,x: 0<=y<64 and 0<=x<64
log={}
def zet(S,y,x,v,regel):
    if not fg[y,x]: return
    if S[y,x]!=v: log[regel]=log.get(regel,0)+1; S[y,x]=v
S=S0.copy()
# ================= B5/B6 vleugelwaaier =================
fan=(xx>=36)&(xx<=56)&(yy>=2)&(yy<=18)&np.isin(S0,[3,4,5])&~rand
voorrand=(S0==5)&(xx<=42)&(yy<=8)
for y,x in zip(*np.where(fan&(S0==5)&~voorrand)): zet(S,y,x,3,'B6 oude streep in waaier weg (wordt modelschacht)')
STR=lijnen(FS,0.30,fan,3)
for l in STR:
    for y,x in l: zet(S,y,x,5,'B6 schacht uit het model (1 px per rij)')
GR=lijnen(FG,0.45,fan&(S!=5),3)
ng=0
for l in GR:
    for y,x in l:
        if S[y,x]==5: continue
        # index 3/4 aan beide kanten; grenst hij aan een schacht (5), dan 1 px verder van de schacht af
        for xx_ in (x, x-1 if ok(y,x+1) and S[y,x+1]==5 else x+1):
            if not ok(y,xx_) or not fan[y,xx_] or S[y,xx_] not in (3,4): continue
            lr=[S[y,xx_+d] for d in (-1,1) if ok(y,xx_+d)]
            if all(v in (3,4) for v in lr):
                zet(S,y,xx_,2,'B5 pengrens uit de modelgroef (1 px, 3 aan beide kanten)'); ng+=1; break
for y in range(63):
  for x in range(63):
    b=[(y,x),(y,x+1),(y+1,x),(y+1,x+1)]
    if all(S[q]==2 for q in b) and fan[y,x]: zet(S,y,x,3,'B5 2x2 weg')
# ================= B7 donkere vleugelonderkant =================
DK=frac(fgn&(Ln<30)&np.isin(Zn,['M','K','W','D']))
onder=(xx>=34)&(xx<=50)&(yy>=25)&(yy<=33)&np.isin(S0,[1,2])&~rand
for y,x in zip(*np.where(onder)): S[y,x]=2
lijn=onder&(DK>=0.30)
for it in range(3):
    for y in range(63):
      for x in range(63):
        b=[q for q in [(y,x),(y,x+1),(y+1,x),(y+1,x+1)] if lijn[q]]
        if len(b)>=3:
            q=min(b,key=lambda q:DK[q]); lijn[q]=False
# losse stukjes (< 3 px, 8-verbonden) weg
seen=np.zeros_like(lijn)
for y,x in zip(*np.where(lijn)):
    if seen[y,x]: continue
    st=[(y,x)]; c=[]; seen[y,x]=1
    while st:
        a,b=st.pop(); c.append((a,b))
        for d,e in N8:
            q,r=a+d,b+e
            if ok(q,r) and lijn[q,r] and not seen[q,r]: seen[q,r]=1; st.append((q,r))
    if len(c)<3:
        for q in c: lijn[q]=False
for y,x in zip(*np.where(onder)):
    zet(S,y,x,1 if lijn[y,x] else 2,'B7 onderkant: modellijn 1 px, rest vlak' )
for y,x in zip(*np.where(onder)):
    if S0[y,x]!=S[y,x]: pass
# ================= C buiklicht =================
P=fgn&(Zn=='P'); BL=mean(box(Ln,P,3),P)
bz=(xx>=17)&(xx<=25)&(yy>=36)&(yy<=44)&np.isin(S0,[12,13])&~rand
n13=int((S0[bz]==13).sum())
# lichtvlek van het model als ellips: gewogen momenten van de gladde modeltoon (BL >= 124) in de buik, cellen op Mahalanobis-afstand
qs=[q for q in zip(*np.where(bz)) if BL[q]>=124]; w=np.array([BL[q]-123 for q in qs])
X=np.array([[q[1]+0.5,q[0]+0.5] for q in qs]); mu=(X*w[:,None]).sum(0)/w.sum()
C=np.cov(X.T,aweights=w)+np.eye(2)*0.25; Ci=np.linalg.inv(C)
def md(q): d=np.array([q[1]+0.5,q[0]+0.5])-mu; return d@Ci@d
print('buiklicht model-ellips midden',mu.round(2))
cells=sorted(zip(*np.where(bz)),key=md)
top=set(cells[:n13])
for q in cells: zet(S,q[0],q[1],13 if q in top else 12,'C buiklicht = ellips van de modellichtvlek, zelfde aantal px')
# ================= A2 gezicht / A1 oog / A4 snavel =================
R_,G_,B_=N[...,0],N[...,1],N[...,2]
FF=frac(fgn&(B_-R_>=20)&(B_-G_>=25))
kop=(xx<=17)&(yy>=17)&(yy<=27)
face=kop&fg&((FF>=0.4)|(np.isin(S0,[8,9])&(FF>=0.25))|((S0==10)|((S0==1)&(xx>=10)&(xx<=14)&(yy>=19)&(yy<=23)&~rand)))   # + oude oogpixels
# oog: Latios (Gen 3, rood oog op blauw gezicht) pixel voor pixel, kern x9-13 y17-21 -> pupil op de modelplek
LA=np.array(Image.open('/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/latios/anim_front_gba.png'))[:64]
OX,OY=int(os.environ.get('OX',1)),int(os.environ.get('OY',2))
MAP={'e':8,'8':10,'7':10,'6':1,'f':1,'a':int(os.environ.get('OOGWIT',10))}
GLANS=(12,18)   # Latios-wit rechtsboven = glans; overige wit -> rood (geen oogwit, SPEC)
oog={}
for y in range(17,22):
  for x in range(9,14):
    h='0123456789abcdef'[LA[y,x]]
    if h in MAP: oog[(y+OY,x+OX)]=5 if (x,y)==GLANS else MAP[h]
face|=np.array([[ (y,x) in oog for x in range(64)] for y in range(64)])
for y,x in zip(*np.where(face)):
    if (y,x) in oog: continue
    buiten=any(not face[y+d,x+e] for d,e in N4)
    schaduw=any(not face[y+d,x+e] for d,e in ((1,0),(0,1)))   # rand alleen onder/rechts (schaduwkant)
    if S0[y,x]==1 and buiten: continue
    zet(S,y,x,8 if schaduw else 9,'A2 gezicht: vlak 9, rand 8 onder/rechts (vorm = modelblauw)')
for (y,x),v in oog.items(): zet(S,y,x,v,'A1 oog uit Latios')
# snavel
LM=mean(Ln,fgn)
snavel=(xx>=6)&(xx<=12)&(yy>=22)&(yy<=27)&fg&~face&~((xx==12)&(yy==25))
for y,x in zip(*np.where(snavel)):
    if rand[y,x]: zet(S,y,x,1,'A4 snavel: donkere rand'); continue
    zet(S,y,x,15 if LM[y,x]>=95 else 14,'A4 snavel: e vlak, f waar het model licht is (>= 95, de rug)')
BASIS=S.copy()
# ================= kuif =================
K=np.load('kuif_t.npy')
kz=(xx<=28)&(yy<=22)&fg&~face&~snavel&~((xx>=29))
kz&=~((yy>=19)&(xx<=8))   # snavelhoek links
kz&=np.isin(S0,[2,3,4,6,7,1])
# achtergrond: vleugel/rug erachter, toon uit de modelkaart zonder bruin (r6-drempels 63/94)
mm=np.isin(Zn,['M','W'])&~np.load('../r4/lijn_nat.npy')&~np.load('../r4/streep_nat.npy')
T=mean(box(Ln,mm,4),mm)
def achter(y,x):
    t=T[y,x]
    if t<=0: return 3
    return 2 if t<63 else 3 if t<94 else 4
massa=kz&(K[0]>=float(os.environ.get('MK',0.55)))&(yy>=14)&(xx<=17)&~rand
STRENG={
 'T1':[(6.1,8.7),(9.9,14.8)],
 'T2':[(11.2,6.3),(11.1,14.8)],
 'T3':[(14.9,10.1),(11.8,15.5)],
 'T4':[(23.2,7.4),(12.6,15.6)],
 'T5':[(26.8,12.2),(23.4,12.6),(15.5,13.9)],
 'T6':[(30.1,19.2),(25.8,16.4),(24.0,15.4),(16.0,15.3)],
 'T7':[(15.0,17.5),(26.7,21.8)],
}
def raster(pl):
    c=[]
    for (x1,y1),(x2,y2) in zip(pl,pl[1:]):
        n=int(max(abs(x2-x1),abs(y2-y1))*8)+1
        for k in range(n+1):
            q=(int(np.floor(y1+(y2-y1)*k/n)),int(np.floor(x1+(x2-x1)*k/n)))
            if not c or c[-1]!=q: c.append(q)
    # trapjes weg: als buren i-1 en i+1 diagonaal raken, i overslaan
    out=[]
    for i,q in enumerate(c):
        if out and i+1<len(c) and max(abs(c[i+1][0]-out[-1][0]),abs(c[i+1][1]-out[-1][1]))==1: continue
        out.append(q)
    return [q for q in out if ok(*q)]
def bouw(var):
    S2=BASIS.copy(); lg={}
    def z(y,x,v,r):
        if S2[y,x]!=v and fg[y,x]: lg[r]=lg.get(r,0)+1; S2[y,x]=v
    for y,x in zip(*np.where(kz&~rand)): z(y,x,achter(y,x),'kuif achtergrond = vleugel (modeltoon)')
    for y,x in zip(*np.where(kz&rand&np.isin(S0,[6,7]))): z(y,x,6,'kuif rand bruin -> donkerbruin')
    if var=='A':
        for y,x in zip(*np.where(massa)): z(y,x,6,'massa donkerbruin')
        for n in ['T1','T2','T3','T4','T5','T6','T7']:
            for y,x in raster(STRENG[n]):
                if kz[y,x]: z(y,x,6 if rand[y,x] else 7,'streng 1 px licht (donker op de rand)')
    if var=='B':
        for y,x in zip(*np.where(massa)): z(y,x,6,'massa donkerbruin')
        for n in ['T1','T2','T4','T5','T6']:
            pl=STRENG[n]; cel=raster(pl)
            steil=abs(pl[-1][1]-pl[0][1])>abs(pl[-1][0]-pl[0][0])
            for y,x in cel:
                if not kz[y,x]: continue
                z(y,x,6 if rand[y,x] else 7,'streng 2 px: licht')
                q=(y,x+1) if steil else (y+1,x)
                if ok(*q) and kz[q] and q not in cel: z(q[0],q[1],6,'streng 2 px: donkere rand (schaduwkant)')
    if var=='C':
        mC=kz&(K[0]>=0.5)&(yy>=14)&~rand
        for y,x in zip(*np.where(mC)): z(y,x,7,'massa licht (bruin model >= 50%)')
        for n in ['T1','T2','T3','T4','T5','T6','T7']:
            for y,x in raster(STRENG[n]):
                if kz[y,x]: z(y,x,6,'streng 1 px donkerbruin (zoals het model)')
    return S2,lg
out={}
for var in 'ABC':
    S2,lg=bouw(var)
    assert ((S2!=0)==fg).all()
    im=Image.fromarray(S2.astype('uint8'),'P'); flat=[v for c in PAL for v in c]; im.putpalette(flat+[0]*(768-len(flat)))
    im.save('kop_%s.png'%var,transparency=0); out[var]={'log':lg,'anders_dan_r6':int((S2!=S0).sum())}
# kopzone-diff tussen varianten
A_,B_,C_=[np.array(Image.open('kop_%s.png'%v)) for v in 'ABC']
d=(A_!=B_)|(A_!=C_)|(B_!=C_)
print('varianten verschillen buiten kuifzone:',int((d&~kz).sum()))
print('strepen in waaier:',len(STR),'pengrenzen:',len(GR),ng,'px')
print(json.dumps(log,indent=1,ensure_ascii=False)); print(json.dumps(out,indent=1,ensure_ascii=False))
np.save('kuifzone.npy',kz)
