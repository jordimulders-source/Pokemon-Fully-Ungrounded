# r8 (kopie van r7/maak7.py; varianten via pijp/common.CFG, PB-voor-PA algemeen i.p.v. vaste rijen)
# r7: van bouw7-uitvoer (= r4-regels op het model met vergrote oogbollen) naar de eindsprite.
#   stap 2  r5-MOET-fixes (sprite/r5/fix5.py)      alleen buiten de bolzones en alleen als de pixel nog gelijk is aan r4
#   stap 3  r5-eindkeuring DFC (eindkeuring_r5/ek5.py) idem, alleen als de pixel nog de 'oud'-waarde heeft
#   stap 3b bolzones: r4-omlijningsregel (zwart als transparant onder/rechts, anders navy) ook op pixels die in kaal al donker waren (ek5-fouttype)
#   stap 4  r6-kleurregels (kleur_r6/kleur6.py), DONKER4 algemeen: r5-index 4 waar het verkleinde model L(601)<100
#   stap 5  mastpaneel PB voor paneel PA (zoals in het model)
#   stap 6  paneelrecept van fase 2 (alleen kleur, geen vorm)
# Gebruik: python3 maak7.py 120|130|100   (100 = controle: stap 2-4 moeten kleur_r6/sprite.png exact teruggeven)
import os, sys, numpy as np
from PIL import Image
from collections import Counter
H=os.path.dirname(os.path.abspath(__file__)); R=os.path.normpath(os.path.join(H,'..','..'))
VAR=sys.argv[1]
WD=os.path.join(H,'w_'+VAR) if VAR.startswith('s') else sys.argv[2]
sys.path.insert(0,os.path.join(H,'pijp')); os.environ['VAR']=VAR
from common import KF,KS,KP
KB={'voor':KF,'links':KS,'rechts':KS}
S=3.515625; TOP=13
A=np.array(Image.open(os.path.join(WD,'sprite.png'))).astype(int)      # bouw7 (r4-equivalent)
KAAL=np.array(Image.open(os.path.join(WD,'kaal.png'))).astype(int)
OWNK=np.full((64,64),'',object); o=np.load(os.path.join(WD,'ownk.npy')); OWNK[TOP:TOP+o.shape[0]]=o
R4=np.array(Image.open(os.path.join(R,'sprite','r4','sprite.png'))).astype(int)
LOG=[]
def zet(B,x,y,c,stap,deel,reden):
    if B[y,x]!=c: LOG.append((x,y,int(B[y,x]),int(c),stap,deel,reden)); B[y,x]=c
# bolzones (spritecoordinaten): middelpunt en buitenstraal van de vergrote bollen (+1 px marge)
BOLM={'voor':(62.16,127.95,21.12),'links':(75.01,64.28,11.25),'rechts':(188.46,91.70,12.48)}
def bolc(n,cx):   # r8: linkerbol geschaald vanuit x=79 (kraagkant), zie model8.py
    return 79+(cx-79)*KS if (n=='links' and VAR.startswith('s')) else cx
ZONE={n:((bolc(n,cx)-3)/S,(cy-3)/S+TOP,r*KB[n]/S) for n,(cx,cy,r) in BOLM.items()}
def inzone(x,y,m=1.0):
    if VAR=='100': return None
    for n,(cx,cy,r) in ZONE.items():
        if np.hypot(x+.5-cx,y+.5-cy)<=r+m: return n
    return None
B=A.copy()
# ---- stap 2: fix5
FIX5={2:[(46,21),(38,26),(39,26),(40,26),(33,28),(27,35),(24,37),(50,35),(17,41),(27,34),(17,29),(34,17),(26,20),(30,21),(52,29),(56,30)],
      1:[(22,50),(36,42),(37,43),(37,47),(49,39),(50,40),(37,23)]}
OVERGESLAGEN=[]
for c,l in FIX5.items():
    for x,y in l:
        z=inzone(x,y)
        if z or B[y,x]!=R4[y,x]: OVERGESLAGEN.append(('fix5',x,y,z or 'pixel anders dan r4')); continue
        zet(B,x,y,c,'r5','fix5','MOET-reparatie keuring_r4 (ongewijzigd overgenomen)')
