# Shuppetto r4: verder op r3 (r3.npy = ../r3/cur.npy). Registratie als r3: spritepixel (i,j) = modelblok x 24+(i-1)*S,
# y 1+(j-4)*S, S = 968/62. Per benoemde reparatie een zone; LOG telt gewijzigde pixels per zone.
# Volgorde: python3 build.py -> cur.npy, banette_evo.png; python3 vel.py; python3 controle.py cur.npy; python3 diff.py
import numpy as np
g=np.load('r3.npy').copy(); r3=g.copy()
LOG={}
def put(name,pts):
    n=0
    for (x,y),v in pts:
        if not(0<=x<64 and 0<=y<64): continue
        if g[y,x]!=v: n+=1
        g[y,x]=v
    LOG[name]=LOG.get(name,0)+n
def grid(name,x0,y0,rows,key):
    pts=[]
    for dy,row in enumerate(rows):
        for dx,ch in enumerate(row):
            if ch in ' _': continue
            pts.append(((x0+dx,y0+dy),key[ch]))
    put(name,pts)
K=1; GL,GM,GD=2,3,4; CYAAN,RM,RD,MOND,GEEL=5,6,7,8,9; BL,BM,BD,WIT,NAV,RL=10,11,12,13,14,15
RING_OUD=5
# ===== palet: oogring (224,64,48) en rood mid (208,64,64) zijn bijna gelijk -> ring wordt RM; plaats 5 = cyaan Shuppet-oog
put('palet_ring_naar_RM',[((i,j),RM) for j,i in zip(*np.where(r3==RING_OUD))])

# ===== 1. MOND: vorm = r3/model (mondmasker D uit mondcov, r3 build.py), hele opening bijna zwart (K, helderheid 27);
#          huid die aan de opening grenst (8-buren) wordt middentint: grijs GM, rood RM (tandpunten licht tegen zwart).
D={26:[41],27:[40,41],28:[40,41],29:[39,40,41],30:[39,40,41],31:[39,40,41],
   32:[15,33,38,39,40,41],33:[15,32,33,34,35,38,39,40,41],34:[16]+list(range(32,42)),35:[16,20,21,25,26]+list(range(31,42)),
   36:[17,19,20,21,25,26,27]+list(range(31,41)),37:list(range(17,23))+list(range(24,29))+list(range(30,35))+list(range(36,41)),
   38:list(range(17,34))+[38,39,40],39:list(range(18,34))+[40],40:[19,20]+list(range(22,28))+list(range(29,34)),
   41:[23,24,25,26,30,31,32],42:[24,25,31,32]}
M=np.zeros((64,64),bool)
for j,xs in D.items():
    for i in xs: M[j,i]=True
put('mond',[((i,j),K) for j,i in zip(*np.where(M))])
PM=np.pad(M,1); buur=np.zeros((64,64),bool)
for dy in (-1,0,1):
    for dx in (-1,0,1): buur|=PM[1+dy:65+dy,1+dx:65+dx]
pts=[]
for j in range(31,45):
    for i in range(14,42):
        if M[j,i] or not buur[j,i]: continue
        if 0 in (g[j-1,i],g[j+1,i],g[j,i-1],g[j,i+1]): continue   # buitenrand blijft selout
        v=g[j,i]
        if v==GD: pts.append(((i,j),GM))
        elif v==RD: pts.append(((i,j),RM))
        elif v==MOND: pts.append(((i,j),RM if i>=27 else GM))
put('mond_huid',pts)

# ===== 4. RECHTEROOG HOOFD: iris (geel + pupil) 0,4-0,5 rij te hoog (model: geel r26,5-29,5 midden 27,5; r3 midden 27,0).
#          Geel x31 r26-29 (midden 27,5), pupil x32 r27-28 (was r26-28), ring x30/x33 en boven/onder de pupil tot r29.
grid('oog_rechts',30,26,[
 "oyoo",   # 26
 "oyko",   # 27
 "oyko",   # 28
 "oyoo"],  # 29
 {'o':RM,'y':GEEL,'k':K})

