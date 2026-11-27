# Ronde 4 vanaf ../sprite_bijl_r3/terreurvogel_bijl_r3.png. Silhouet (alpha), oog B, onderdelen en kleurkeuze bevroren.
# Schaduw niet meer uit modelhelderheid per pixel (liep vast: vlakke veelhoeken), maar per onderdeel een rond volume
# (koepel op de afstand tot de eigen rand, licht linksboven) -> 3 tinten per kleurgroep; materiaal (welke kleur) blijft van r3.
import numpy as np; from PIL import Image
B0=Image.open('../sprite_bijl_r3/terreurvogel_bijl_r3.png'); B=np.array(B0).astype(int); S=B.copy()
PAL=[tuple(B0.getpalette()[i*3:i*3+3]) for i in range(16)]
FIG=B>0; H=W=64
OOG={(29,17),(29,18),(30,14),(30,15),(30,16),(30,17),(30,18),(31,15),(31,16),(31,17),(31,18),(32,16),(32,17)}
def leeg(y,x): return not(0<=y<64 and 0<=x<64) or not FIG[y,x]
RAND={(y,x) for y in range(64) for x in range(64) if FIG[y,x] and any(leeg(y+a,x+b) for a,b in((-1,0),(1,0),(0,-1),(0,1)))}
yy,xx=np.mgrid[0:64,0:64]

# ---------- palet (richting v8; schaduw koeler, licht warmer; stappen ±30-40) ----------
# index 6 = gedeelde donkere tint (steen-schaduw/lijn en antraciet-schaduw lagen al dicht bij elkaar, 60 vs 50);
# index 3 komt daardoor vrij als vierde antracietstap (hooglicht op vleugel/schouder).
PAL[6]=(48,46,55)                                                 # gedeeld donker (koel)
PAL[4]=(106,99,92);  PAL[5]=(172,162,146)                         # steen: midden, licht
PAL[7]=(82,78,86);   PAL[8]=(120,111,108); PAL[3]=(158,146,132)   # antraciet: midden, licht, hooglicht (warm)
PAL[9]=(107,61,51);  PAL[10]=(156,58,50); PAL[11]=(160,108,86); PAL[12]=(206,128,84)  # roest donker, rood, tan, oranje
PAL[13]=(84,66,54);  PAL[14]=(146,124,98); PAL[15]=(204,178,138)  # poten: donker/lijn, midden, licht

# ---------- materiaal (uit r3) ----------
# b steen, k kop-bruin, r roest, a antraciet, p poot
def mat_van(y,x,v):
    if v in (3,4,5): return 'b'
    if v in (13,14,15): return 'p'
    if v in (6,7,8): return 'a'
    if v==11: return 'k'
    if v==9: return 'k' if (x<=27 and y<=34) or (x<=21) else 'r'
    if v in (10,12): return 'r'
    return None
MAT=np.full((64,64),None,object)
for y in range(64):
    for x in range(64):
        if FIG[y,x]: MAT[y,x]=mat_van(y,x,B[y,x])
# lijn-/randpixels krijgen het materiaal van de meeste buren (voor de seloutkleur)
for _ in range(4):
    for y in range(64):
        for x in range(64):
            if FIG[y,x] and MAT[y,x] is None:
                c={}
                for a in(-1,0,1):
                    for b in(-1,0,1):
                        if 0<=y+a<64 and 0<=x+b<64 and MAT[y+a,x+b] is not None: c[MAT[y+a,x+b]]=c.get(MAT[y+a,x+b],0)+1
                if c: MAT[y,x]=max(c,key=c.get)

# ---------- onderdelen ----------
def poly(pts):
    """punt-in-veelhoek (x,y)-hoekpunten -> masker"""
    m=np.zeros((64,64),bool); n=len(pts)
    for y in range(64):
        for x in range(64):
            px,py=x+0.5,y+0.5; ins=False
            for i in range(n):
                x1,y1=pts[i]; x2,y2=pts[(i+1)%n]
                if (y1>py)!=(y2>py) and px<x1+(py-y1)*(x2-x1)/(y2-y1): ins=not ins
            m[y,x]=ins
    return m
