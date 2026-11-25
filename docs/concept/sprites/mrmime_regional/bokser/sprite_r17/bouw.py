# r17 (vanaf r16): armen + vuisten = r9 1-op-1 (zelfde pixels), geplaatst op de schouderballen; broek en benen langer
# door bestaande rijen te herhalen; buik rechtsonder rond; hele sprite 3 px naar rechts en 3 rijen omhoog.
# r16 (vanaf r14/r15): armen = natief model (kale 52-reductie, reductie.py), zelfde verschuiving als hun vuist
# (vuisten uit dezelfde 52-reductie, dus pols loopt de vuist in zoals in het model); ronde romp loopt helemaal door
# en ligt vóór de broek-bovenkant (broek eronder); daarna de r15-omkleuringen + eindkeurderspunten.
# r14 (vanaf r13): verre schouder = Mr. Mime-schouderbal (kopie van de nabije, 1 toon donkerder, deels achter de borst);
# armen = Galar-armdoorsnede (lijn, 3 px huid: licht/midden/schaduw, lijn) langs de pose herhaald; vuist 2 px verder vooruit.
# r13: rechtop, lange dunne ledematen. Kop = r12 (Mr. Mime-formaat), 4 rijen hoger geplaatst.
# Romp + schouderballen = Mr. Mime (zonder heupbollen = geen rok); broek + benen + schoenen = r10/r11 (boksbroek met
# Y-naad en knik; benen 2 rijen langer door herhaalde rechte rijen); verre arm = Galar-bovenarm (rechts), nabije arm =
# Galar-arm (links, V met elleboog onder); vuisten = r11. Alles omgekleurd naar het grijze palet.
import numpy as np, sys
from PIL import Image
P='../../../../../../graphics/pokemon/mr_mime/'
MM=np.array(Image.open(P+'anim_front_gba.png'))[:64,:64]
GA=np.array(Image.open(P+'galar/front.png'))[:64,:64]
r10=np.load('../sprite_r10/bokser.npy'); r11=np.load('../sprite_r11/bokser.npy'); r12=np.load('../sprite_r12/bokser.npy')
A=lambda i,d=0: int(sys.argv[i]) if len(sys.argv)>i else d
HY=-4; DY=0; GY=-2; GX=3      # GX: 3 px naar rechts (r9-vuist past anders niet); GY: hele sprite 2 rijen omhoog (broek 3 lager, benen 1 rij korter -> +2 hoogte)
F=np.zeros((64,64),int)
def put(L):
    for (x,y),v in L.items():
        y+=GY; x+=GX
        if 0<=x<64 and 0<=y<64: F[y,x]=v
# ---- kop: r12-kop (rijen 11-33, zonder lijf) 4 omhoog
kop12=np.load('../sprite_r12/kop.npy')
KOP={(x,y+HY):int(kop12[y,x]) for y,x in zip(*np.where(kop12))}
# ---- Mr. Mime: romp (zonder heupbollen), verre schouder, nabije schouderbal
def mm(rows,xs,keep,cmap,dx=0,dy=DY,src=MM):
    out={}
    for y in rows:
        for x in xs:
            v=int(src[y,x])
            if v and keep(x,y,v):
                c=cmap(x,y,v)
                if c is not None: out[(x+dx,y+dy)]=c
    return out
cirkel=lambda x,y:23<=x<=31 and 31<=y<=41
nab=lambda x,y:(27<=y<=35 and x>=34 and not(y>=34 and x<=34)) and not(y<=28 and x<=36)
def romp_keep(x,y,v):
    if nab(x,y) and v in(5,6,7,8,10,11): return False
    if x<=20 and v!=4: return False
    if v in(5,6,7,8) and not cirkel(x,y): return False        # heupbollen/schouderrand: geen rok
    if v==14 and x>=36 and y>=39: return False                 # rechterheup-lijn van Mr. Mime (losse pixels)
    return v in(15,1,2,4,14,5,6,7,8) and not(y==29 and 26<=x<=33)
def romp_c(x,y,v):
    if v==14: return 1
    if v==4: return 4
    if v in(5,6,7,8): v={5:15,6:15,7:1,8:1}[v]                 # rode cirkel weg: buikwit
    return {15:8,1:7,2:6}[v]
