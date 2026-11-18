# Shuppetto r3: verder op r2 (r2.npy = ../r2/cur.npy). Registratie: spritepixel (i,j) = modelblok x 24+(i-1)*S, y 1+(j-4)*S,
# S = 968/62 (getoetst met reg.py: dx 0, dy 0 geeft de beste silhouet-IoU en zwart-correlatie). Per benoemde reparatie een zone.
# Volgorde: python3 mondcov.py; python3 build.py -> cur.npy, banette_evo.png; python3 vel.py; controle: python3 controle.py cur.npy
import numpy as np; from scipy import ndimage as nd
g=np.load('r2.npy').copy(); r2=g.copy()
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
K=1; GL,GM,GD=2,3,4; RING,RM,RD,MOND,GEEL=5,6,7,8,9; BL,BM,BD,WIT,NAV,RL=10,11,12,13,14,15
GRIJS={GL,GM,GD}; ROOD={RM,RD,RL}; HUID=GRIJS|ROOD

# ===== 1. MOND: vorm gemeten op het model (mondcov.py: donker L<70 per spritepixel, >= 0,5; halve-pixelkaart voor de punten):
#          bovenrand met 3 boventanden (punten x18 r36, x23 r37, x29 r37), 3 ondertanden (punten x21 r40, x28 r40, x35 r37),
#          linkerlijn van de mond (x15 r32 -> x17 r36), rechterarm langs de wang tot r26. Rand zwart, binnenkant MOND.
#          Huid in de zone opnieuw: grijs links van de naad, rood rechts; boventanden licht (GM/RM), onderkaak schaduw (GD/RD).
D={26:[41],27:[40,41],28:[40,41],29:[39,40,41],30:[39,40,41],31:[39,40,41],
   32:[15,33,38,39,40,41],33:[15,32,33,34,35,38,39,40,41],34:[16]+list(range(32,42)),35:[16,20,21,25,26]+list(range(31,42)),
   36:[17,19,20,21,25,26,27]+list(range(31,41)),37:list(range(17,23))+list(range(24,29))+list(range(30,35))+list(range(36,41)),
   38:list(range(17,34))+[38,39,40],39:list(range(18,34))+[40],40:[19,20]+list(range(22,28))+list(range(29,34)),
   41:[23,24,25,26,30,31,32],42:[24,25,31,32]}
M=np.zeros((64,64),bool)
for j,xs in D.items():
    for i in xs: M[j,i]=True
NAADX={32:24,33:24,34:25,40:27,41:27,42:27,43:27,44:27}
P=np.pad(r2>0,1)
binnen=lambda i,j:P[j,i+1] and P[j+2,i+1] and P[j+1,i] and P[j+1,i+2]
def huid(i,j):
    nx=NAADX.get(j)
    if nx is not None and i==nx: return GD
    grijs=i<(nx if nx is not None else 27)
    if j<=37: return GM if grijs else (RD if i>=41 else RM)
    if grijs: return GM if (j,i) in ((40,21),(41,20),(41,21),(41,22)) else GD
    if (j,i) in ((40,28),(41,28),(41,29)): return RM
    if 34<=i<=37 and j<=40: return RM
    return RD
pts=[]
for j in range(32,45):
    for i in range(14,42):
        if M[j,i]: continue
        if not binnen(i,j): continue
        if r2[j,i] in (NAV,): continue
        if j>=41 and r2[j,i] not in (MOND,K) and not (j<=42): continue
        pts.append(((i,j),huid(i,j)))
put('mond_huid',pts)
PM=np.pad(M,1); pts=[]
for j,i in zip(*np.where(M)):
    rand=not(PM[j,i+1] and PM[j+2,i+1] and PM[j+1,i] and PM[j+1,i+2])
    pts.append(((i,j),K if rand else MOND))
put('mond',pts)

# ===== 4. LINKEROOG: spitse amandelkas uit de halve-pixelkaart (half.py 13 24 26 33): twee punten boven (x16, x19-20 r26),
#          bovenlid r27, schuine rechterkant naar de punt rechtsonder (x22 r30-31), ronde onderkant links; 1 rij lager dan r2
OK={'k':K,'D':MOND,'O':RING,'Y':GEEL,'g':GM}
grid('oog_links',15,25,[
 "_____g__",
 "gkggkkgg",
 "gkkkkkgg",
 "gkDOOkgg",
 "gkOYkOkg",
 "gkOYkODk",
 "ggkDODkk",
 "___kkkgg"],OK)

# ===== 7. LINKS ONDER HET KRUIS: de r2-"linkerarm" (x4-6 r26-31) staat niet in het model (dekking x4-5 <= 0,1: alleen
#          twee draden); weg. Mutspunt naar het belletje uit het model (cls.py/half.py 0 22 17 40): linkerlijn x7, vulling
#          donkergrijs (in de schaduw onder de muts), binnenlijn r28 x11-12 -> x10 r29-30, punt x8 r31-32 op de bel.
LK={'k':K,'d':GD,'m':GM,'.':0,'e':NAV}
grid('mutspunt_links',3,26,[
#  34567890123
 "_.e.kdddddk",   # 26
 "..e.kdddddk",   # 27
 "..e.kdddkkk",   # 28
 "..e.kddkddk",   # 29
 "..e.kddke_k",   # 30
 "..e.kdk.e_k",   # 31
 "__e.kdk_e_k",   # 32
 ],LK)