PART=np.zeros((64,64),int)   # 1 snavel 2 kop 3 lijf 4 vleugel 5 dij 6 poot nabij 7 poot ver 8 nek 9 staart
mb=np.array([[MAT[y,x]=='b' for x in range(64)] for y in range(64)])&FIG
mp=np.array([[MAT[y,x]=='p' for x in range(64)] for y in range(64)])&FIG
PART[FIG]=3
PART[mb]=1
KOP=FIG&~mb&~mp&(yy<=33)&(xx<=27)
PART[KOP]=2
# vleugel: gevouwen op de rug, onderrand van schouder (29,36) naar de veerpunten rechts (model: lichte plaat + donkere punten)
NEK=FIG&~mb&~mp&(yy>=34)&(xx<=27)&(yy<=44)
PART[NEK]=8
STAART=FIG&~mp&(xx>=49)&(yy<=39)
PART[STAART]=9
VLEUGEL=poly([(28,30),(44,29),(50,32),(51,35),(50,38),(49,41),(46,39),(45,42),(42,40),(40,42),(36,40),(31,38),(28,35)])&FIG&~mp
PART[VLEUGEL]=4
DIJ=(((xx-43.5)/6.5)**2+((yy-46.0)/3.4)**2<=1)&FIG&~mp&(PART==3)
PART[DIJ]=5
PART[mp&(xx<=34)]=6
PART[mp&(xx>34)]=7

def afstand(M):
    """euclidische afstand van elke pixel in M tot de dichtstbijzijnde pixel buiten M"""
    out=np.zeros((64,64)); buiten=np.argwhere(~M)
    for y,x in zip(*np.where(M)):
        out[y,x]=np.sqrt(((buiten-[y,x])**2).sum(1).min())
    return out
def blur(A,M,sig):
    out=A.copy(); r=int(2*sig)+1
    for y,x in zip(*np.where(M)):
        s=w=0.0
        for a in range(-r,r+1):
            for b in range(-r,r+1):
                if 0<=y+a<64 and 0<=x+b<64 and M[y+a,x+b]:
                    k=np.exp(-(a*a+b*b)/(2*sig*sig)); s+=k*A[y+a,x+b]; w+=k
        out[y,x]=s/w
    return out
LV=np.array([-0.62,-0.62,0.75]); LV=LV/np.linalg.norm(LV)
def belichting(M,R,sig=1.0,glob=0.0,yc=None,ys=1.0):
    d=afstand(M); dd=np.minimum(d,R); h=np.sqrt(np.maximum(0,R*R-(R-dd)**2))
    h=blur(h,M,sig)
    hp=np.pad(h,1,mode='edge'); Mp=np.pad(M,1)
    gx=np.zeros((64,64)); gy=np.zeros((64,64))
    for y,x in zip(*np.where(M)):
        l=hp[y+1,x] if Mp[y+1,x] else 0; r_=hp[y+1,x+2] if Mp[y+1,x+2] else 0
        u=hp[y,x+1] if Mp[y,x+1] else 0; o=hp[y+2,x+1] if Mp[y+2,x+1] else 0
        gx[y,x]=(r_-l)/2; gy[y,x]=(o-u)/2
    n=np.stack([-gx,-gy,np.ones((64,64))],-1); n/=np.linalg.norm(n,axis=-1,keepdims=True)
    I=(n*LV).sum(-1)
    if glob and yc is not None: I=I-glob*(yy-yc)/ys
    I[~M]=np.nan
    return I
def niveaus(I,M,fs,fl):
    v=I[M]; lo=np.percentile(v,fs*100); hi=np.percentile(v,100-fl*100)
    L=np.full((64,64),-1); L[M&(I<lo)]=0; L[M&(I>=lo)&(I<hi)]=1; L[M&(I>=hi)]=2
    return L
TONEN={'b':(6,4,5),'a':(6,7,8),'k':(9,11,12),'r':(9,10,12),'p':(13,14,15)}
LIJN={'b':6,'a':6,'k':9,'r':9,'p':13}


LOG=[]
def zet(y,x,v,stap):
    if (y,x) in OOG or not FIG[y,x]: raise SystemExit('bevroren pixel %s'%((y,x),))
    if S[y,x]!=v: LOG.append((stap,y,x,int(S[y,x]),int(v))); S[y,x]=v

# ---------- binnenlijnen die blijven (snavel/mond/oogmasker/kop-snavelnaad en de borstplooi boven de nabije poot) ----------
ZWART_HOUD={(y,x) for y in range(64) for x in range(64) if B[y,x]==1 and (y,x) not in RAND and (y,x) not in OOG
            and (x<=24 or (28<=x<=32 and 46<=y<=48))}

