# r9 vormherstel (Jordi over r8: "probeer de vormen goed te herstellen, rond rond, rechthoekig rechthoek,
#   de panelen in het midden groeien niet mee, het oog netjes erin zetten").
# Invoer: sprite_<VAR>.png (pijplijn r8 = maak9.py, model met mastpanelen x KM). Alleen pixelreparaties, elk gelogd:
#   A panelen: eigendom per pixel = pixelmidden binnen het modelparallellogram (GEO uit lijnen.py, model-uv), volgorde
#     achter->voor PC, PA, PB, PD, PF, PE; romp ervoor waar het model >=50% romp heeft. Kleur = bestaand recept (fase 2):
#     rand navy/zwart (DC), lichte rand, vaktint per vak, rasterlijn 1 px per kolom/rij op de modelpositie.
#   B bollen: buitenrand = gefitte cirkel (pixelmidden <= r); nieuwe binnenpixels krijgen de tint van de buur binnenin.
#   C ogen: ring + iris + pupil 2x2 als vaste vorm (voor 8/6/2, zij 6/4/2), tinten uit de modeldekking (ogen7).
#   D romp-omlijning: randpixel tegen transparant -> zwart onder/rechts, navy elders (r4-regel).
# Gebruik: VAR=s18p15m20 python3 herstel9.py
import os, sys, numpy as np
from PIL import Image
from collections import Counter
H=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,os.path.join(H,'pijp'))
VAR=os.environ['VAR']
import lijnen, kruis, ogen7
S=3.515625; TOP=13
im=Image.open(os.path.join(H,'sprite_%s.png'%VAR)); PALF=im.getpalette()[:48]
A=np.array(im).astype(int); B=A.copy()
OH=kruis.OH
OW=np.full((64,64),'',object); OW[TOP:TOP+OH]=np.load(os.path.join(H,'w_'+VAR,'ownk.npy'))
LOG=[]
def zet(x,y,c,deel,reden):
    if B[y,x]!=c: LOG.append((x,y,int(B[y,x]),int(c),deel,reden)); B[y,x]=c
SY,SX=np.mgrid[0:64,0:64]; MX=3+(SX+.5)*S; MY=3+(SY-TOP+.5)*S
# romp-dekking uit het model (romp = niet-achtergrond min paneelkleur), op spriteraster
PANM=np.load(os.path.join(H,'model_%s_pan.npy'%VAR))   # r9: paneelpixels van het model (model9.py), de rest is romp
MODCOV=np.zeros((64,64)); MODCOV[TOP:TOP+OH]=kruis.cov(~kruis.bg&~PANM)
ORDE=['PC','PA','PB','PD','PF','PE']
TINT={'PD':[14,13,13,11],'PE':[14,13,13,11],'PA':[13,13,11,11],'PC':[13,13,11,11],'PB':[14,13,13],'PF':[14,13,11]}
LIJN={'PA':[.25,.5,.75],'PC':[.25,.5,.75],'PD':[.25,.5,.75],'PE':[.25,.5,.75],'PB':[1/3,2/3],'PF':[1/3,2/3]}
UV={k:lijnen.uv(k,MX,MY) for k in ORDE}
def inpar(k,x,y):
    u,v=UV[k][0][y,x],UV[k][1][y,x]; return 0<=u<=1 and 0<=v<=1
# ---------------- A. panelen
oudpan=OW!=''
body=(A>0)&~oudpan
IDEAAL={k:(UV[k][0]>=0)&(UV[k][0]<=1)&(UV[k][1]>=0)&(UV[k][1]<=1) for k in ORDE}
uni=np.zeros((64,64),bool)
for m in IDEAAL.values(): uni|=m
# romp blijft romp: buiten de paneelvlakken, of binnen een paneelvlak waar het model >=50% romp heeft
romp=body&(~uni|(MODCOV>=0.5))
P=np.full((64,64),'',object)
for k in ORDE: P[IDEAAL[k]&~romp]=k
P[romp]='#'
# losse punten aan scherpe parallellogramhoeken (pixelmidden net binnen, <=1 buur van hetzelfde paneel) -> weg
for _ in range(3):
    for k in ORDE:
        for y,x in zip(*np.where(P==k)):
            n=sum(1 for dy,dx in ((-1,0),(1,0),(0,-1),(0,1)) if 0<=y+dy<64 and 0<=x+dx<64 and P[y+dy,x+dx]==k)
            if n<=1: P[y,x]=''