# ===== 2/3. GRIJZE MUTS: buitenlijn als vloeiende curve op de modelomtrek (silcmp.py + half.py 4 6 27 27):
#          links 15,13,12,11,10,10 (geen bult op r11-12), rechtsboven één zwarte schaduwlijn 1 px diagonaal x22-23 r9 -> x26 r12
#          (model: zwart aan de schaduwkant), boven/links GD-selout (lichtkant, model heeft daar geen zwarte lijn).
#          Schaduwvlak rechts (model 'd' vanaf x19-20) zonder losse GM-strook ertussen.
MK={'k':K,'d':GD,'m':GM,'l':GL,'.':0}
grid('muts_rand_boven',10,8,[
 ".....ddddddd",
 "...ddlllldddkk",
 "..dlllllllddddk",
 ".dlllllllldddddkkk",
 "dlllllllllddddddk",
 ],MK)
# licht linksboven als vlak dat de koepel volgt (onderrand rond, geen rechte band op r13)
LICHT={9:(15,18),10:(13,19),11:(12,19),12:(11,18),13:(12,16),14:(12,14)}
pts=[]
for j in range(9,16):
    for i in range(11,22):
        if g[j,i] in (GL,GM):
            a=LICHT.get(j); pts.append(((i,j),GL if a and a[0]<=i<=a[1] else GM))
put('muts_licht',pts)
# steken over de naad: model r18,5-19 (x23,5-25) en r22 (x22,5-25); r2 had de bovenste op r17 (1,5 rij te hoog)
put('steek_weg',[((24,17),GM),((25,17),GD),((26,17),GD)])
put('steek',[((23,18),K),((24,18),K),((25,18),K)])
put('steek_schaduw_weg',[((x,19),RM) for x in (25,26) if g[19,x]==RD])

# ===== 5. SHUPPETS: silhouet = model (shup_L/R.npy, dekking >= 0,5), opgebouwd als kop+hoorn, armpjes, lijfje met de
#          binnenlijnen van het model (half.py-kaart); ogen als echte ogen naar de Gen 3 Shuppet (zwarte rand boven/onder,
#          licht oog met donkere pupil), verre oog smal op de koprand. Selout marine aan de lichtkant, zwart aan de schaduwkant.
SK={'k':K,'n':NAV,'L':BL,'M':BM,'D':BD,'W':WIT,'e':NAV,'.':0}
def leeg(x0,y0,x1,y1):
    put('shuppet_leeg',[((i,j),0) for j in range(y0,y1) for i in range(x0,x1)])
leeg(3,39,17,57); leeg(45,43,62,63)
grid('shuppet_L',3,39,[
#  34567890123456
 "_____n________",   # 39 hoorn
 "____nLk_______",   # 40
 "____nLMkk_____",   # 41
 "___nLLLMMkk___",   # 42
 "__nLLLLMMMk___",   # 43
 "__kLLLMLkkkk__",   # 44
 "_kWkLLMkWWWk__",   # 45
 "_kWkLMMkWnWk__",   # 46
 "_kkMMMMMkkkk__",   # 47
 "__kMMMnnDDk___",   # 48
 "___kkDDDkk____",   # 49
 "_____kDDDknk__",   # 50
 "____nLLLLnMMk_",   # 51
 "___nLLLLnLnMk_",   # 52
 "___kkkLLnMnDk_",   # 53
 "____kMMMMDDk__",   # 54
 "_____kkkkkk___",   # 55
 "______________",   # 56
 ],SK)
grid('shuppet_R',47,43,[
#  47890123456789 (x47..60)
 "______k_______",   # 43 hoorn
 "_____nk_______",   # 44
 "_____nLk______",   # 45
 "____nLMk______",   # 46
 "____nLMMk_____",   # 47
 "___nLLMMMkk___",   # 48
 "__nLLLMMMMDk__",   # 49
 "_nkLLMkkkMDk__",   # 50
 "_kWkLkWWWkDk__",   # 51
 "_kWkMkWnWkDk__",   # 52
 "_kkMMMkkkDk___",   # 53
 "__kkMDDDDk____",   # 54
 "____kDDDk_____",   # 55
 "__nnLMMMMDDk__",   # 56
 "_nLLnLLMMMDDk_",   # 57
 "_kkk_nLMMMDDk_",   # 58
 "_____nLMMDDDk_",   # 59
 "_____nMkDDDk__",   # 60
 "_____kk_kkk___",   # 61
 ],SK)
def draad(naam,segs):
    pts=[]
    for x,a,b in segs:
        for j in range(a,b+1):
            if g[j,x]==0: pts.append(((x,j),NAV))
    put(naam,pts)
draad('draden_terug',[(4,39,40),(5,41,41),(11,39,41),(13,39,41),(50,43,47),(57,43,47),(59,47,51),(58,52,55),(56,43,40)])

# ===== 6. RECHTERBEL los van het kruis: het kruis ligt achter de bel; waar het lichte kruis direct tegen de belrand
#          komt (x55 r19-22) wordt het de schaduwtint van het kruis (bel werpt schaduw), zodat er een donkere rand tussen zit
put('bel_rechts_los',[((55,j),GD) for j in range(19,23) if g[j,55] in (GL,GM)])
np.save('cur.npy',g)
from view import png; png(g,'banette_evo.png')
print(LOG)