# ---------- volume ----------
MASSA=FIG&~mb&~mp&(PART!=2)                                  # nek+lijf+vleugel+dij+staart als één massa (buik onder donker)
I_MASSA=belichting(MASSA,9.0,1.6,0.45,np.where(MASSA)[0].mean(),9.0)
def lv(I,M,fs,fl):
    return niveaus(I,M,fs,fl)
NIV=np.full((64,64),-1)
# lijf: één massa-belichting, veel schaduw onder
ML=PART==3
NIV[ML]=lv(I_MASSA,MASSA,0.30,0.18)[ML]
# nek: buis
for p,(R,sig,fs,fl) in {8:(3.0,0.9,0.34,0.18),9:(3.0,0.9,0.30,0.22),2:(6.0,1.2,0.30,0.14),1:(3.0,0.8,0.28,0.24),
                         5:(3.2,0.9,0.24,0.34),6:(2.0,0.6,0.32,0.30),7:(2.0,0.6,0.32,0.30)}.items():
    M=PART==p; I=belichting(M,R,sig); NIV[M]=lv(I,M,fs,fl)[M]
# vleugel: eigen koepel, één stap lichter dan het lijf (hooglicht = index 3)
MV=PART==4; IV=belichting(MV,5.0,1.0); NIVV=lv(IV,MV,0.50,0.10)
NIV[MV]=NIVV[MV]

def vul():
    for y in range(64):
        for x in range(64):
            if not FIG[y,x] or (y,x) in OOG or (y,x) in RAND or (y,x) in ZWART_HOUD: continue
            m=MAT[y,x]; n=NIV[y,x]
            if PART[y,x]==4 and m=='a': t=(6,7,8,3)[n+1]          # vleugel: 7/8/3, schaduw 6 alleen via lijnen
            elif PART[y,x]==8 and m=='k': t=(9,11,11)[n]           # nek-bruin: geen oranje vlakken
            else: t=TONEN[m][n]
            zet(y,x,t,'volume')

def buiten_normaal(y,x):
    vx=vy=0
    for a in(-1,0,1):
        for b in(-1,0,1):
            if (a or b) and leeg(y+a,x+b): vx+=b; vy+=a
    n=np.hypot(vx,vy); return (vx/n,vy/n) if n else (0,0)
def omlijning():
    """DC: buitenlijn 1 px; aan de lichtkant (boven/links) de donkerste eigen tint, aan de schaduwkant zwart"""
    for y,x in RAND:
        if (y,x) in OOG: continue
        nx,ny=buiten_normaal(y,x)
        licht=(ny<-0.35 and nx<0.75) or (nx<-0.6 and ny<0.5)
        zet(y,x,LIJN[MAT[y,x]] if licht else 1,'omlijning')
def vleugellijnen():
    MV=PART==4
    for y,x in zip(*np.where(MV)):
        if (y,x) in RAND: continue
        onder=[(y+1,x),(y+1,x+1)]
        if any(0<=q[0]<64 and q[1]<64 and FIG[q] and not MV[q] and PART[q] in (3,5) for q in onder):
            zet(y,x,1,'vleugelrand')               # onderrand vleugel over het lijf: zwart (antraciet, diepste schaduw)
            for q in [(y+1,x),(y+2,x)]:
                if FIG[q] and PART[q]==3 and q not in RAND and MAT[q]=='a': zet(q[0],q[1],6,'slagschaduw')
        elif x>0 and FIG[y,x-1] and not MV[y,x-1] and PART[y,x-1] in (3,8) and y>=33:
            zet(y,x,6,'vleugelrand')               # voorrand over de schouder: donkere eigen tint

