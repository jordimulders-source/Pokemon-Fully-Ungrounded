# r11 (25 nov): gerichte reparaties op r10/sprite.png, rest pixel-gelijk.
# Jordi over r10: "de ogen zijn nu zwarte vierkanten, allemaal dezelfde grootte en zelfde blik, dit moet nog wat meer
#   driekwart, vooral de zijwaartse ogen. Rechterbol is niet goed bol, het maakt niet uit dat die dan het paneel overlapt.
#   Kijk naar hoe het model dat doet. Bovenste paneel is een beetje afgekapt, onderste moet ook nog net wat verder doorlopen"
# 1 ogen: vorm per oog uit het model (model_gekozen.png = r13b, echte ogen) verkleind met de bolschaal (voor 1,3/s, zij
#   1,8/s; s = 3,515625), zij-ogen horizontaal extra verkort (KX); klasse per spritepixel = modeldekking (ring/iris/pupil),
#   tint = modeltint per klasse. Geen wit binnen de ring.
# 2 rechterbol: volle cirkel (middelpunt/straal van r10), voor paneel PC en de buis; tint nieuwe pixels uit de kale reductie.
# 3 mast PB: punt linksboven (eindkap) terug (rij 13, zoals de kale reductie).
# 4 mast PF: volle lengte 47 (= PB, 3 gelijke vakken); het deel onder/naast PE wordt zichtbaar. Paneelrecept van herstel10.
import os, sys, numpy as np
from PIL import Image
from collections import Counter
H=os.path.dirname(os.path.abspath(__file__)); R10=os.path.join(H,'..','r10')
MOD=os.path.join(H,'..','..','model','model_gekozen.png')
S=3.515625; TOP=13
im=Image.open(os.path.join(R10,'sprite.png')); PALF=im.getpalette()[:48]; PAL=np.array(PALF).reshape(16,3)
A=np.array(im).astype(int); B=A.copy()
P=np.load(os.path.join(R10,'w_r10','P_herstel.npy')).astype(object)
K=np.array(Image.open(os.path.join(R10,'w_r10','kaal.png'))).astype(int)
KMAP={15:15,14:5,13:5,12:4,11:4,5:3,4:3,3:3,2:2,1:1,6:6,7:7,8:8,9:9,10:10,0:1}
LOG=[]
def zet(x,y,c,deel,reden):
    if B[y,x]!=c: LOG.append((x,y,int(B[y,x]),int(c),deel,reden)); B[y,x]=c
def leeg(x,y): return not(0<=x<64 and 0<=y<64) or B[y,x]==0
N4=((-1,0),(1,0),(0,-1),(0,1))
BOLT={15,5,4,3}

# ---------------- 2. rechterbol: volle cirkel (r10: c=(52.75,38.23), R=6.48; pixelmidden <= R)
RC=(52.75,38.23); RR=6.48
SY,SX=np.mgrid[0:64,0:64]
CIRK=np.hypot(SX+.5-RC[0],SY+.5-RC[1])<=RR
for y,x in zip(*np.where(CIRK)):
    if P[y,x]!='#' or B[y,x]==0:
        c=KMAP[int(K[y,x])]
        if c not in BOLT:   # kale reductie geeft hier geen boltint: tint van de dichtstbijzijnde bestaande bolpixel
            best=None
            for yy,xx in zip(*np.where(CIRK)):
                if P[yy,xx]=='#' and B[yy,xx] in BOLT:
                    d=np.hypot(xx-x,yy-y)
                    if best is None or d<best[0]: best=(d,B[yy,xx])
            c=int(best[1])
        P[y,x]='#'; zet(x,y,c,'bol_rechts','volle cirkel voor PC/buis: tint uit de kale reductie')
# omlijning van de cirkel: binnenpixel met een 4-buur buiten de cirkel -> zwart onder/rechts, navy elders
for y,x in zip(*np.where(CIRK)):
    uit=[(dy,dx) for dy,dx in N4 if not CIRK[y+dy,x+dx]]
    if not uit: continue
    c=1 if any(d in ((1,0),(0,1)) for d in uit) else 2
    zet(x,y,c,'bol_rechts','cirkelrand (zwart schaduwkant, navy lichtkant)')