ROMP =mm(range(29,44),range(17,41),romp_keep,romp_c)
VERSCH=mm(range(29,35),range(17,21),lambda x,y,v:v in(5,6,7,8,14),lambda x,y,v:{5:7,6:5,7:4,8:1,14:1}[v])
NABSCH=mm(range(27,36),range(34,45),lambda x,y,v:nab(x,y) and v in(5,6,7,8,10,14),lambda x,y,v:{5:7,6:5,7:4,8:1,10:7,14:1}[v])
# ---- Galar-armen (huid: 7 licht roze, 8 roze, 5 bruine lijn, 4 zwart)
GSK={7:8,8:7,5:1,4:1}
GBOVEN={29:(42,43),30:(41,44),31:(41,44),32:(41,45),33:(42,45),34:(43,47),35:(44,47),36:(45,46)}  # Galar rechterbovenarm
VERARM=mm(range(29,37),range(40,48),lambda x,y,v:GBOVEN[y][0]<=x<=GBOVEN[y][1] and v in GSK,lambda x,y,v:GSK[v],dx=A(1,-30),dy=A(2,-2),src=GA)
# nabije arm: dezelfde Galar-bovenarm, bovenkant onder vuist/schouderbal, elleboog rechtsonder naar buiten (onderarm erachter gevouwen, zoals r9)
NABARM=mm(range(29,37),range(40,48),lambda x,y,v:GBOVEN[y][0]<=x<=GBOVEN[y][1] and v in GSK,lambda x,y,v:{8:8,7:7,5:1,4:1}[v],dx=A(3,-4),dy=A(4,6),src=GA)
# ---- r11/r12-delen
VUIST={}
for y in range(25,32):
    for x in range(8,16):
        if r11[y,x] and not(y==31 and x>=16): VUIST[(x-3+A(7,-2),y-5)]=int(r11[y,x])
BORST={(x,y-4):int(r12[y,x]) for y in range(34,40) for x in range(30,38) if r12[y,x] and (x,y) in
       {(x0+i,yy) for yy,x0,n in [(34,32,4),(35,31,6),(36,30,8),(37,30,8),(38,31,7),(39,32,5)] for i in range(n)}}
V={(x,y+HY):3 for yy,x0,n in [(34,26,6),(35,26,4),(36,26,3),(37,27,2),(38,28,1)] for x in range(x0,x0+n) for y in [yy]}
# broek+benen+schoenen uit r10: broek = r11-rijen (26-30,32,34,35), benen 36-44 met rij 37 en 42 herhaald, schoenen 45-51
rows=[26,27,28,29,30,32,34,35,36,37,38,39,40,41,42,42,43,44,45,46,47,48,49,50,51]
ONDER={}
Y0=A(5,37)
for i,ry in enumerate(rows):
    for x in range(35):
        if r10[ry,x] and not(ry<=35 and x<14): ONDER[(x+7,Y0+i)]=int(r10[ry,x])
# ---- lagen (achter -> voor)
# ---- r14: verre schouderbal
# heupbol van Mr. Mime (linkerheup, rond, rechterkant achter de romp) als verre schouder, 3 px naar links, 8 rijen omhoog
VERBAL={(x+A(8,-21),y+A(9,0)):{7:7,5:5,4:4,1:1,2:2}[v] for (x,y),v in NABSCH.items()}   # tweede Mr. Mime-schouderbal
# ---- r14: armen als buis met Galar-doorsnede (lijn, licht, midden, schaduw, lijn)
def buis_h(cols):              # cols: {x: bovenste huidrij}; doorsnede verticaal, licht boven
    out={}
    for x,t in cols.items():
        out[(x,t-1)]=1; out[(x,t)]=8; out[(x,t+1)]=7; out[(x,t+2)]=6; out[(x,t+3)]=1
    return out
def buis_v(rows):              # rows: {y: linker huidkolom}; doorsnede horizontaal, licht links
    out={}
    for y,l in rows.items():
        out[(l-1,y)]=1; out[(l,y)]=8; out[(l+1,y)]=7; out[(l+2,y)]=6; out[(l+3,y)]=1
    return out
VX=A(6,0)
r9=np.load('../sprite_r9/bokser.npy')
def r9deel(rijen,dx,dy):        # rijen: {r9-rij: (x0,x1)} -> laag in put-coördinaten (vóór GY)
    return {(x+dx,y+dy-GY):int(r9[y,x]) for y,(x0,x1) in rijen.items() for x in range(x0,x1+1) if r9[y,x]}
FDX,FDY=A(10,-12),A(11,9); NDX,NDY=A(12,-9),A(13,11)
VUIST =r9deel({8:(13,15),9:(12,16),10:(11,17),11:(10,17),12:(10,18),13:(10,18),14:(10,19),15:(12,19),16:(14,18)},FDX,FDY)
VERARM=r9deel({16:(19,21),17:(17,26),18:(17,26),19:(18,26),20:(19,26),21:(20,27),22:(21,29)},FDX,FDY)
BORST =r9deel({19:(40,44),20:(38,44),21:(38,45),22:(37,45),23:(37,45),24:(38,46),25:(38,45),26:(40,45)},NDX,NDY)
NABARM=r9deel({22:(46,50),23:(46,50),24:(47,51),25:(46,51),26:(46,52),27:(46,52),28:(48,52),29:(50,52)},NDX,NDY)
VERSCH={}
for k in [(42,34),(43,35)]: NABSCH.pop(k,None)            # losse pixels van Mr. Mimes manchet naast de bal
for L in (VERARM,VERBAL,VERSCH,ONDER,ROMP,V,NABARM,NABSCH,KOP,BORST,VUIST): put(L)   # romp vóór de broek-bovenkant
for x in (40+GX,41+GX): F[34+GY,x]=1 if F[34+GY,x]==0 else F[34+GY,x]   # onderrand schouderbal dicht
G=F.copy()
for y,x in zip(*np.where(F>=5)):
    for dy,dx in((1,0),(-1,0),(0,1),(0,-1)):
        if F[y+dy,x+dx]==0: G[y+dy,x+dx]=1