# ---- stap 3: ek5
src=open(os.path.join(R,'eindkeuring_r5','ek5.py')).read()
FIX=eval(src[src.index('FIX=[')+4:src.index(']\nsrc=')+1])
for x,y,oud,nieuw,reden in FIX:
    z=inzone(x,y)
    if z or B[y,x]!=oud: OVERGESLAGEN.append(('ek5',x,y,z or 'oud %d, nu %d'%(oud,B[y,x]))); continue
    zet(B,x,y,nieuw,'ek5','ek5',reden)
# ---- stap 3b: bolranden in de bolzones, regel uit ek5 ('zwart aan de lichtkant -> navy'; schaduwkant zwart)
if VAR!='100':
    for y in range(64):
        for x in range(64):
            if B[y,x] not in (1,2): continue
            n=inzone(x,y,0.6)
            if not n: continue
            cx,cy,r=ZONE[n]
            leeg=[(dy,dx) for dy,dx in ((0,-1),(-1,0),(0,1),(1,0)) if not(0<=y+dy<64 and 0<=x+dx<64) or B[y+dy,x+dx]==0]
            if not leeg or OWNK[y,x]: continue
            schaduw=any(d in leeg for d in ((1,0),(0,1)))   # r4-regel stap 4: transparant onder/rechts = schaduwkant
            zet(B,x,y,1 if schaduw else 2,'bol','bol_'+n,'bolomlijning r4-regel: '+('schaduwkant zwart' if schaduw else 'lichtkant navy (ek5: zwart op de lichtkant -> navy)'))
# ---- stap 4: kleur6
from PIL import Image as _I
import importlib.util
from common import M as _M
m=np.array(_I.open(_M).convert('RGB')).astype(float)
import kaal
OH=KAAL.shape[0]
Wx=kaal.overlap(64,3,S,m.shape[1]); Wy=kaal.overlap(64-TOP,3,S,m.shape[0])
L601=sum(w*(Wy@m[:,:,c]@Wx.T/(S*S)) for c,w in enumerate((0.299,0.587,0.114)))
PAL6={0:(0,0,0),1:(24,19,36),2:(41,38,69),3:(60,48,96),4:(150,138,186),5:(206,198,228),6:(80,44,104),7:(116,70,142),
      8:(156,100,182),9:(38,104,110),10:(86,182,174),11:(58,52,104),12:(120,106,172),13:(0,0,0),14:(0,0,0),15:(248,248,252)}
C=np.zeros_like(B); PANEL={1,2,5}
def nb(A_,y,x): return [A_[y+dy,x+dx] if 0<=y+dy<64 and 0<=x+dx<64 else 0 for dy,dx in ((-1,0),(1,0),(0,-1),(0,1))]
for y in range(64):
    for x in range(64):
        v=B[y,x]; n=nb(B,y,x)
        if v==0: continue
        if v==15: c=15
        elif v in (14,13): c=5
        elif v in (12,11): c=4
        elif v==4: c=3 if (y>=TOP and L601[y-TOP,x]<100) else 4
        elif v==5: c=12 if sum(q in PANEL for q in n)>=3 else 3
        elif v==2: c=11 if all(q in PANEL for q in n) else 2
        else: c=v
        C[y,x]=c
        if c!=v and not (v in (6,7,8,9,10,1,3) ): pass