# oude lijnpixels die nu binnen de cirkel liggen (geen buur buiten): tint van de buur naar binnen
for y,x in zip(*np.where(CIRK)):
    if any(not CIRK[y+dy,x+dx] for dy,dx in N4): continue
    if B[y,x] in (1,2) and (x,y) not in []:
        d=np.hypot(x+.5-RC[0],y+.5-RC[1]); ux,uy=(x+.5-RC[0])/d,(y+.5-RC[1])/d
        for st in (1.2,2.2,3.2):
            ix,iy=int(np.floor(x+.5-ux*st)),int(np.floor(y+.5-uy*st))
            if B[iy,ix] in BOLT: zet(x,y,int(B[iy,ix]),'bol_rechts','oude lijn binnen de cirkel -> boltint van binnen'); break
# pixels buiten de cirkel die voor r10 bolpixel waren en nu een losse romppixel tegen de cirkel zijn: laten (buis/kraag)

# ---------------- 3. mast PB: eindkap linksboven (kale reductie heeft hier rij 13, x 34)
assert K[13,34]==2 and B[14,34]==2
P[13,34]="PB"; zet(34,13,2,'PB','eindkap: punt linksboven zoals de kale reductie (rij 13)')

# ---------------- 4. mast PF: volle lengte 47 (zelfde maat en vakken als PB)
sys.path.insert(0,os.path.join(R10,'pijp'))
T=np.array((123.0,100.0)); RV=np.array((0.0,47.0)); LV=np.array((145.46913591942328,108.98765436776931))-T
Mx=np.array([RV,LV]).T; INV=np.linalg.inv(Mx)
MX=3+(SX+.5)*S; MY=3+(SY-TOP+.5)*S
def uvf(mx,my):
    d=np.stack([mx-T[0],my-T[1]]); r=np.tensordot(INV,d,1); return r[0],r[1]
U,V=uvf(MX,MY); ID=(U>=0)&(U<=1)&(V>=0)&(V<=1)
LIJN=[1/3,2/3]; TINT=[14,13,11]
# nieuw PF-vlak: transparant binnen het parallellogram
for y,x in zip(*np.where(ID&(B==0))): P[y,x]='PF'
# losse punten aan scherpe hoeken (<=1 buur van PF) weg, zoals herstel10
for _ in range(3):
    for y,x in zip(*np.where(P=='PF')):
        n=sum(1 for dy,dx in N4 if 0<=y+dy<64 and 0<=x+dx<64 and P[y+dy,x+dx]=='PF')
        if n<=1: P[y,x]=''
du=np.abs(uvf(MX,MY+S)[0]-U)
NEW={}
def binnen(xx,yy): return 0<=xx<64 and 0<=yy<64 and ID[yy,xx] and P[yy,xx]!=''
for y,x in zip(*np.where(P=='PF')):
    bo,on,li,re=binnen(x,y-1),binnen(x,y+1),binnen(x-1,y),binnen(x+1,y)
    if not(bo and on and li and re): NEW[(x,y)]=1 if (not on or (not re and bo)) else 2; continue
    uu=U[y,x]; i=int(np.clip(np.searchsorted(LIJN,uu),0,2)); vt=TINT[i]
    if any(abs(uu-p)<=du[y,x]/2+1e-9 for p in LIJN): NEW[(x,y)]=-(14 if vt==11 else 12); continue
    NEW[(x,y)]=vt
for (x,y),c in list(NEW.items()):
    if c not in (14,13,11): continue
    for dy,dx in ((-1,0),(0,-1)):
        a_,b_=(x+dx,y+dy),(x-dx,y-dy)
        if P[a_[1],a_[0]]=='PF' and NEW.get(a_)==2 and P[b_[1],b_[0]]=='PF' and (NEW.get(b_,0) in (14,13,11) or NEW.get(b_,0)<0):
            NEW[(x,y)]=12; break
for (x,y),c in NEW.items(): zet(x,y,abs(c),'PF','mast PF volle lengte 47: recept (rand/vak/lijn) zoals herstel10')
for y,x in zip(*np.where((P=='')&(B>0))):
    if ID[y,x]: zet(x,y,0,'PF','losse hoekpunt -> transparant')