# ---------- poten (per pixel, naar de modelpoten: schenen met schubringen, tenen met donkere tussenlijnen) ----------
PT={'d':13,'e':14,'f':15,'1':1}
POOT_NABIJ={46:{26:'e'},47:{26:'e'},48:{27:'e'},49:{27:'f',28:'e'},
 50:{27:'f',28:'f',29:'e',30:'e',31:'e',32:'d'},
 51:{26:'f',27:'e',28:'d',29:'e',30:'d'},
 52:{25:'f',26:'e',27:'e',28:'d',29:'d'},
 53:{21:'f',22:'f',23:'f',24:'d',25:'e',26:'d'},
 54:{19:'f',20:'f',21:'e',22:'e',23:'d'},
 55:{12:'f',13:'f',14:'f',15:'e',16:'d',17:'f',18:'e',19:'e',20:'e',21:'e',22:'d'},
 56:{11:'f',12:'e',13:'d',14:'f',15:'e',16:'e',17:'d',19:'e',20:'f',21:'d'},
 57:{11:'e',12:'d',13:'f',14:'e',20:'f',21:'d'},
 58:{11:'f',12:'e',13:'d',21:'e'}}
POOT_VER={48:{49:'e'},49:{48:'f',49:'e',50:'d'},50:{48:'e',49:'e',50:'d'},51:{49:'e',50:'d',51:'d'},
 52:{50:'f',51:'e',52:'d'},53:{51:'e',52:'e',53:'d',55:'e'},54:{52:'f',53:'e',54:'d',55:'d'},
 55:{53:'f',54:'e',55:'e',56:'d'},56:{53:'e',54:'e',55:'e',56:'d'},57:{54:'f',55:'e',56:'d',57:'d'},
 58:{54:'e',55:'e',56:'e',57:'e',58:'d'},59:{54:'e',55:'f',56:'e',57:'d',58:'f',59:'f',60:'e'},
 60:{54:'d',55:'e',56:'d',57:'e',58:'e',59:'d'},61:{57:'d',58:'e'}}
def poten():
    for tab in (POOT_NABIJ,POOT_VER):
        for y,row in tab.items():
            for x,c in row.items():
                if (y,x) in RAND or MAT[y,x]!='p': raise SystemExit('poot buiten vulvlak %s'%((y,x),))
                zet(y,x,PT[c],'poten')
    # alle pootvulpixels moeten in de tabellen staan
    for y,x in zip(*np.where(mp)):
        if (y,x) not in RAND and x not in (POOT_NABIJ if x<=34 else POOT_VER).get(y,{}): print('niet gezet',y,x)

# ---------- hand-afwerking per pixel (lijf, vleugel, staart, kop, nek) ----------
CH={'1':1,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'r':10,'k':11,'o':12,'d':13,'e':14,'f':15}
def pix(tab,stap):
    for y,row in tab.items():
        for x,c in row.items():
            if (y,x) in RAND: raise SystemExit('%s: randpixel %s'%(stap,(y,x)))
            zet(y,x,CH[c],stap)
def rij(y,x0,s):
    return {x0+i:c for i,c in enumerate(s) if c not in '.#-pz '}
def seg(*delen):
    """delen: (x0,'tekens'), aaneengesloten per rij"""
    out={}
    for x0,t in delen:
        for k,c in enumerate(t):
            if c!='-': out[x0+k]=c
    return out