def own(x,y): return P[y,x] if 0<=x<64 and 0<=y<64 else ''
LICHTROMP={15,5,4,3}
# voormalige paneelpixels buiten het parallellogram: romp als het model daar >=50% romp heeft (kleur uit de kale reductie)
K=np.array(Image.open(os.path.join(H,'w_'+VAR,'kaal.png'))).astype(int)
KMAP={15:15,14:5,13:5,12:4,11:4,5:3,4:3,3:3,2:2,1:1,6:6,7:7,8:8,9:9,10:10,0:1}   # kaal-index -> r6-palet (kleur6-regels)
for y,x in zip(*np.where((P=='')&oudpan&(A>0)&(MODCOV>=0.5))): P[y,x]='#'
# gaten (>=3 buren bezet) dicht met het meest voorkomende buurlabel; losse romppixels (<=1 buur) weg
def buren(y,x): return [P[y+dy,x+dx] for dy,dx in ((-1,0),(1,0),(0,-1),(0,1)) if 0<=y+dy<64 and 0<=x+dx<64]
for _ in range(2):
    for y in range(64):
        for x in range(64):
            nb=[q for q in buren(y,x) if q]
            if P[y,x]=='' and len(nb)>=3: P[y,x]=max(set(nb),key=nb.count)
            elif P[y,x]=='#' and len(nb)<=1: P[y,x]=''
NEW=np.zeros((64,64),int)
for k in ORDE:
    T,R,L=map(np.array,lijnen.GEO[k]); d=L-T; vlak=abs(d[0])>=abs(d[1])
    u=UV[k][0]; du=np.abs(lijnen.uv(k,MX,MY+S)[0]-u) if vlak else np.abs(lijnen.uv(k,MX+S,MY)[0]-u)
    ID=IDEAAL[k]
    def binnen(xx,yy): return 0<=xx<64 and 0<=yy<64 and ID[yy,xx] and P[yy,xx]!=''
    for y,x in zip(*np.where(P==k)):
        # rand = geometrisch: een buur ligt buiten het eigen parallellogram (of is leeg); wat er voor ligt (romp,
        # voorpaneel) telt als binnen, zodat de rand recht doorloopt. Zwart onder (en rechts als boven nog binnen), anders navy.
        bo,on,li,re=binnen(x,y-1),binnen(x,y+1),binnen(x-1,y),binnen(x+1,y)
        if not(bo and on and li and re):
            NEW[y,x]=1 if (not on or (not re and bo)) else 2; continue
        uu=u[y,x]; i=int(np.clip(np.searchsorted(LIJN[k],uu),0,len(TINT[k])-1)); vt=TINT[k][i]
        if any(abs(uu-p)<=du[y,x]/2+1e-9 for p in LIJN[k]): NEW[y,x]=-(14 if vt==11 else 12); continue
        NEW[y,x]=vt
# lichte rand: vakpixel direct onder/rechts van een navy rand van hetzelfde paneel, met nog een vakpixel erachter
VAK={14,13,11}
for k in ORDE:
    for y,x in zip(*np.where(P==k)):
        if NEW[y,x] not in VAK: continue
        for dy,dx in ((-1,0),(0,-1)):
            yy,xx,y2,x2=y+dy,x+dx,y-dy,x-dx
            if own(xx,yy)==k and NEW[yy,xx]==2 and own(x2,y2)==k and (NEW[y2,x2] in VAK or NEW[y2,x2]<0):
                NEW[y,x]=12; break
NEW=np.abs(NEW)
for y in range(64):
    for x in range(64):
        k=P[y,x]
        if k in ORDE: zet(x,y,int(NEW[y,x]),k,'paneel uit modelparallellogram (rand/vak/lijn volgens recept)')
        elif k=='' and B[y,x]: zet(x,y,0,'paneelrand','buiten het modelparallellogram / losse pixel -> transparant')
        elif k=='#' and (A[y,x]==0 or oudpan[y,x]): zet(x,y,KMAP[int(K[y,x])],'romp','romp waar het model romp heeft (kleur kale reductie)')
