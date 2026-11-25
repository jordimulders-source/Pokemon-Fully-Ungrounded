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
HY=-4; DY=0
F=np.zeros((64,64),int)
def put(L):
    for (x,y),v in L.items():
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
    return v in(15,1,2,4,14,5,6,7,8) and not(y==29 and 26<=x<=33)
def romp_c(x,y,v):
    if v==14: return 1
    if v==4: return 4
    if v in(5,6,7,8): v={5:15,6:15,7:1,8:1}[v]                 # rode cirkel weg: buikwit
    return {15:8,1:7,2:6}[v]
ROMP =mm(range(29,40),range(17,41),romp_keep,romp_c)
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
        if r11[y,x] and not(y==31 and x>=16): VUIST[(x-3,y-5)]=int(r11[y,x])
BORST={(x,y-4):int(r12[y,x]) for y in range(34,40) for x in range(30,38) if r12[y,x] and (x,y) in
       {(x0+i,yy) for yy,x0,n in [(34,32,4),(35,31,6),(36,30,8),(37,30,8),(38,31,7),(39,32,5)] for i in range(n)}}
V={(x,y+HY):3 for yy,x0,n in [(34,26,6),(35,26,4),(36,26,3),(37,27,2),(38,28,1)] for x in range(x0,x0+n) for y in [yy]}
# broek+benen+schoenen uit r10: broek = r11-rijen (26-30,32,34,35), benen 36-44 met rij 37 en 42 herhaald, schoenen 45-51
rows=[26,27,28,29,30,32,34,35,36,37,37,38,39,40,41,42,42,43,44,45,46,47,48,49,50,51]
ONDER={}
Y0=A(5,37)
for i,ry in enumerate(rows):
    for x in range(35):
        if r10[ry,x] and not(ry<=35 and x<14): ONDER[(x+7,Y0+i)]=int(r10[ry,x])
# ---- lagen (achter -> voor)
for (x,y),v in {(14,29):7,(15,31):7}.items(): VERARM[(x,y)]=v if (x,y) in VERARM else None   # losse glanspixels in de verre arm
VERARM={k:v for k,v in VERARM.items() if v is not None}
for k in [(42,34),(43,35)]: NABSCH.pop(k,None)            # losse pixels van Mr. Mimes manchet naast de bal
for L in (VERARM,VERSCH,ROMP,ONDER,V,NABARM,NABSCH,KOP,BORST,VUIST): put(L)   # broek over de onderkant van de romp
for x in (40,41): F[34,x]=1 if F[34,x]==0 else F[34,x]   # onderrand schouderbal dicht
G=F.copy()
for y,x in zip(*np.where(F>=5)):
    for dy,dx in((1,0),(-1,0),(0,1),(0,-1)):
        if F[y+dy,x+dx]==0: G[y+dy,x+dx]=1
F=G; np.save('ruw.npy',F)
ys,xs=np.where(F); print('maat',xs.max()-xs.min()+1,'x',ys.max()-ys.min()+1,'rijen',ys.min(),ys.max())