# ---------------- 1. ogen uit het model
a=np.array(Image.open(MOD).convert('RGB')).astype(int)
lab=((a[:,:,None,:]-PAL[None,None])**2).sum(3).argmin(2); lab[a.min(2)>=245]=0
from collections import deque
class ndimage:
    @staticmethod
    def binary_fill_holes(m):
        h,w=m.shape; out=np.zeros((h,w),bool); q=deque()
        for y in range(h):
            for x in range(w):
                if (y in (0,h-1) or x in (0,w-1)) and not m[y,x]: out[y,x]=1; q.append((y,x))
        while q:
            y,x=q.popleft()
            for dy,dx in N4:
                yy,xx=y+dy,x+dx
                if 0<=yy<h and 0<=xx<w and not m[yy,xx] and not out[yy,xx]: out[yy,xx]=1; q.append((yy,xx))
        return ~out
    @staticmethod
    def label(m):
        h,w=m.shape; lb=np.zeros((h,w),int); n=0
        for y in range(h):
            for x in range(w):
                if m[y,x] and not lb[y,x]:
                    n+=1; lb[y,x]=n; q=deque([(y,x)])
                    while q:
                        yy,xx=q.popleft()
                        for dy,dx in N4:
                            a2,b2=yy+dy,xx+dx
                            if 0<=a2<h and 0<=b2<w and m[a2,b2] and not lb[a2,b2]: lb[a2,b2]=n; q.append((a2,b2))
        return lb,n
    @staticmethod
    def sum(m,lb,idx): return [int((lb==i).sum()) for i in idx]
import oogmasker
KX=float(os.environ.get('KX','0.75'))
# model: bolmiddelpunt/straal (r13b), sprite: bolmiddelpunt (r10), schaal = bolfactor/s; venster rond het oog
OGEN={'voor':dict(mb=(62.16,127.95),sb=(16.83,48.54),f=1.3/S,kx=1.0,box=(40,80,112,150),FR=1.75),
      'links':dict(mb=(79+(75.01-79)*1.0,64.28),sb=(19.57,30.43),f=1.8/S,kx=KX,box=(60,80,55,76),FR=2.1),
      'rechts':dict(mb=(188.46,91.70),sb=(52.75,38.23),f=1.8/S,kx=KX,box=(174,192,85,104),FR=2.1)}