np.save(os.path.join(H,'w_'+VAR,'P_herstel.npy'),P.astype(str))
def tussen(stap):
    if os.environ.get('STAP')==stap:
        im2=Image.fromarray(B.astype(np.uint8),'P'); im2.putpalette(PALF); im2.save(os.path.join(H,'w_'+VAR,'herstel_%s.png'%stap),transparency=0)
        print(Counter(l[4] for l in LOG)); sys.exit()
if False:
    im2=Image.fromarray(B.astype(np.uint8),'P'); im2.putpalette(PALF); im2.save(os.path.join(H,'w_'+VAR,'herstel_A.png'),transparency=0)
    print(Counter(l[4] for l in LOG)); sys.exit()
tussen('A')
# ---------------- B. bollen: vrije buitenrand = cirkel (pixelmidden <= R)
from common import KF,KS
def sp(mx,my): return ((mx-3)/S,(my-3)/S+TOP)
BOLGEO={'voor':(62.16,127.95,20.62*KF),'links':(79+(75.01-79)*KS,64.28,10.75*KS),'rechts':(188.46,91.70,11.98*KS),
        'achter':(182.0,36.1,14.8),'knoop':(128.0,72.0,20.5)}
RND={}; VRIJ={}
def isleeg(x,y): return not(0<=x<64 and 0<=y<64) or B[y,x]==0
def randpix(cx,cy,R,vrij):
    out=[]
    for y in range(64):
        for x in range(64):
            if B[y,x]==0 or P[y,x]!='#': continue
            d=np.hypot(x+.5-cx,y+.5-cy); a_=np.degrees(np.arctan2(y+.5-cy,x+.5-cx))%360
            if abs(d-R)>2 or not vrij(a_): continue
            if any(isleeg(x+dx,y+dy) for dy,dx in ((-1,0),(1,0),(0,-1),(0,1))): out.append((x,y,d))
    return out
