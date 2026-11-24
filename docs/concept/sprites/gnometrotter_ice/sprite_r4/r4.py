# r4.py: Gnometrotter Ice r4 uit r3 (23 nov). Logt elke gewijzigde pixel per zone.
# Zones (opdracht Jordi): gesp weg | rechterschouder rond | lijf ijsvormen | linkerhand als Rock af | rest = 0.
# Bronnen: r3 (basis), Ice-model r3 (ellipsen schouder/bovenarm, facetlijnen, tinten), Rock af (alleen linkerhand).
import numpy as np; from PIL import Image
import os; H=os.path.dirname(os.path.abspath(__file__))
R3=os.path.join(H,'../sprite_r3/gnometrotter_ice.png'); MOD=os.path.join(H,'../r3/gemini_r3_lijf.png')
ROCK=os.path.join(H,'../../gnometrotter_rock/af/gnometrotter_rock.png')
im=Image.open(R3); o=np.asarray(im).copy(); n=o.copy()
m=np.asarray(Image.open(MOD).convert('RGB')).astype(float); lum=m.mean(2); P=8.1
rock=np.asarray(Image.open(ROCK))
PINK={6,7,8,15}; PINKI={7,8,15}; BLUE={9,10,11}
log=[]; zone={}
def zet(x,y,v,z):
    if n[y,x]!=v or (x,y) in zone:
        n[y,x]=v; zone[(x,y)]=z
def cel(X,Y):
    x0=512+(X-32)*P; y0=523-(60-Y)*P
    return m[int(round(y0)):int(round(y0+P)),int(round(x0)):int(round(x0+P))].reshape(-1,3)

# ---------- 1. GESP WEG: riem loopt door (tinten van de riem rechts ernaast, x30: E/D/D) ----------
for y,v in ((39,14),(40,13),(41,13)):
    for x in range(24,30): zet(x,y,v,'gesp')

# ---------- 2. RECHTERSCHOUDER: ovaal + bovenarm als ellipsen gefit op de zwarte modelomlijning ----------
ys,xs=np.nonzero(lum<60); MX=(xs-512)/P+32; MY=(ys-523)/P+60
def fit(sel):
    x=MX[sel];y=MY[sel];A=np.c_[x*x,x*y,y*y,x,y]; c=np.linalg.lstsq(A,np.ones_like(x),rcond=None)[0]
    a,b,cc,d,e=c; ce=np.linalg.solve([[2*a,b],[b,2*cc]],[-d,-e]); return c,ce
c_ov,ce_ov=fit((MX>39.5)&(MX<51)&(MY>20.5)&(MY<30)&~((MX>50.2)&(MY>26.3)))
c_ar,ce_ar=fit((MX>49.8)&(MX<56.5)&(MY>26.0)&(MY<34.5)&~((MX<51)&(MY<28.5))&~((MY>33.3)&(MX>52.5)))
def binnen(c,ce,X,Y):
    s=np.sign(c@np.array([X*X,X*Y,Y*Y,X,Y])-1); return s==np.sign(c@np.array([ce[0]**2,ce[0]*ce[1],ce[1]**2,ce[0],ce[1]])-1)
def dekking(c,ce,X,Y,k=6):
    t=(np.arange(k)+.5)/k; return np.mean([binnen(c,ce,X+a,Y+b) for a in t for b in t])
OV=np.zeros((64,64),bool); AR=np.zeros((64,64),bool)
for Y in range(15,40):
    for X in range(36,60):
        OV[Y,X]=dekking(c_ov,ce_ov,X,Y)>=0.5
        AR[Y,X]=dekking(c_ar,ce_ar,X,Y)>=0.3 and not OV[Y,X]

def rand(M,X,Y): return any(not M[Y+dy,X+dx] for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)))
def roze_tint(X,Y,lo,hi):
    v=mlum(X,Y); return 15 if v>=hi else (8 if v>=lo else 7)
def mlum(X,Y):
    l=cel(X,Y).mean(1); return l[l>90].mean()   # modelhelderheid zonder de zwarte lijn
# ovaal: rand = 6 (zwart waar hij aan de buitenkant grenst), binnen = modelhelderheid, 3x3 gemiddeld binnen het ovaal
def glad(M,X,Y):
    v=[mlum(X+a,Y+b) for a in (-1,0,1) for b in (-1,0,1) if M[Y+b,X+a]]; return np.nanmean(v)
binn=[(X,Y) for Y in range(64) for X in range(64) if OV[Y,X] and not rand(OV,X,Y)]
G={p:glad(OV,*p) for p in binn}
lo,hi=np.percentile(list(G.values()),[30,82])
for Y in range(64):
    for X in range(64):
        if not OV[Y,X]: continue
        if rand(OV,X,Y):
            buiten=any(o[Y+dy,X+dx]==0 for dx,dy in ((1,0),(0,-1),(1,-1),(0,1)))
            zet(X,Y,1 if (buiten or o[Y,X]==1) else 6,'schouder')
        else: v=G[(X,Y)]; zet(X,Y,15 if v>=hi else (8 if v>=lo else 7),'schouder')
# bovenarm: r3 houdt zijn tinten; alleen de afgekapte bovenhoek wordt rond volgens de modelellips (dekking >= 0,3).
# r3-roze buiten de ellips: aan de buitenkant -> transparant, tussen ovaal en bovenarm -> zwarte naad (zoals het model).
# ellips-pixels die nu rand worden (buurpixel weg) -> 6, zoals de r3-rand van de bovenarm.
for Y in range(27,32):
    for X in range(50,57):
        if OV[Y,X] or o[Y,X] not in PINK or AR[Y,X] or not (Y==27 or X>=54): continue
        buiten=any(o[Y+dy,X+dx]==0 for dx,dy in ((1,0),(0,-1),(1,-1)))
        zet(X,Y,0 if buiten else 1,'schouder')