# links: r9 schaalde de linkerbol vanuit de kraagkant x=79; het spritemiddelpunt (19,57) hoort bij modelx 79+(75,01-79)*1,8.
OGEN['links']['mb']=(75.01,64.28); OGEN['links']['anker']=79.0
INFO={}; EYE=set()
for nm,o in OGEN.items():
    x0,x1,y0,y1=o['box']; sub=lab[y0:y1,x0:x1]
    eye,iris,pup,ring,_c,_r=oogmasker.masker(sub,o['FR'],None); iris_s=iris|pup
    ys,xs=np.where(iris_s); ec=np.array((xs.mean()+.5+x0,ys.mean()+.5+y0))   # irismiddelpunt (model)
    # spritepositie van het irismiddelpunt: bolmiddelpunt + offset x f (links: bol was vanuit de kraag geschaald, offset
    #   t.o.v. het modelbolmiddelpunt x 1,8 komt op hetzelfde neer)
    sc=np.array(o['sb'])+(ec-np.array(o['mb']))*o['f']*S/S
    f=o['f']; kx=o['kx']
    COV={k:np.zeros((64,64)) for k in ('ring','iris','pup')}; TON={k:np.zeros((64,64)) for k in (6,7,8,9,10)}
    nss=8
    for y in range(int(sc[1])-8,int(sc[1])+9):
        for x in range(int(sc[0])-8,int(sc[0])+9):
            for j in range(nss):
                for i in range(nss):
                    px,py=x+(i+.5)/nss,y+(j+.5)/nss
                    mx=ec[0]+(px-sc[0])/(f*kx); my=ec[1]+(py-sc[1])/f
                    ix,iy=int(np.floor(mx))-x0,int(np.floor(my))-y0
                    if not(0<=ix<x1-x0 and 0<=iy<y1-y0): continue
                    for k,m in (('ring',ring),('iris',iris),('pup',pup)):
                        if m[iy,ix]: COV[k][y,x]+=1/nss**2
                    L=sub[iy,ix]
                    if ring[iy,ix]:
                        # ringtint: 6/7/8 direct; lichte bol-/lavendelpixels binnen de ring = belicht ringdeel (8); donker (1,2,3) = 6
                        t=L if L in (6,7,8) else (8 if L in (4,12,14) else None)
                        if t: TON[t][y,x]+=1
                    elif iris[iy,ix]:
                        t=10 if L==10 else 9; TON[t][y,x]+=1
    tot=COV['ring']+COV['iris']+COV['pup']
    # rand van de bol (omlijning) blijft omlijning: het oog komt er niet overheen (in het model raakt de ring de bolrand)
    def bolrand(x,y): return B[y,x] in (1,2) and (P[y,x]!='#' or any(leeg(x+dx,y+dy) or P[y+dy,x+dx]!='#' for dy,dx in N4) or (nm=='rechts' and any(not CIRK[y+dy,x+dx] for dy,dx in N4)))
    zone=[(y,x) for y,x in zip(*np.where(tot>=0.5)) if P[y,x]=='#' and not bolrand(x,y)]
    # pupil: aantal pixels = modelpupiloppervlak x schaal^2 x kx (afgerond, min 1); de pixels met de meeste pupildekking
    npup=max(1,int(round((pup&np.isin(sub,(1,2,3))).sum()*f*f*kx)))   # alleen echt donkere pupilpixels tellen
    pupset=set(sorted(zone,key=lambda q:-COV['pup'][q])[:npup])
    pix={}
    for y,x in zone:
        if (y,x) in pupset: c=2
        elif COV['iris'][y,x]+COV['pup'][y,x]>=COV['ring'][y,x]: c=10 if TON[10][y,x]>TON[9][y,x] else 9
        else: c=max((6,7,8),key=lambda q:TON[q][y,x]) if any(TON[q][y,x] for q in (6,7,8)) else 7
        pix[(x,y)]=c
    xs_=[p[0] for p in pix]; ys_=[p[1] for p in pix]
    INFO[nm]=dict(model_iris_c=tuple(np.round(ec,1)),sprite_iris_c=tuple(np.round(sc,2)),schaal=round(f,3),kx=kx,
                  maat='%dx%d'%(max(xs_)-min(xs_)+1,max(ys_)-min(ys_)+1),pixels=len(pix),
                  pupil=sum(1 for c in pix.values() if c==2))
    # oude oogpixels buiten de nieuwe vorm -> boltint van de buur (zoals herstel10)
    oud=[(x,y) for y in range(64) for x in range(64) if B[y,x] in (6,7,8,9,10) and P[y,x]=='#' and np.hypot(x+.5-sc[0],y+.5-sc[1])<=6 and (x,y) not in pix]
    for x,y in oud:
        c=None
        for rr in (1,2,3):
            for ey,ex in ((0,-1),(-1,0),(0,1),(1,0),(-1,-1),(1,1),(-1,1),(1,-1)):
                xx,yy=x+ex*rr,y+ey*rr
                if 0<=xx<64 and 0<=yy<64 and (xx,yy) not in pix and B[yy,xx] in BOLT: c=B[yy,xx]; break
            if c: break
        zet(x,y,int(c or 5),'oog_'+nm,'oude oogpixel buiten de nieuwe oogvorm -> boltint van de buur')
    for (x,y),c in pix.items():
        if P[y,x]!='#': INFO[nm].setdefault('buiten_bol',[]).append((x,y))
        zet(x,y,c,'oog_'+nm,'oog uit het model (dekking ring/iris/pupil, modeltint)'); EYE.add((x,y))
    INFO[nm]['pix']=pix

# ---------------- 1b. ogen opschonen (alleen per pixel, vanuit de modelreductie hierboven; reden per oog)
#   voor: ring links 1 px (dun), rechts 2 px zoals het model, lichte band rechtsboven (8), schaduw rechtsonder (6); pupil 3 px +\n#     1 donkere tealhoek (afgerond)
#   links: iris tegen de bolrand links (zoals het model), pupil 1x2, ring rechts 2 px, boven 7 + lichte band 8
#   rechts: idem, pupil 1x2 in een iris van 3 breed (rechtsonder donker teal), ring rechts 2 px
SCHOON={'voor':{45:{13:7,14:7,15:7,16:7},
               46:{11:7,12:8,13:8,14:8,15:8,16:8,17:7},
               47:{11:7,12:9,13:9,14:10,15:10,16:8,17:8,18:7},
               48:{10:5,11:7,12:9,13:10,14:10,15:10,16:8,17:8,18:7},
               49:{10:5,11:7,12:10,13:2,14:2,15:10,16:9,17:7,18:7},
               50:{10:5,11:7,12:10,13:2,14:9,15:10,16:9,17:7,18:7},
               51:{11:7,12:10,13:10,14:10,15:10,16:9,17:6,18:7},
               52:{11:7,12:7,13:10,14:10,15:7,16:6,17:7},
               53:{12:7,13:7,14:7,15:7,16:7}},
        'links':{28:{16:7,17:7,18:7},
                 29:{15:7,16:10,17:10,18:8,19:7},
                 30:{15:9,16:10,17:10,18:7,19:7},
                 31:{15:10,16:2,17:10,18:7,19:7},
                 32:{15:10,16:2,17:9,18:6,19:7},
                 33:{16:7,17:7,18:7}},
        'rechts':{36:{49:7,50:7,51:7},
                  37:{48:7,49:8,50:8,51:8,52:7},
                  38:{48:7,49:10,50:10,51:10,52:8,53:7},
                  39:{48:7,49:10,50:2,51:10,52:7,53:7},
                  40:{48:7,49:10,50:2,51:9,52:7,53:7},
                  41:{48:7,49:9,50:10,51:9,52:6,53:7},
                  42:{49:7,50:7,51:7,52:7}}}