for nm,(mx,my,mr) in BOLGEO.items():
    cx,cy=sp(mx,my); R0=mr/S
    # vrije hoeken: het punt net buiten de modelcirkel is transparant in de huidige sprite
    vrijset=[]
    for a_ in range(0,360,3):
        px,py=cx+(R0+0.9)*np.cos(np.radians(a_)),cy+(R0+0.9)*np.sin(np.radians(a_))
        qx,qy=int(np.floor(px)),int(np.floor(py))
        px2,py2=cx+(R0-1.2)*np.cos(np.radians(a_)),cy+(R0-1.2)*np.sin(np.radians(a_))
        if isleeg(qx,qy) and not isleeg(int(np.floor(px2)),int(np.floor(py2))) and P[int(np.floor(py2)),int(np.floor(px2))]=='#': vrijset.append(a_)
    vs=set(vrijset)
    # alleen aaneengesloten vrije stukken van >= 4 stappen (12 graden)
    vrij2=set(a_ for a_ in vs if sum(((a_+3*i)%360 in vs) for i in range(-2,3))>=4)
    vrij=lambda a_: (int(a_//3)*3)%360 in vrij2
    VRIJ[nm]=vrij2
    rp=randpix(cx,cy,R0,vrij)
    if len(rp)<5: RND[nm]=None; continue
    R=float(np.mean([d for _,_,d in rp]))+0.5
    for it in range(2):
        for y in range(64):
            for x in range(64):
                d=np.hypot(x+.5-cx,y+.5-cy); a_=np.degrees(np.arctan2(y+.5-cy,x+.5-cx))%360
                if abs(d-R)>2.2 or not vrij(a_): continue
                if d<=R and B[y,x]==0 and P[y,x]=='':
                    # binnen de cirkel en leeg -> bol (rand; tint volgt in D)
                    P[y,x]='#'; zet(x,y,1,'bol_'+nm,'cirkel: pixelmidden binnen r=%.2f -> bol'%R)
                elif d>R and B[y,x]>0 and P[y,x]=='#':
                    P[y,x]=''; zet(x,y,0,'bol_'+nm,'cirkel: pixelmidden buiten r=%.2f -> transparant'%R)
    # randpixels die nu binnen liggen (geen lege buur) maar nog lijnkleur hebben: tint van de buur naar binnen
    for y in range(64):
        for x in range(64):
            d=np.hypot(x+.5-cx,y+.5-cy); a_=np.degrees(np.arctan2(y+.5-cy,x+.5-cx))%360
            if abs(d-R)>2.2 or not vrij(a_) or P[y,x]!='#' or B[y,x] not in (1,2): continue
            if any(isleeg(x+dx,y+dy) for dy,dx in ((-1,0),(1,0),(0,-1),(0,1))): continue
            ix,iy=int(np.floor(x+.5-(x+.5-cx)/d*1.2)),int(np.floor(y+.5-(y+.5-cy)/d*1.2))
            c=B[iy,ix]
            if c in (1,2):
                ix,iy=int(np.floor(x+.5-(x+.5-cx)/d*2.2)),int(np.floor(y+.5-(y+.5-cy)/d*2.2)); c=B[iy,ix]
            if c not in (1,2,0): zet(x,y,int(c),'bol_'+nm,'oude rand ligt nu binnen de cirkel: tint van de buur naar binnen')
    RND[nm]=dict(c=(round(cx,2),round(cy,2)),R=round(R,2),vrij=len(vrij2)*3)
tussen('B')
# ---------------- C. ogen: vaste vorm (voor ring 8/iris 6, zij ring 6/iris 4), pupil 2x2 in het midden, geen wit;
#   tinten uit de modeldekking op dezelfde (eventueel verschoven) plek
RING8=[4,6,8,8,8,8,6,4]; IRIS6=[0,4,6,6,6,6,4,0]
RING6=[4,6,6,6,6,4];     IRIS4=[0,2,4,4,2,0]
VORM={'voor':(RING8,IRIS6),'links':(RING6,IRIS4),'rechts':(RING6,IRIS4)}
labm=ogen7.lab; Wx=kruis.Wx; Wy=kruis.Wy
def mcov(m):
    o=np.zeros((64,64)); o[TOP:TOP+OH]=Wy@m.astype(float)@Wx.T/(S*S); return o
CV={c:mcov(labm==c) for c in (6,7,8,9,10)}
OOGIDX=(6,7,8,9,10)
OOG={}; EYEPIX=set()
for nm,(ring,iris) in VORM.items():
    inf=ogen7.INFO[nm]; mcx,mcy=inf['sprite_c']; n=len(ring)
    bolnm={'voor':'voor','links':'links','rechts':'rechts'}[nm]
    bcx,bcy=sp(*BOLGEO[bolnm][:2])
    def masker(ox,oy):
        m={}
        for r,w in enumerate(ring):
            x0=ox+(n-w)//2
            for x in range(x0,x0+w): m[(x,oy+r)]='ring'
        for r,w in enumerate(iris):
            x0=ox+(n-w)//2
            for x in range(x0,x0+w): m[(x,oy+r)]='iris'
        h=n//2; 
        for x in (ox+h-1,ox+h):
            for y in (oy+h-1,oy+h): m[(x,y)]='pup'
        return m
    def geldig(m):
        for (x,y),t in m.items():
            if not(0<=x<64 and 0<=y<64) or P[y,x]!='#' or B[y,x]==0: return False
            # geen oogpixel op de bolrand: alle 4 buren bezet en romp (geen paneel)
            for dy,dx in ((-1,0),(1,0),(0,-1),(0,1)):
                if isleeg(x+dx,y+dy) or P[y+dy,x+dx]!='#': return False
            # linkerbol: niet over de kraag (kraag/buis rechts van de bol: buiten de bolcirkel)
            if np.hypot(x+.5-bcx,y+.5-bcy)>BOLGEO[bolnm][2]/S-0.6: return False
        return True
    ox0=int(round(mcx-n/2)); oy0=int(round(mcy-13-n/2))+13
    kand=sorted(((abs(ox0+dx+n/2-mcx)+abs(oy0+dy+n/2-mcy),dx,dy) for dx in range(-3,4) for dy in range(-3,4)))
    for dist,dx,dy in kand:
        m=masker(ox0+dx,oy0+dy)
        if geldig(m): break
    else:
        raise SystemExit('geen geldige plek voor oog '+nm)
    sx_,sy_=ox0+dx+n/2-mcx, oy0+dy+n/2-mcy      # verschuiving t.o.v. het model (spritepx)
    OOG[nm]=dict(vorm='ring %d, iris %d, pupil 2x2'%(n,n-2),plek=(ox0+dx,oy0+dy),verschuiving=(round(sx_,2),round(sy_,2)))
    # oude oogpixels buiten de nieuwe vorm -> boltint van de buur (naar de bolrand toe gezien, niet-oog)
    oud=[(x,y) for y in range(64) for x in range(64) if B[y,x] in OOGIDX+(2,) and P[y,x]=='#' and np.hypot(x+.5-(ox0+dx+n/2),y+.5-(oy0+dy+n/2))<=n/2+1.5 and (x,y) not in m and not any(isleeg(x+ex,y+ey) for ey,ex in ((-1,0),(1,0),(0,-1),(0,1)))]
    for x,y in oud:
        c=None
        for rr in (1,2,3):
            for ey,ex in ((0,-1),(-1,0),(0,1),(1,0),(-1,-1),(1,1),(-1,1),(1,-1)):
                xx,yy=x+ex*rr,y+ey*rr
                if 0<=xx<64 and 0<=yy<64 and (xx,yy) not in m and B[yy,xx] in (15,5,4,3): c=B[yy,xx]; break
            if c: break
        zet(x,y,int(c or 5),'oog_'+nm,'oude oogpixel buiten de nieuwe oogvorm -> boltint van de buur')
    for (x,y),t in m.items():
        mx_,my_=int(round(x-sx_)),int(round(y-sy_))   # modelplek (zonder verschuiving)
        if t=='pup': c=2
        elif t=='iris': c=9 if CV[9][my_,mx_]>CV[10][my_,mx_] else 10
        else:   # ring: licht linksboven (8), schaduw rechtsonder (6), rest 7 (modeldekking gaf ruis na de verschuiving)
            a_=np.degrees(np.arctan2(y+.5-(oy0+dy+n/2),x+.5-(ox0+dx+n/2)))%360
            c=8 if 180<=a_<=270 else (6 if a_<=90 else 7)
        EYEPIX.add((x,y))
        zet(x,y,c,'oog_'+nm,{'pup':'pupil 2x2 in het midden','iris':'iris (tint uit model)','ring':'ring (licht linksboven, schaduw rechtsonder)'}[t])
tussen('C')
# ---------------- D. omlijning romp/bollen: randpixel tegen transparant -> zwart onder/rechts, navy elders (r4-regel)
for y in range(64):
    for x in range(64):
        if P[y,x]!='#' or B[y,x]==0: continue
        if (x,y) in EYEPIX: continue
        lo=isleeg(x,y+1); lr=isleeg(x+1,y); lb=isleeg(x,y-1); ll=isleeg(x-1,y)
        if not(lo or lr or lb or ll): continue
        c=1 if (lo or lr) else 2
        if B[y,x] in (1,2) and not any(l.startswith('bol') for l in [q[4] for q in LOG if q[0]==x and q[1]==y]): continue   # bestaande lijn laten
        zet(x,y,c,'omlijning','randpixel tegen transparant: '+('zwart (schaduwkant)' if c==1 else 'navy (lichtkant)'))
tussen('D')
# ---------------- E. metingen en uitvoer
OUT=B
def rand_dev(nm,ARR):
    if RND.get(nm) is None: return None
    (cx,cy),R=RND[nm]['c'],RND[nm]['R']
    leeg=lambda x,y: not(0<=x<64 and 0<=y<64) or ARR[y,x]==0
    dev=[]
    for y in range(64):
        for x in range(64):
            if ARR[y,x]==0 or ARR[y,x] in (11,12,13,14): continue
            if not any(leeg(x+dx,y+dy) for dy,dx in ((-1,0),(1,0),(0,-1),(0,1))): continue
            d=np.hypot(x+.5-cx,y+.5-cy); a_=np.degrees(np.arctan2(y+.5-cy,x+.5-cx))%360
            if abs(d-R)<=2 and (int(a_//3)*3)%360 in VRIJ[nm]: dev.append(d-(R-0.5))
    return dict(n=len(dev),min=round(min(dev),2),max=round(max(dev),2),R=R,vrij_graden=RND[nm]['vrij'])
def paneelcontrole(k):
    ID=IDEAAL[k]; own=(P==k)
    afw_in=int((own&~ID).sum()); afw_uit=int((ID&~own&(P=='')).sum())
    # trapritme: per kolom de bovenste/onderste pixel van het parallellogram (mast: per rij links/rechts) -> lengtes van de treden
    from itertools import groupby
    T,R_,L=map(np.array,lijnen.GEO[k]); d=R_-T; mast=abs(d[1])>abs(d[0])
    ys,xs=np.where(ID)
    runs={}
    if not mast:
        for naam,f in (('boven',min),('onder',max)):
            seq=[f(ys[xs==x]) for x in sorted(set(xs))]; runs[naam]=[len(list(g)) for _,g in groupby(seq)]
    else:
        for naam,f in (('links',min),('rechts',max)):
            seq=[f(xs[ys==y]) for y in sorted(set(ys))]; runs[naam]=[len(list(g)) for _,g in groupby(seq)]
    # rasterlijnen: per lijn het aantal pixels, positie (u) gelijk verdeeld
    return dict(eigen_buiten_parallellogram=afw_in,leeg_binnen_parallellogram=afw_uit,trap=runs)
RONDH={nm:dict(r8=rand_dev(nm,A),r9=rand_dev(nm,OUT)) for nm in BOLGEO}
PCTRL={k:paneelcontrole(k) for k in ORDE}
assert len(np.unique(OUT))<=16
def save(arr,path):
    im2=Image.fromarray(arr.astype(np.uint8),'P'); im2.putpalette(PALF); im2.save(path,transparency=0)
save(OUT,os.path.join(H,'sprite.png'))
PP=np.array(PALF,np.uint8).reshape(16,3)
def rgb(arr,bg=(235,240,235)):
    r=PP[arr]; r[arr==0]=bg; return Image.fromarray(r)
rgb(OUT).resize((512,512),Image.NEAREST).save(os.path.join(H,'sprite_8x.png'))
d=np.array(rgb(A)).astype(int); d=(d*0.45+255*0.55).astype(np.uint8); d[A!=OUT]=(220,30,30)
Image.fromarray(d).resize((512,512),Image.NEAREST).save(os.path.join(H,'diff_herstel.png'))
with open(os.path.join(H,'w_'+VAR,'log_herstel9.txt'),'w') as f:
    f.write('x y oud->nieuw onderdeel reden (t.o.v. pijplijnuitvoer sprite_r9.png = r8-pijplijn op het r9-model)\n')
    for l in LOG: f.write('%d %d %d->%d %s %s\n'%l)
    last={}
    for l in LOG: last[(l[0],l[1])]=l
    fin=[l for (x,y),l in last.items() if OUT[y,x]!=A[y,x]]
    f.write('\nTELLING (pixels anders dan de pijplijnuitvoer, laatste reden telt)\n')
    for (dl,r),n in sorted(Counter((l[4],l[5]) for l in fin).items()): f.write('%-11s %-75s %d\n'%(dl,r,n))
    f.write('totaal %d\n'%len(fin))
    f.write('\nRONDHEID (randpixels in de vrije sector, afwijking d-(R-0,5) in px)\n')
    for nm,v in RONDH.items(): f.write('%s %s\n'%(nm,v))
    f.write('\nBOLLEN %s\nOGEN %s\n'%(RND,OOG))
    f.write('\nPANELEN %s\n'%PCTRL)
    f.write('kleuren %d (incl. transparant)\n'%len(np.unique(OUT)))
print('totaal',len(fin)); print(sorted(Counter(l[4] for l in fin).items()))
for nm,v in RONDH.items(): print(nm,v)
for k,v in PCTRL.items(): print(k,v)
print(OOG)