F=G
if F[34+GY,19+GX]==0: F[34+GY,19+GX]=1                               # gaatje tussen verre bal en romp dicht
# ---- r15-omkleuringen (keurder r15) op de r16-plaats + eindkeurder r15. Kop/romp/schouders: r15-y-2; broek: r15-y+1;
#      benen/schoenen vanaf r15-rij 48: gelijk; r15-rij 45-46: +1. (Punt 5 en 8 van r15 vervallen: buik nu uit Mr. Mime,
#      nabije onderarm nu uit het model.)
def z(x,y,van,naar):
    x+=GX
    assert F[y,x]==van,(x,y,int(F[y,x]),van); F[y,x]=naar
for x,y in [(41,27),(42,28),(43,29),(42,33)]: z(x,y-2,4,1)
for x,y in [(40,33),(41,33)]: z(x,y-2,1,4)
z(42,30,5,4)
for x,y in [(16,29),(17,29),(16,30),(17,30)]: z(x,y-2,7,5)
for y in range(26,31):
    for x in range(15+GX,21+GX):
        if F[y,x]==5 and not((x-GX,y) in [(16,27),(17,27),(16,28),(17,28)]): F[y,x]=4
for x in (15,16,17): z(x,32,4,1); z(x,33,1,0)
z(20,25,4,1); z(21,26,4,1)
for x,y in [(27,49),(28,50),(29,51),(29,52),(29,53),(29,54)]: z(x,y,8,1); z(x-1,y,1,0)
for y,xm in {46:29,47:29,48:29,49:30,50:31,51:31,52:31,53:31,54:31}.items():
    for x in range(20+GX,xm+1+GX):
        if F[y,x]==8: F[y,x]=7
        elif F[y,x]==7: F[y,x]=6
for x in (27,28,29):                        # broeksband (r15 rij 38 -> 39): alleen waar de broek niet achter de buik zit
    if F[39,x+GX]==6: F[39,x+GX]=3
z(27,43,1,2)                                # Y-naad (r15 rij 42 -> 43)
z(47,9,3,1); z(48,10,3,1); z(40,13,3,1)     # kuif (r15 (47,11),(48,12),(40,15))
for x,y in [(36,59),(35,60),(36,60),(37,61)]: z(x,y,5,3)   # nabije schoen: hooglicht linksboven
for x,y in [(32,58),(33,58)]: z(x,y,3,5)
# buik-onderkant: schaduw (208) als sikkel die naar links uitloopt i.p.v. een horizontale band
for y,xm in {35:28,36:26,37:24,38:25,39:24}.items():
    for x in range(20+GX,xm+1+GX):
        if F[y,x]==7: F[y,x]=8
# ---- r17: buik rechtsonder rond (rij 39 vóór de 3-rij-verschuiving): bandpixels -> buikschaduw, rand 1 px naar rechts
for x in (33,34,35): assert F[39,x]==6; F[39,x]=7
assert F[39,36]==3; F[39,36]=1
# ---- r17: broekpijpen +2 en benen +1 door bestaande rijen te herhalen; daarna 3 rijen omhoog en 3 px naar rechts
def herhaal(F,y):               # rij y nog eens invoegen onder zichzelf (alles eronder 1 rij omlaag)
    return np.vstack([F[:y+1],F[y:y+1],F[y+1:-1]])
assert not F[61:].any() or True
F=np.vstack([F,np.zeros((4,64),int)])
for y in A(14,[43,44]) if False else [44,44]: F=herhaal(F,y)      # pijpen (rij '1333332133333221')
F=herhaal(F,54)                                                   # rechte beenrij
F=F[3:67]
np.save('ruw.npy',F)
ys,xs=np.where(F); print('maat',xs.max()-xs.min()+1,'x',ys.max()-ys.min()+1,'rijen',ys.min(),ys.max())
# aanroep: python3 bouw.py -30 -2 -4 6 37 -2 -4 -21 0

# aanroep: python3 bouw.py -30 -2 -4 6 40 -2 -4 -21 0

# aanroep r17: python3 bouw.py -30 -2 -4 6 40 -2 -4 -21 0