for nm,rij in SCHOON.items():
    nieuw={(x,y) for y,d in rij.items() for x in d}
    # oogpixels van de reductie buiten de opgeschoonde vorm -> boltint van de buur
    for (x,y) in list(INFO[nm]['pix']):
        if (x,y) not in nieuw and B[y,x] in (2,6,7,8,9,10):
            c=None
            for rr in (1,2):
                for ey,ex in ((0,1),(-1,0),(1,0),(0,-1)):
                    xx,yy=x+ex*rr,y+ey*rr
                    if (xx,yy) not in nieuw and B[yy,xx] in BOLT: c=B[yy,xx]; break
                if c: break
            zet(x,y,int(c or 5),'oog_'+nm,'opschonen: reductiepixel buiten de oogvorm -> boltint')
    for y,d in rij.items():
        for x,c in d.items():
            assert P[y,x]=='#', (nm,x,y)
            zet(x,y,c,'oog_'+nm,'opschonen (ringdikte/pupil naar het model)')
    xs=[p[0] for p in nieuw]; ys=[p[1] for p in nieuw]
    INFO[nm]['maat_schoon']='%dx%d'%(max(xs)-min(xs)+1,max(ys)-min(ys)+1); INFO[nm]['pupil_schoon']=sum(1 for y,d in rij.items() for c in d.values() if c==2)
np.save(os.path.join(H,'P_r11.npy'),P.astype(str))
def opslaan(arr,path):
    im2=Image.fromarray(arr.astype(np.uint8),'P'); im2.putpalette(PALF); im2.save(path,transparency=0)
if __name__=='__main__':
    for k,v in INFO.items(): print(k,{q:w for q,w in v.items() if q!='pix'})
    assert len(np.unique(B))<=16
    opslaan(B,os.path.join(H,'sprite.png'))
    r=PAL[B].astype(np.uint8); r[B==0]=(235,240,235)
    Image.fromarray(r).resize((512,512),Image.NEAREST).save(os.path.join(H,'sprite_8x.png'))
    d=(PAL[A]*0.45+255*0.55).astype(np.uint8); d[A==0]=(250,250,250); d[A!=B]=(220,30,30)
    Image.fromarray(d).resize((512,512),Image.NEAREST).save(os.path.join(H,'diff_r10.png'))
    last={}
    for l in LOG: last[(l[0],l[1])]=l
    fin=[l for (x,y),l in last.items() if B[y,x]!=A[y,x]]
    with open(os.path.join(H,'log_herstel11.txt'),'w') as f:
        f.write('x y oud->nieuw onderdeel reden (t.o.v. r10/sprite.png)\n')
        for l in LOG: f.write('%d %d %d->%d %s %s\n'%l)
        f.write('\nTELLING (anders dan r10, per onderdeel)\n')
        for k,n in sorted(Counter(l[4] for l in fin).items()): f.write('%s %d\n'%(k,n))
        f.write('totaal %d\n'%len(fin))
        f.write('kleuren %d (incl. transparant)\n'%len(np.unique(B)))
        for k,v in INFO.items(): f.write('%s %s\n'%(k,{q:w for q,w in v.items() if q!='pix'}))
    print('anders dan r10:',len(fin),sorted(Counter(l[4] for l in fin).items()))