for Y in range(27,32):
    for X in range(50,57):
        if AR[Y,X] and n[Y,X] in PINKI and any(n[Y+dy,X+dx]==0 for dx,dy in ((1,0),(0,-1))): zet(X,Y,6,'schouder')

# buitenrand van de bovenarm boven/rechts zwart, zoals Rock af en het model (ronde zwarte boog i.p.v. vlakke roze bovenkant)
for Y in range(27,32):
    for X in range(51,57):
        if n[Y,X]==6 and (n[Y,X+1]==0 or n[Y-1,X]==0 or n[Y-1,X+1]==0) and not (Y==27 and X==51): zet(X,Y,1,'schouder')

# aansluiting ovaal|bovenarm zoals Rock af (rij 27: 6 6 | 8 | 1 1): bovenste pixel van de bovenarm roze, naad 6
zet(50,27,6,'schouder'); zet(51,27,8,'schouder')

# ---------- 5. LINKERHAND als Rock af (Jordi: "nee ijs moet de linkerhand ook als rock") ----------
# Doos x0-17, y28-36 (vuist + arm tot de baard). Roze/zwart van Rock af overnemen (roze indexen gedeeld);
# waar Rock stok toont en Ice r3 roze/zwart had: stokindex van Rock (2-5, zelfde rol in het ijspalet);
# waar Ice r3 al stok had: Ice r3 houden; waar Rock leeg is en Ice r3 roze/zwart: leeg.
STOK={2,3,4,5}
def vuist(A,X,Y):   # roze, of zwart dat aan roze grenst (omlijning van vuist/arm)
    if A[Y,X] in PINK: return True
    return A[Y,X]==1 and any(A[Y+b,X+a] in PINK for a in (-1,0,1) for b in (-1,0,1) if 0<=X+a<64)
for Y in range(28,37):
    for X in range(0,18):
        r=int(rock[Y,X]); i=int(o[Y,X])
        if X>=14 and i in (2,12,13,14): continue          # baard van Ice blijft
        if vuist(rock,X,Y): v=r
        elif not vuist(o,X,Y): continue                     # stok/leeg zonder vuist: Ice r3 houdt
        elif r in STOK and X<=12: v=r                       # stok die bij Rock onder de vuist uitkomt
        elif r==0: v=0
        else: continue
        zet(X,Y,v,'linkerhand')

# ---------- 3. LIJF: een paar grote ijsvormen uit de facetlijnen van het model, alleen roze 6/7/8/15 en blauw 9/10/11 ----------
def lijnpix(pts):   # pixels waar een modellijn (polylijn in spritecoordinaten) doorheen loopt
    s=set()
    for (x0,y0),(x1,y1) in zip(pts,pts[1:]):
        k=int(max(abs(x1-x0),abs(y1-y0))*4)+1
        for t in np.linspace(0,1,k): s.add((int(np.floor(x0+(x1-x0)*t)),int(np.floor(y0+(y1-y0)*t))))
    return s
# romp: lichte rand (15) van het grote bovenvlak langs zijn linkerranden (modelribbe (34,30)-(37,33.5)),
# zoals de bestaande 15-ribbe linksboven; vlak eronder/rechts blijft 8/7 van r3.
RIB=lijnpix([(34.3,30.2),(37.2,33.4)])
for X,Y in sorted(RIB):
    if n[Y,X] in (7,8): zet(X,Y,15,'lijf')
# oude ovaaltop boven de nieuwe ovaalrand ligt achter het ovaal (model: donker roze lijf) -> geen 15 meer
for X,Y in ((42,20),(41,21),(42,21)):
    if n[Y,X]==15: zet(X,Y,7,'schouder')
# rechterdij: vlakken volgens de modelribben (verticaal x44,5 tot y47,5; horizontaal y47,5; diagonaal (45,47,5)-(49,5,44,5))
DIAG={(X,int(47.6-(X+0.5-45.2)*3.2/4.4)) for X in range(46,50)}   # 1 px per kolom
def schaduwrand(X,Y): return n[Y,X]==9 and (n[Y,X+1]==1 or n[Y+1,X]==1)
for Y in range(42,50):
    for X in range(41,50):
        if n[Y,X] not in (10,11): continue               # 9 (lijnen, schaduwsikkel) van r3 blijven
        if (X,Y) in DIAG and X>=46: v=9                    # naad tussen de twee rechtervlakken
        elif X<=44 and Y<=47: v=11                         # bovenvlak links (licht)
        else: v=10                                         # rechter- en ondervlakken
        zet(X,Y,v,'lijf')
# linkerdij (deel naast de baard): bovenvlak 11, ondervlak 10 onder de horizontale modelribbe y46,5
for Y in (47,48):
    for X in range(20,29):
        if n[Y,X]==11: zet(X,Y,10,'lijf')

# ---------- uitvoer + log ----------
out=Image.fromarray(n.astype('uint8'),'P'); out.putpalette(im.getpalette()); out.info['transparency']=0
out.save(os.path.join(H,'gnometrotter_ice.png'),transparency=0)
out.resize((512,512),Image.NEAREST).save(os.path.join(H,'gnometrotter_ice_8x.png'))
tel={}
with open(os.path.join(H,'r4_log.txt'),'w') as f:
    for Y in range(64):
        for X in range(64):
            if n[Y,X]!=o[Y,X]:
                z=zone.get((X,Y),'rest'); tel[z]=tel.get(z,0)+1
                f.write('%s (%d,%d) %X -> %X\n'%(z,X,Y,o[Y,X],n[Y,X]))
sil=int(((n>0)!=(o>0)).sum())
print('gewijzigd per zone:',tel,'| silhouet:',sil)
