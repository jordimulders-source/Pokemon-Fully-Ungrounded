# Vileplume r9 = r8_kroonr7 (r7-kroon + gezicht + linkerpoot uit r8) + coordinator r9:
#  1. VL/VR: de donkere tentakellijnen uit het model (r9/lijnen.py: R0/K-pixels van het natieve model, per spritepixel
#     geprojecteerd) -> hoekpieken = modellijnen; de sterkste ±9 per anemoon blijven (klonteren door lijnen te schrappen),
#     elk als lijn van 1 px (buitenste deel 2 px: fingertoppen aan de rand) van de lichte kern rond het mondje tot de rand,
#     in de modelrichting. Lijnen die bijna horizontaal naast het mondje lopen worden geschrapt (model: daar loopt de
#     lichte kern door, de lijnen beginnen schuin). Vulling: lichte tentakeltint R3, schaduwsikkel R2 (zoals r7).
#  2. mondjes alle vijf: kleiner stempel (varianten M1-M4, --mond=).
#  3. gelaat B standaard, A-E mee. 4. linkerpoot en krater als r8.
import sys, numpy as np
sys.path.insert(0,'gereedschap'); sys.path.insert(0,'r9')
from PIL import Image
from gemeen import opslaan; from anemonen import AN, MOND
from lijnen import lijnkaart
def opt(n,d):
    for x in sys.argv:
        if x.startswith('--'+n+'='): return x.split('=')[1]
    return d
RONDE=opt('ronde','r9'); MODUS=opt('modus','model'); WIJD='--wijd' in sys.argv; MV=opt('mond','M1'); NL=int(opt('n',9)); HUBX=float(opt('hubx',0.6)); HUBY=float(opt('huby',0.3))
im=Image.open('r8/vileplume_r8_kroonr7.png'); PAL=[tuple(p) for p in np.array(im.getpalette()[:48]).reshape(-1,3)]
o=np.asarray(im).astype(int).copy(); r7=o.copy()
KROONELL=[(25.0,21.5,10.2,6.2),(43.5,20.0,8.8,6.0),(14.0,14.0,9.0,5.6),(49.0,12.3,8.6,5.4),(33.5,6.3,7.4,2.7)]
OUDMOND=[(22,26,21,23),(40,45,19,21),(11,16,13,15),(46,51,11,13),(31,36,5,7)]
SIKKEL=0.75
def inell(i,X,Y,s=1.0):
    cx,cy,a,b=KROONELL[i]; return ((X+.5-cx)/(a*s))**2+((Y+.5-cy)/(b*s))**2<=1
def sik(i,X,Y):
    cx,cy,a,b=KROONELL[i]; return 0.55*(X+.5-cx)/a+0.83*(Y+.5-cy)/b>SIKKEL
def vul(i,X,Y): return 4 if sik(i,X,Y) else 5
# ---- 1. kroonbinnenkant VL/VR leeg: R1-lijnen en oude mondring -> vulling ----
BIN={}
for i in (1,0):
    m=np.zeros((64,64),bool)
    for Y in range(2,32):
        for X in range(1,63):
            if not inell(i,X,Y,0.97) or (i==1 and inell(0,X,Y)): continue
            if r7[Y,X] in (2,3,4,5): m[Y,X]=True
    # alleen pixels die niet aan de omlijning (K) raken
    for Y,X in zip(*np.where(m)):
        if any(r7[Y+dy,X+dx]==1 for dy,dx in ((0,1),(1,0),(0,-1),(-1,0))): m[Y,X]=False
    BIN[i]=m
    if MODUS=='r7': continue          # kroon van r7 ongewijzigd, alleen de mondjes nieuw
    if MODUS=='r7lijnen':
        # variant: de r7-stralen houden, maar als modellijnen in R0 (donker, zoals de lijnen in het model) i.p.v. R1;
        # buitenste deel (d > BUITEN van de kroonstraal) een pixel breder naar de schaduwkant -> fingertoppen aan de rand
        cx,cy,a,b=KROONELL[i]
        for Y,X in zip(*np.where(m)):
            if r7[Y,X]==3:
                o[Y,X]=2
                if np.hypot((X+.5-cx)/a,(Y+.5-cy)/b)>float(opt('rand',0.7)):
                    for X2,Y2 in ((X+1,Y),(X,Y+1)):
                        if m[Y2,X2] and r7[Y2,X2] in (4,5) and WIJD: o[Y2,X2]=2; break
            elif r7[Y,X]==2: o[Y,X]=vul(i,X,Y)
        continue
    for Y,X in zip(*np.where(m)): o[Y,X]=vul(i,X,Y)