R6=C.copy(); K6=Counter((int(b_),int(c_)) for b_,c_ in zip(B.ravel(),C.ravel()) if b_ and b_!=c_)
# ---- stap 5: PB voor PA. Model: mast PB (x 123-132) ligt voor PA. Spritekolommen PB: v=0,14 -> x34 (lichte rand), v=0,53 -> x35 (vak),
#      v=0,92 -> x36 (schaduwrand). Overlap met PA: rijen 22-25 (uv-meting lijnen.uv, RAPPORT); rij 21 krijgt de 2e dwarslijn (u=0,66).
from lijnen import uv
def puv(k,x,y): return uv(k,3+(x+.5)*S,3+(y-TOP+.5)*S)
D=C.copy()
if VAR!='100':
    # algemeen (r8, panelen breder): elke PA-pixel binnen PB (uv in [0,1]) wordt PB: kolom zonder PB links = lichte rand (navy),
    # zonder PB rechts = schaduwrand (zwart), anders vak; dwarslijnen van PB op u=1/3 en 2/3 (zelfde grens als bouw stap 3)
    def inPB(x,y):
        u,v=puv('PB',x,y); return -0.02<=u<=1.02 and 0<=v<=1
    def inPA(x,y):
        u,v=puv('PA',x,y); return -0.02<=u<=1.02 and -0.05<=v<=1.05
    lim=S/47/2*1.0
    for y in range(TOP,64):
        for x in range(64):
            if OWNK[y,x] not in ('PA','PB') or not (inPB(x,y) and inPA(x,y)): continue
            u,v=puv('PB',x,y)
            if not inPB(x-1,y): c=2
            elif not inPB(x+1,y): c=1
            elif min(abs(u-1/3),abs(u-2/3))<=lim+0.005: c=12
            else: c=11
            zet(D,x,y,c,'PB','PB','mastpaneel PB voor PA (model): '+{2:'lichte rand',11:'vak',1:'schaduwrand zwart',12:'dwarslijn'}[c])
            OWNK[y,x]='PB'
# ---- stap 6: paneelrecept fase 2 (exacte fase 2-paneelkleuren)
PAL=dict(PAL6); PAL[11]=(44,34,84); PAL[13]=(84,76,150); PAL[14]=(112,104,182); PAL[12]=(170,158,222)
# vaktint per vak (tussen de dwarslijnen), licht -> donker langs het paneel van linksboven naar rechtsonder.
# voorpanelen (PD, PE) 14,13,13,11; masten PF 14,13,11 en PB 14,13,13; achterpanelen achter de romp (PA, PC): 13,13,11,11
#   (fase 2: het achterpaneel is donker: vak 9 met A-lijnen). Lijnen op een donker vak (11) worden 14 (fase 2: B-lijnen op 9).
TINT={'PD':[14,13,13,11],'PE':[14,13,13,11],'PA':[13,13,11,11],'PC':[13,13,11,11],'PB':[14,13,13],'PF':[14,13,11]}   # PB onderste vak midden i.p.v. donker: ligt voor het donkere PA-uiteinde
LIJN={'PA':[.25,.5,.75],'PC':[.25,.5,.75],'PD':[.25,.5,.75],'PE':[.25,.5,.75],'PB':[1/3,2/3],'PF':[1/3,2/3]}
E=D.copy()
if VAR!='100':
    for y in range(64):
        for x in range(64):
            k=OWNK[y,x]
            if not k or D[y,x] not in (11,12): continue
            u,v=puv(k,x,y)
            # richting: vak 0 = het uiteinde linksboven (GEO T ligt voor alle panelen linksboven, PB/PF bovenaan)
            i=int(np.clip(np.searchsorted(LIJN[k],u),0,len(TINT[k])-1))
            vt=TINT[k][i]
            if D[y,x]==11: zet(E,x,y,vt,'paneel',k,'vak %d: tint %s'%(i+1,{14:'licht',13:'midden',11:'donker'}[vt]))
            else: zet(E,x,y,14 if vt==11 else 12,'paneel',k,'rasterlijn lichter dan het vak'+(' (B op donker vak, fase 2)' if vt==11 else ''))
    # lichte rand (12) langs de lichte rand: vakpixel direct onder/rechts van de navy lichtrand, alleen als er nog een vakpixel achter ligt
    F=E.copy()
    for y in range(64):
        for x in range(64):
            k=OWNK[y,x]
            if not k or E[y,x] not in (14,13,11): continue
            for dy,dx in ((-1,0),(0,-1)):
                yy,xx=y+dy,x+dx; y2,x2=y-dy,x-dx
                if 0<=yy<64 and 0<=xx<64 and E[yy,xx]==2 and 0<=y2<64 and 0<=x2<64 and OWNK[y2,x2]==k and E[y2,x2] in (14,13,11):
                    zet(F,x,y,12,'paneel',k,'lichte rand langs de lichtkant (fase 2)'); break
    E=F
