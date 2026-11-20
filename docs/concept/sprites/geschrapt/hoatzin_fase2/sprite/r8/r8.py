# Hoatzin r8 = r7-pijplijn (gedeelde stappen, buiten de kop pixelgelijk aan r7 B), nieuw rond oog (Sharpedo) en kuif met volume.
# (oorspronkelijk r7:) Hoatzin r7 op r6 (silhouet bevroren, niets getekend: lijnen/vlakken uit modelmetingen, oog uit Latios Gen 3)
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
# oog: rond, Sharpedo (Gen 3) x25-29 y23-27 pixel voor pixel: ring -> ring, rood -> iris, wit midden -> pupil,
#      donkerrood linksboven -> glans, overig donkerrood -> iris; pupil op de modelplek (12,21)
SH=np.array(Image.open('/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/sharpedo/anim_front_gba.png'))[:64]
OOG={}
for y in range(23,28):
  for x in range(25,30):
    h='0123456789abcdef'[SH[y,x]]; q=(y-4,x-15)
    if h in 'e1': OOG[q]='ring'
    elif h=='c': OOG[q]='iris'
    elif h=='d': OOG[q]='pupil'
    elif h=='b': OOG[q]='glans' if (x,y)==(26,24) else 'iris'
face|=np.array([[ (y,x) in OOG for x in range(64)] for y in range(64)])
for y,x in zip(*np.where(face)):
    if (y,x) in OOG: continue
    buiten=any(not face[y+d,x+e] for d,e in N4)
    schaduw=any(not face[y+d,x+e] for d,e in ((1,0),(0,1)))   # rand alleen onder/rechts (schaduwkant)
    if S0[y,x]==1 and buiten: continue
    zet(S,y,x,8 if schaduw else 9,'A2 gezicht: vlak 9, rand 8 onder/rechts (vorm = modelblauw)')
def zet_oog(S2,ring):
    for (y,x),r in OOG.items(): S2[y,x]={'ring':ring,'iris':10,'pupil':1,'glans':5}[r]
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
# ---- kuif r8: plukken als taps toelopende vormen (plaats/richting/kromming uit het model, middellijnen T1-T7 gemeten
#      op het 1024-model, zie r7), elk met licht (linksboven), middentint, donkere schaduwkant en omlijning ----
KL=np.load('kuif_L.npy')
PAL[6]=tuple(int(v) for v in os.environ.get('P6','132,72,46').split(','))    # bruin midden
PAL[7]=tuple(int(v) for v in os.environ.get('P7','192,122,72').split(','))   # bruin licht; donker = 2 (gedeeld), lijn = 1
PLUK={  # naam: (middellijn basis -> punt, halve breedte basis, halve breedte punt)
 'T1':([(10.0,16.5),(6.1,8.7)],1.5,0.45),
 'T2':([(11.4,16.5),(11.2,6.3)],1.5,0.45),
 'T3':([(12.6,16.0),(14.9,10.1)],1.3,0.45),
 'T4':([(13.2,16.2),(18.0,11.4),(23.2,7.4)],1.6,0.45),
 'T5':([(14.5,15.2),(23.4,12.6),(26.8,12.2)],1.4,0.45),
 'T6':([(15.0,16.6),(24.0,15.6),(25.8,16.4),(30.1,19.2)],1.5,0.45),
 'T7':([(15.0,18.2),(26.7,21.8)],1.5,0.45),
}
def pluk(pl,w0,w1):
    P_=np.array(pl,float); seg=np.diff(P_,axis=0); L_=np.r_[0,np.cumsum(np.hypot(*seg.T))]; tot=L_[-1]
    d=np.full((64,64),9.0); n=np.zeros((64,64)); tt=np.zeros((64,64))
    for y in range(64):
      for x in range(64):
        p=np.array([x+0.5,y+0.5]); best=None
        for i,(a_,v) in enumerate(zip(P_[:-1],seg)):
            l2=v@v; t=np.clip((p-a_)@v/l2,0,1); q=a_+t*v; dd=np.hypot(*(p-q))
            if best is None or dd<best[0]:
                nrm=np.array([v[1],-v[0]])/np.sqrt(l2)          # normaal
                if nrm[0]+nrm[1]>0: nrm=-nrm                      # naar linksboven (lichtkant)
                best=(dd,(p-q)@nrm,(L_[i]+t*np.sqrt(l2))/tot)
        d[y,x],n[y,x],tt[y,x]=best
    hw=w0+(w1-w0)*tt
    return (d<=hw)&(tt<1.0+1e-6), n/np.maximum(hw,0.3), tt