# ===== 3. LINKERKRUIS: silhouet = model (dekking >= 0,5, red2.py 0 16 12 28): bovenbalk x3-9 r18-22 met kap links
#          (inkeping x6-7 r18), onderbalk naar links tot x1 r24-25 (r3 liep tot x0 en r17 x3-4: buiten het model).
#          Rand zwart (randpixels van het silhouet; hoed-kolom x10 en mutspunt-rand r25 x5-9 blijven).
#          Tinten uit het model: kopvlak van de kap donker (x4 r20, x5 r21: model 93-103), bovenvlak van beide balken licht,
#          rest middentint, schaduw onder de bovenbalk (x7 r23) en de onderkant van de onderbalk (x5-6 r24, x4 r25) donker.
grid('kruis_links',0,17,[
#  0123456789
 "___..____k",   # 17
 "__..kk__kl",   # 18
 "__.kllkkll",   # 19
 "___kdllllm",   # 20
 "____kdmmmm",   # 21
 "___.kmmmmd",   # 22
 "__.kllldmd",   # 23
 ".kkmlddkdd",   # 24
 ".kmmd_____",   # 25
 "..kkk_____",   # 26
 "..n_______",   # 27
 ],{'k':K,'l':GL,'m':GM,'d':GD,'n':NAV,'.':0})

# ===== 2/5. SHUPPETS: zone leeg, opnieuw uit het model (red2.py: silhouet dekking >= 0,5, donker < 70, mediaan-
#          helderheid per blok: +-170 licht, +-140 mid, +-100 schaduw). Hoorn, ronde kop, buikje met twee armpjes,
#          golvende zoom. Ogen als in het model: zwarte rand, cyaan iris, pupil (marine) als verticale spleet.
SK={'k':K,'n':NAV,'L':BL,'M':BM,'D':BD,'E':CYAAN,'.':0}
def leeg(x0,y0,x1,y1):
    put('shuppet_leeg',[((i,j),0) for j in range(y0,y1) for i in range(x0,x1)])
leeg(3,39,17,57); leeg(45,42,62,63)
grid('shuppet_L',3,39,[
#  34567890123456
 ".....nk.......",   # 39 hoorn
 "....nLk.......",   # 40
 "....nLMk......",   # 41
 "...nLLMMMkk...",   # 42
 "..nLLLMMMMk...",   # 43
 ".nkkLMMkkkMk..",   # 44
 ".kEnLMknEEkD..",   # 45 pupil links in het nabije oog (model x10,6-11,2)
 ".kEnLMknEEkD..",   # 46
 ".kkkMMMkkkDk..",   # 47
 "..kMMnnMMDk...",   # 48 mondje (model: donker x7,9-9,3 r48,6)
 "...kkDDDDk....",   # 49
 ".....kDDDDkkk.",   # 50
 "....nLLLMnMDk.",   # 51
 "...nLLLLMnMDk.",   # 52
 "....knLMMnDDk.",   # 53
 "....kMLMDnDDk.",   # 54
 "....kMMDkDDk..",   # 55
 ".....kkk.k....",   # 56
 ],SK)
grid('shuppet_R',46,42,[
#  4567890123456789 (x46..61)
 "......n.........",   # 42 hoorn
 "......nk........",   # 43
 ".....nLk........",   # 44
 ".....nLMk.......",   # 45
 "....nLLMk.......",   # 46
 "....nLLMMk......",   # 47
 "...nLLLMMMk.....",   # 48
 "..nLLLLMMMDk....",   # 49
 "..kkLLMkkkMDk...",   # 50
 ".kEnLMkEnEkDk...",   # 51
 ".kEnMMkEnEkD....",   # 52
 "..kkMMDkkkk.....",   # 53
 "...kkDDDDk......",   # 54
 ".....kDDk.......",   # 55
 "...nnnDDDkkkk...",   # 56
 "..nLLknLLMMDMk..",   # 57
 "..kkk.nLMMDDMk..",   # 58
 "......nLMDDkkk..",   # 59
 ".....nLMkDDDk...",   # 60
 ".....kkk.kkk....",   # 61
 ],SK)
def draad(naam,pts):
    put(naam,[((x,y),NAV) for x,y in pts if g[y,x]==0])
draad('draden_terug',[(4,39),(4,40),(5,41),(5,42),(11,39),(11,40),(11,41),(13,39),(13,40),(13,41),
    (50,42),(50,43),(50,44),(50,45),(50,46),(50,47),(58,42),(57,43),(57,44),(57,45),(57,46),(57,47),
    (60,42),(59,47),(59,48),(59,49),(59,50),(59,51),(58,52),(58,53),(58,54),(58,55)])
np.save('cur.npy',g)
from view import png; png(g,'banette_evo.png')
print(LOG)