# oude mondjes van de achterste 3 weg (ring -> lichte vulling)
for i in ((0,1,2,3,4) if MODUS=='r7' else (2,3,4)):
    x0,x1,y0,y1=OUDMOND[i]
    for Y in range(y0,y1+1):
        for X in range(x0,x1+1):
            if o[Y,X] in (2,3,5): o[Y,X]=4 if sik(i,X,Y) else 5
# ---- 2. lijnen uit het model ----
def hoekpieken(i,m):
    w=lijnkaart(i); cx,cy=m
    H=np.zeros(72)
    for Y,X in zip(*np.where(w>0)):
        dx,dy=X+.5-cx,Y+.5-cy; r=np.hypot(dx/(HUBX+3),dy/(HUBY+2))
        if r<1: continue
        H[int(((np.degrees(np.arctan2(dy,dx))+180)%360)//5)]+=w[Y,X]
    Hs=np.array([H[k-1]+2*H[k]+H[(k+1)%72] for k in range(72)])/4
    pk=[k for k in range(72) if Hs[k]>=Hs[k-1] and Hs[k]>Hs[(k+1)%72] and Hs[k]>0.15]
    pk=sorted(pk,key=lambda k:-Hs[k])
    gekozen=[]
    for k in pk:
        t=-180+k*5+2.5
        if abs(np.sin(np.radians(t)))<float(opt('minsin',0.55)): continue      # geen horizontale streep naast het mondje
        if all(abs((t-g+180)%360-180)>=float(opt('minhoek',22)) for g in gekozen): gekozen.append(t)
        if len(gekozen)>=NL: break
    return sorted(gekozen),Hs
def dda(p0,p1):
    v=p1-p0; n=int(np.ceil(np.abs(v).max()*2))+1; out=[]
    for t in np.linspace(0,1,n):
        q=(int(np.floor(p0[0]+v[0]*t)),int(np.floor(p0[1]+v[1]*t)))
        if not out or out[-1]!=q: out.append(q)
    return out
MONDC=[]
for i in range(5):
    x0,x1,y0,y1=OUDMOND[i]; MONDC.append(np.array([(x0+x1+1)/2,(y0+y1+1)/2]))
LIJNEN={}
for i in ((1,0) if MODUS=='model' else ()):
    m=MONDC[i]; hoeken,_=hoekpieken(i,m); LIJNEN[i]=hoeken
    for t in hoeken:
        e=np.array([np.cos(np.radians(t)),np.sin(np.radians(t))])
        p0=m+e/np.sqrt((e[0]/(3+HUBX))**2+(e[1]/(1.5+HUBY))**2)
        s=0
        while BIN[i][int(np.floor((m+e*s)[1])),int(np.floor((m+e*s)[0]))] or s<1: s+=0.1
        p1=m+e*s
        L=np.linalg.norm(p1-p0)
        if L<1: continue
        for X,Y in dda(p0,p1+e*0.5):
            if not(0<=Y<64 and 0<=X<64): continue
            if BIN[i][Y,X] or r7[Y,X]==1:
                if BIN[i][Y,X]: o[Y,X]=2
            # buitenste 45%: 2 px (wig naar de rand, fingertoppen)
            if np.linalg.norm(np.array([X+.5,Y+.5])-p0)>float(opt('buiten',0.55))*L:
                if abs(e[1])>abs(e[0]):          # alleen steile lijnen worden 2 px (geen liggende balkjes)
                    X2,Y2=(X+1,Y) if e[0]*e[1]>=0 else (X-1,Y)
                    if BIN[i][Y2,X2]: o[Y2,X2]=2
# ---- 3. mondjes: één stempel voor alle vijf ----
STEMPELS={'M1':[[3,2,2,2,3],[2,5,5,5,2]],          # 5x2: boog boven, licht eronder
          'M2':[[2,5,5,5,2],[3,2,2,2,3]],          # 5x2: kommetje
          'M3':[[3,2,2,3],[2,5,5,2],[3,2,2,3]],    # 4x3 ring
          'M4':[[3,2,2,2,3],[2,5,5,5,2],[3,2,2,2,3]], # 5x3 ring
          'M5':[[2,2,2,2],[2,5,5,2]],              # 4x2
          'M6':[[3,2,2,2,3],[2,5,5,5,2],[0,3,2,3,0]]} # 5x3, ondergrens smaller
ST=STEMPELS[MV]
for i in range(5):
    h,w=len(ST),len(ST[0]); X0_=int(np.floor(MONDC[i][0]-w/2+0.5)); Y0_=int(np.floor(MONDC[i][1]-h/2+0.5))
    # lichte rand van 1 px
    for Y in range(Y0_-1,Y0_+h+1):
        for X in range(X0_-1,X0_+w+1):
            if o[Y,X] in (2,3,4,5): o[Y,X]=4 if sik(i,X,Y) else 5
    for dy,rij in enumerate(ST):
        for dx,k in enumerate(rij):
            if k: o[Y0_+dy,X0_+dx]=k
# ---- 4. gelaat. Jordi: "neem gewoon de vileplume mond en ogen over en doe ze ver genoeg uit elkaar".
# Ogen en mond pixel voor pixel uit graphics/pokemon/vileplume/anim_front.png (bovenste 64x64), Vileplumes eigen
# kleuren omgezet naar de dichtstbijzijnde kleur van ons palet; geplaatst op de plek van de U uit het model
# (linkeroog linksboven op y33, de lichte rij y32 blijft tussen kroonrand en oog), onderlinge afstanden als Vileplume
# (ogen 8 px uit elkaar, net als in de game).
r8A=np.asarray(Image.open('r8/vileplume_r8_gelaatA.png')).astype(int)
assert (o[32:]==np.asarray(Image.open('r8/vileplume_r8_gelaatB.png')).astype(int)[32:]).all()
o[32:]=r8A[32:]
for X in range(25,30): o[33,X]=10                           # U uit het model weg
for X in range(26,29): o[34,X]=10
vp=Image.open('../../../../../graphics/pokemon/vileplume/anim_front.png'); vo=np.asarray(vp)[:64].astype(int)
vpal=np.array(vp.getpalette()[:48]).reshape(-1,3)
GEZ=[(36,24),(37,24),(37,25),(38,32),(38,33),(39,26),(40,26),(40,27),(41,28),(41,29),(41,30),(40,31)]   # ogen (7/8) en mond (14)
for y,x in GEZ: assert vo[y,x] in (7,8,14), (y,x,vo[y,x])
P=np.array(PAL[1:],float)
def dichtst(rgb): return 1+int(np.argmin(((P-np.array(rgb,float))**2).sum(1)))
DX,DY=int(opt('gx',-1)),int(opt('gy',-3))                     # Vileplume (36,24) -> ons (33,23)
KLEUR={}
for y,x in GEZ:
    k=dichtst(vpal[vo[y,x]]); KLEUR[int(vo[y,x])]=k; o[y+DY,x+DX]=k
print('gezicht: Vileplume-kleur -> onze index', {k:(tuple(vpal[k]),v,PAL[v]) for k,v in KLEUR.items()})
opslaan(o,PAL,'%s/vileplume_%s.png'%(RONDE,RONDE))
d=o!=kr
print('mond',MV,'modus',MODUS,'lijnen',{AN[i][0]:[round(t) for t in LIJNEN[i]] for i in LIJNEN})
print('t.o.v. r7: VL/VR-binnen %d px, mondjes achter %d px, krater %d px, gelaat %d px, linkerpoot %d px'%((d&(BIN[0]|BIN[1])).sum(),(d&~(BIN[0]|BIN[1])&(np.arange(64)[:,None]<32)).sum(),(d&KR&(kr>=11)).sum(),d[32:41].sum(),d[41:].sum()))
ch='.K0123abcdeGuomy'
for y in range(0,32): print('%2d '%y+''.join(ch[v] for v in o[y]))