OUT=E
assert ((A>0)!=(OUT>0)).sum()==0 or VAR=='100'
def save(arr,pal,path):
    im=Image.fromarray(arr.astype(np.uint8),'P'); flat=[c for i in range(16) for c in pal[i]]; im.putpalette(flat); im.save(path,transparency=0)
if VAR=='100':
    r6=np.array(Image.open(os.path.join(R,'kleur_r6','sprite.png')))
    print('controle VAR=100: verschil met kleur_r6/sprite.png =',int((r6!=R6).sum()),'pixels'); sys.exit()
if VAR=='130':
    r7=np.array(Image.open(os.path.join(R,'sprite','r7','sprite_bol130.png')))
    print('controle VAR=130: verschil met r7/sprite_bol130.png =',int((r7!=OUT).sum()),'pixels',[(x,y,r7[y,x],OUT[y,x]) for y,x in zip(*np.where(r7!=OUT))]); sys.exit()
tag=VAR
save(OUT,PAL,os.path.join(H,'sprite_%s.png'%tag))
P=np.array([PAL[i] for i in range(16)],np.uint8)
def rgb(arr,bg=(235,240,235)):
    r=P[arr]; r[arr==0]=bg; return Image.fromarray(r)
rgb(OUT).resize((512,512),Image.NEAREST).save(os.path.join(H,'sprite_%s_8x.png'%tag))
save(R6,PAL6,os.path.join(WD,'stap4_r6regels.png')); save(D,PAL6,os.path.join(WD,'stap5_pb.png'))
# ---- rondheid bollen: buitenrand (pixel grenst aan transparant) binnen de bolsector tegen de achtergrond
RND={}
SECT={'voor':((30,200),),'links':((90,265),),'rechts':((350,360),(0,120))}   # r8: links boven 265 = onderrand PA, rechts 300-350 = paneel PC
for n,(cx,cy,r) in ZONE.items():
    dev=[]
    for y in range(64):
        for x in range(64):
            if OUT[y,x]==0: continue
            if not any(not(0<=y+dy<64 and 0<=x+dx<64) or OUT[y+dy,x+dx]==0 for dy,dx in ((0,-1),(-1,0),(0,1),(1,0))): continue
            a_=np.degrees(np.arctan2(y+.5-cy,x+.5-cx))%360
            if not any(lo<=a_<=hi for lo,hi in SECT[n]): continue
            d=np.hypot(x+.5-cx,y+.5-cy)
            if abs(d-r)<=2.5: dev.append(d-(r-0.5))
    RND[n]=(len(dev),round(min(dev),2),round(max(dev),2),round(float(np.mean(dev)),2))
# ---- log
with open(os.path.join(WD,'log_maak8.txt'),'w') as f:
    f.write('x y oud->nieuw stap onderdeel reden (volle spritecoordinaten)\n')
    for l in LOG: f.write('%d %d %d->%d %s %s %s\n'%l)
    f.write('\nOVERGESLAGEN (bolzone of pixel al anders)\n')
    for l in OVERGESLAGEN: f.write('%s %d %d %s\n'%l)
    f.write('\nTELLING per stap/onderdeel\n')
    for (st,dl),n in sorted(Counter((l[4],l[5]) for l in LOG).items()): f.write('%-7s %-10s %d\n'%(st,dl,n))
    f.write('\nRONDHEID (aantal randpixels, min/max afwijking t.o.v. cirkel r-0,5 in px): %s\n'%RND)
    f.write('kleuren %d (incl. transparant)\n'%len(np.unique(OUT)))
    f.write('stap 4 (r6-kleurregels) indexwissels: %d %s\n'%(sum(K6.values()),sorted(K6.items())))
print(VAR,'kleuren',len(np.unique(OUT)),'rond',RND,'overgeslagen',len(OVERGESLAGEN))
print(sorted(Counter((l[4],l[5]) for l in LOG).items()))