LIJF={
 31:seg((34,'3338'),(58,'888')),
 32:seg((30,'8833338887'),(55,'88888')),
 33:seg((29,'88333888887776'),(53,'888776')),
 34:seg((28,'oor8388888777776'),(50,'888777766')),
 35:seg((27,'rorr'),(31,'88888'),(36,'77777777'),(44,'777777'),(50,'oorrr'),(55,'66')),
 36:seg((26,'rr99'),(30,'8888'),(34,'777777777'),(43,'71'),(45,'777'),(48,'rro6'),(52,'6666')),
 37:seg((26,'6697'),(30,'11'),(32,'8888'),(36,'oo777'),(41,'667o'),(45,'11'),(47,'7r66')),
 38:seg((26,'788766'),(32,'11'),(34,'77or66'),(40,'6'),(41,'11'),(43,'7oor'),(47,'11'),(49,'6')),
 39:seg((26,'78877766'),(34,'11'),(36,'rr666'),(41,'88'),(43,'11'),(45,'rrr'),(48,'66')),
 40:seg((26,'7787777766'),(36,'111'),(39,'677776'),(45,'111'),(48,'6')),
 41:seg((26,'77777777777'),(37,'66'),(39,'111'),(42,'776666')),
 42:seg((26,'7777777777777'),(39,'666'),(42,'11111'),(47,'6')),
 43:seg((26,'777777777'),(35,'66'),(37,'78888'),(42,'66666')),
 44:seg((26,'777777777'),(35,'688338887776'),(47,'6')),
 45:seg((26,'777777'),(32,'6666'),(36,'8888'),(40,'777777'),(46,'666')),
 46:seg((27,'7'),(29,'6666666'),(36,'68'),(38,'7777777'),(45,'66666')),
 47:seg((27,'66'),(31,'666666'),(37,'777777'),(43,'6666666')),
 48:seg((28,'666'),(33,'6'),(41,'77666666')),
 49:seg((29,'6666'),(44,'6666')),
}
KOPNEK={
 24:{16:'o',17:'k',19:'o',20:'k',22:'9'},
 25:seg((15,'ook9okk99')),
 26:seg((14,'ookk9okk99')),
 27:seg((13,'ookkkkk9kk99')),
 28:seg((12,'9kkkkkkkk9k999')),
 29:seg((13,'9kkk'),(19,'kkkk9'),(25,'9')),
 30:seg((19,'kkk99')),
 31:seg((19,'kkk999')),
 32:seg((18,'kkkkrr99')),
 33:seg((17,'9kkkkrr9')),
 34:seg((16,'69kkkrrr9')),
 35:seg((18,'kkkrrrr9')),
 36:seg((17,'kkkrrror9')),
 37:seg((18,'kkrroor9')),
 38:seg((19,'9rrror9')),
 39:seg((20,'9rrrr')),
 40:seg((21,'rr')),
}
SNAVEL={
 30:seg((3,'554'),(10,'444')),
 31:seg((2,'5554444444'),(13,'4')),
 32:seg((2,'554444444'),(12,'444')),
 33:seg((1,'5544444444444666')),
 34:seg((1,'5544444444444'),(16,'6')),
 35:seg((1,'55444444444'),(12,'6'),(14,'666')),
 36:seg((1,'5544444444'),(11,'6'),(13,'66')),
 37:seg((1,'5544444666'),(12,'66')),
 38:seg((2,'5544466'),(11,'66')),
 39:seg((2,'554466')),
 40:seg((2,'55466')),
 41:seg((3,'546')),
 42:seg((4,'46')),
}
BORST={40:seg((23,'887')),41:seg((22,'7887')),42:seg((22,'7787')),43:seg((23,'777')),44:seg((24,'77')),45:seg((25,'6'))}
def hand():
    pix(LIJF,'lijf/vleugel/staart'); pix(KOPNEK,'kop/nek'); pix(SNAVEL,'snavel'); pix(BORST,'borst')
    # losse gekleurde randpixels tussen zwart (nek-voorkant) -> zwart: nooit zwart en kleur om en om op één rand
    for y,x in [(37,17),(39,19)]: zet(y,x,1,'omlijning')

def opslaan(pad,A=None):
    A=S if A is None else A
    im=Image.fromarray(A.astype('uint8'),'P'); p=[]
    for c in PAL: p+=list(c)
    im.putpalette(p+[0]*(768-len(p))); im.save(pad,transparency=0)
def zone(y,x):
    p=PART[y,x]
    return {1:'snavel',2:'kop',3:'lijf',4:'vleugel',5:'dij',6:'poot nabij',7:'poot ver',8:'nek',9:'staart'}[p]
if __name__=='__main__':
    vul(); omlijning(); vleugellijnen(); poten(); hand()
    np.save('r4.npy',S); opslaan('terreurvogel_bijl_r4.png')
    from collections import Counter
    R2=np.array(Image.open('../sprite_bijl_r2/oog_B.png')).astype(int)
    print('gewijzigd t.o.v. r3 per zone:',dict(Counter(zone(y,x) for y,x in zip(*np.where(S!=B)))))
    print('pixels per zone:',dict(Counter(zone(y,x) for y,x in zip(*np.where(FIG)))))
    print('alpha-diff r3',int(((S>0)!=(B>0)).sum()),'alpha-diff r2/oog_B',int(((S>0)!=(R2>0)).sum()))
    print('oog gewijzigd t.o.v. oog_B',sum(int(S[p]!=R2[p]) for p in OOG),'(waarden',[int(S[p]) for p in sorted(OOG)],')')
    print('oog-RGB gelijk:',all(PAL[S[p]]==tuple(Image.open('../sprite_bijl_r2/oog_B.png').getpalette()[R2[p]*3:R2[p]*3+3]) for p in OOG))
    print('kleuren gebruikt',len(set(S[FIG].tolist())),'+ transparant')