WB=float(os.environ.get('WB',0.8))
PLUK={k:(v[0],v[1]+WB,v[2]+0.05) for k,v in PLUK.items()}
PL={k:pluk(*v) for k,v in PLUK.items()}
basis=kz&(K[0]>=0.55)&(yy>=14)&(xx<=16)&(yy<=19)
TK=np.where(KL>0,KL,50.0); TMED=float(np.median(KL[(K[0]>=0.3)&kz]))
def bouw(var):
    S2=BASIS.copy()
    for y,x in zip(*np.where(kz&~rand)): S2[y,x]=achter(y,x)          # vleugel erachter (rustig vlak)
    namen=['T7','T6','T5','T4','T3','T2','T1'] if var!='P2' else ['T7','T6','T4','T2','T1']
    eig=np.zeros((64,64),int); nn=np.zeros((64,64))
    m_all=basis.copy()
    for y,x in zip(*np.where(basis)): nn[y,x]=0.35-((xx[y,x]-12)+(yy[y,x]-15))*0.12; eig[y,x]=99
    for k,naam in enumerate(namen):
        m,nv,tv=PL[naam]; m=m&kz
        if var=='P2': m=pluk(PLUK[naam][0],PLUK[naam][1]+0.4,0.6)[0]&kz; nv=pluk(PLUK[naam][0],PLUK[naam][1]+0.4,0.6)[1]
        for y,x in zip(*np.where(m)): eig[y,x]=k+1; nn[y,x]=nv[y,x]
        m_all|=m
    # tonen: lichtkant licht, midden/schaduwkant midden, modeltoon schuift mee (donker model -> 1 stap donkerder)
    for y,x in zip(*np.where(m_all)):
        s_=nn[y,x]+(TK[y,x]-TMED)/float(os.environ.get('TM',120))
        S2[y,x]=7 if s_>float(os.environ.get('S1',-0.2)) else 6 if s_>float(os.environ.get('S2',-0.75)) else 2
    # randen per pluk: schaduwkant (onder/rechts grenst aan iets anders) donker 2, buitenrand tegen achtergrond 1
    for y,x in zip(*np.where(m_all)):
        if rand[y,x]:
            S2[y,x]=1 if any(not ok(y+d,x+e) or not fg[y+d,x+e] for d,e in ((1,0),(0,1))) else 6; continue
        if any(ok(y+d,x+e) and not m_all[y+d,x+e] for d,e in ((1,0),(0,1))) and var!='K1': S2[y,x]=2
    if var=='K1':   # hele haardos als één geheel omlijnd: zwart aan de schaduwkant, donkere selout (2) aan de lichtkant
        for y,x in zip(*np.where(m_all)):
            buiten=[(d,e) for d,e in N4 if not ok(y+d,x+e) or not m_all[y+d,x+e]]
            if buiten: S2[y,x]=1 if any(d==1 or e==1 for d,e in buiten) else 2
        # binnen: tussen de plukken schaduw (donker) waar een pluk over een andere valt
        for y,x in zip(*np.where(m_all)):
            if S2[y,x] in (6,7) and any(ok(y+d,x+e) and m_all[y+d,x+e] and eig[y+d,x+e]!=eig[y,x] and eig[y+d,x+e]<eig[y,x] for d,e in ((1,0),(0,1))): S2[y,x]=2
    return S2
out={}
VARS=os.environ.get('VARS','K1,P1,P2').split(',')
for kv in VARS:
    S2k=bouw(kv)
    for ov,ring in (('A',1),('B',8)):
        S2=S2k.copy(); zet_oog(S2,ring)
        assert ((S2!=0)==fg).all()
        im=Image.fromarray(S2.astype('uint8'),'P'); flat=[v for c_ in PAL for v in c_]; im.putpalette(flat+[0]*(768-len(flat)))
        im.save('kop_%s_oog%s.png'%(kv,ov),transparency=0)
R7=np.array(Image.open('r7.png')); kopz=kz|face|snavel
for kv in VARS:
    a_=np.array(Image.open('kop_%s_oogA.png'%kv))
    print(kv,'buiten kopzone anders dan r7 B:',int(((a_!=R7)&~kopz).sum()),' in kopzone:',int(((a_!=R7)&kopz).sum()))
with open('normal.pal','w') as f: f.write('JASC-PAL\n0100\n16\n'+''.join('%d %d %d\n'%tuple(c_) for c_ in PAL))
np.save('kuifzone.npy',kz)
