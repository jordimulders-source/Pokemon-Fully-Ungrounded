# Shuppetto r5: verder op r4 (r4.npy = ../r4/cur.npy). Registratie: spritepixel (i,j) = modelblok x 24+(i-1)*S,
# y 1+(j-4)*S, S = 968/62. Per reparatiepunt van keuring_r4 een zone; LOG telt gewijzigde pixels per zone.
# python3 build.py -> cur.npy, banette_evo.png; python3 vel.py cur.npy vel.png; python3 controle.py cur.npy; python3 diff.py
import numpy as np
g=np.load('r4.npy').copy(); r4=g.copy()
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
KEY={'k':K,'l':GL,'m':GM,'d':GD,'c':CYAAN,'r':RM,'R':RD,'b':MOND,'y':GEEL,'L':BL,'M':BM,'B':BD,'w':WIT,'n':NAV,'e':RL,'.':0,'K':K}

# ===== 2. MOND: vorm = r4-mondmasker (= model, mmask.py/mcls.py), alleen de 1 px rand K, binnenkant donkerbruin (index 8,
#          palet: lichter gemaakt zodat hij op 1x van K afsteekt; model-vulling mediaan (65,52,55)).
D={26:[41],27:[40,41],28:[40,41],29:[39,40,41],30:[39,40,41],31:[39,40,41],
   32:[15,33,38,39,40,41],33:[15,32,33,34,35,38,39,40,41],34:[16]+list(range(32,42)),35:[16,20,21,25,26]+list(range(31,42)),
   36:[17,19,20,21,25,26,27]+list(range(31,41)),37:list(range(17,23))+list(range(24,29))+list(range(30,35))+list(range(36,41)),
   38:list(range(17,34))+[38,39,40],39:list(range(18,34))+[40],40:[19,20]+list(range(22,28))+list(range(29,34)),
   41:[23,24,25,26,30,31,32],42:[24,25,31,32]}
M=np.zeros((64,64),bool)
for j,xs in D.items():
    for i in xs: M[j,i]=True
P=np.pad(M,1); inner=M&P[:-2,1:-1]&P[2:,1:-1]&P[1:-1,:-2]&P[1:-1,2:]
put('2 mond',[((i,j),MOND) for j,i in zip(*np.where(inner))])
#   tandpuntjes linksonder: de 1 px huidstrook tussen mondrand en buitenrand (model: grijze strook x16-18 r37-40; (16,38) en
#   (17,39) liggen óp de silhouetrand = selout) wordt één doorlopende strook in D (was m/d/d/m om en om = losse puntjes);
#   tandpunt (21,40) zit vast aan de tandbasis r41 (model: tand x20,5-21,5 r39,5-41).
put('2 mond_tanden',[((16,37),GD),((18,40),GD)])

# ===== 1. OGEN HOOFD: model: rode ring, crèmegele iris aan beide kanten van een zwarte verticale spleet, in een donkere kas.
#   Rechteroog: geel x30,8-33,3 r26,5-29,6, spleet x31,6-32,0 r26,8-29,3, ring tot x34,0 -> Y x31/x33, K x32 r27-28,
#   ring x30 en x34 (+1 px in de kas, toegestaan), ring boven r25. Kas-ruis (30,25) b -> K (één kleur per rand).
grid('1 oog_rechts',29,25,[
#  9012345
 "kkrrrbb",   # 25
 "kryyyrk",   # 26
 "brykyrk",   # 27
 "brykyrk",   # 28
 "bryyyrk",   # 29
 ],{**KEY,'r':RM})
#   Linkeroog: geel x18,4-19,9 r28,7-31,3, spleet x19,3-19,6 -> Y x18/x20, K x19 r29-30, ring x17/x21 en r28/r31 (x18-20).
#   Kasrand rechts (21,28) en (22,29) K (model: diagonale kaslijn (20,26)->(23,31)); (17,28) b -> K, (21,31) blijft K.
grid('1 oog_links',16,28,[
#  6789012
 "kkrrrk_",   # 28
 "kryKyrk",   # 29
 "kryKyrk",   # 30
 "_krrrkk",   # 31
 ],KEY)

# ===== 3. LINKERKRUIS: silhouet blijft (r4 = model-dekking). Tinten als twee gekruiste latten (model: lat B lang van linksonder
#   naar rechtsboven vóór, lat A met korte uiteinden linksboven en rechtsonder erachter): lat B lichte bovenrand (l), lijf m,
#   onderrand d als diagonaal (6,24)-(7,23) (model: (7,23) 102, (6,24) 102); uiteinde linksonder m (geen losse d); lat A linksboven:
#   kopvlak d (x4 r19-20, model 92-107), bovenvlak l, V-inkeping tussen de bovenste uiteinden (6-7,19) K, schaduw onder de lat (5,21) d (model 95); rechtsonder: onderrand d r24.
grid('3 kruis_links',0,17,[
#  0123456789
 "_________k",   # 17
 "____kk__kl",   # 18
 "___kdlkkll",   # 19
 "___kdllllm",   # 20
 "____kdlmmm",   # 21
 "____klmmmm",   # 22
 "___kllmdmm",   # 23
 ".kkllmdkdd",   # 24
 ".kmmmkkkkk",   # 25
 ],KEY)

# ===== 4. SHUPPET-OGEN: model (mgrid 4x): per oog donkere rand, lichtblauwe iris, donkere spleet. Nabije oog: iris aan beide
#   kanten (L-Shuppet x10 c, x11 n, x12 c; spleet model x11,75; R-Shuppet x53 c, x54 n, x55 c al goed). Verre oog: rand rondom
#   (rechterrand nieuw: L x7, R x50), binnen 2 px: spleet links (model L 5,3-5,8 in iris 4,6-6,9; R 48,5-48,8 in 47,9-49,4)
#   -> n c, zodat beide ogen dezelfde kant op kijken (was c n + n c c = loensend).
grid('4 shuppet_ogen_L',4,44,[
#  4567890123
 "_kk_______",   # 44
 "knck_kcnck",   # 45
 "knck_kcnck",   # 46
 ],KEY)
grid('4 shuppet_ogen_R',47,50,[
#  7890123456
 "_kk_______",   # 50
 "knck_kcnck",   # 51
 "knck_kcnck",   # 52
 ],KEY)

# ===== 5. DRADEN: 1 px, één lijn per draad, monotone (Bresenham-achtige) lijn volgens de modelsporen (spoor.py: x-midden per
#   rij). Waar twee modeldraden < 2 px uit elkaar liggen, gekozen pixel zodat er steeds 1 px lucht tussen zit.
def wis(name,x0,y0,x1,y1):
    put(name,[((i,j),0) for j in range(y0,y1+1) for i in range(x0,x1+1) if g[j,i]==NAV])
def draad(name,segs):
    pts=[]
    for x,y0,y1 in segs:
        for y in range(y0,y1+1):
            if g[y,x]==0: pts.append(((x,y),NAV))
    put(name,pts)
# rechts: R3 (model 58,2 -> 56,7; eindigt r40), R4 (59,6 -> 57,5, naar Shuppetkop r48), R5 (61,4 -> 58,4, tot r55)
wis('5 draden_rechts',56,25,61,55)
draad('5 draden_rechts',[(57,25,37),(56,38,40), (59,26,38),(58,39,43),(57,44,48), (61,28,38),(60,39,43),(59,44,50),(58,51,55)])
# links: A (model 2,6 -> 4,9: x2 r27-29, x3 r30-36, x4 r37-42, dan Shuppetkop (5,43)); B (5,5 -> 6,2: x5 r26-30, x6 r31-32 -> bel)
wis('5 draden_links',2,27,5,42); wis('5 draden_links',5,26,6,32)
draad('5 draden_links',[(2,27,29),(3,30,36),(4,37,42),(5,26,30),(6,31,32)])

# ===== 6. BELLETJES: ronde bel, glans linksboven (w), l, m (3 tinten) + omlijning; donkere spleet als in het model: liggende
#   balk + staander naar de onderrand (links: balk r35 x7-8 (model y35,5-36,3, x6,8-9,3), staander x8 r36-37; rechts: balk r20
#   x51-52 (model y19,8-20,4), staander x52 r21). Linkerbel 5 breed zoals het model (x5,3-9,8; r4 was 6 breed), rechts 6 breed
#   (model 49,8-54,3).
grid('6 bel_links',5,33,[
#  5678901
 ".kkk.._",   # 33
 "kwllk._",   # 34
 "klKKk._",   # 35
 "klmKk._",   # 36
 "kmmKk._",   # 37
 ".kkk.__",   # 38
 ],KEY)
grid('6 bel_rechts',49,17,[
#  901234
 "_kkkk.",   # 17
 "kwwllk",   # 18
 "kwllmk",   # 19
 "klKKmk",   # 20
 "kmmKmk",   # 21
 ],KEY)

# ===== 7. GLANS RODE MUTS: de band lichtste tint (e) langs de buitenlijn wordt r; glans als vlek linksboven óp het volume,
#   1-2 px van de rand (model: lichtste rood 212-215 rond (34-37,7-8)).
put('7 glans_muts',[((i,j),RM) for j in range(4,16) for i in range(26,48) if g[j,i]==RL])
grid('7 glans_muts',33,7,[
#  3456
 "____",   # 7
 "_eee",   # 8
 "eee_",   # 9
 "ee__",   # 10
 ],KEY)

# ===== 8. SCHADUWGRENS ROOD: eerste schaduwpixel (R) per rij volgens het model (kleur.py: lichtrood 202-215, schaduw 172-176):
#   r9 x42 (naast de steek), r10-11 x41, r12 x40, r13-14 x39, r15-16 x38, r17-19 x37, r20-21 x38, r22 x39, r23 x40
#   -> vloeiende boog '(' (model r14-21: x37 199-204 = randje, x38 172-176; kleinste x midden, kleur mag naar Gen 3); rommel (36-37,22) R en (38,22) r weg.
GRENS={9:42,10:41,11:41,12:40,13:39,14:39,15:38,16:38,17:37,18:37,19:37,20:38,21:38,22:39,23:40}
pts=[]
for j,x0 in GRENS.items():
    for i in range(33,46):
        if g[j,i] in (RM,RD):
            pts.append(((i,j),RD if i>=x0 else RM))
put('8 schaduwgrens',pts)

# ===== 12. STEEKNAAD: model: donkerrode naad (36,6)->(38,7)->(39,8)->(40,10)->(41,11), daarna in de schaduw; één kruissteek
#   (X) op (39,8) (model: kruisje rond (39,5-40, 8)). Het stuk (40,10)-(41,13) valt op 64 px samen met de schaduwgrens. Naad in R (donker rood) op lichtrood.
put('12 naad',[((p),RM) for p in [(39,7),(38,8)]])   # oude stukjes naad r4 ((37-39,7),(38-39,8)) die buiten de nieuwe naad vallen
put('12 naad',[((p),RD) for p in [(36,6),(37,7),(38,7),(39,8),(40,7),(38,9),(40,9)]])   # naad + X-steek rond (39,8)


# ===== 10. SPLEET HOOFD/RECHTERARM (45, 22-28): model: zwarte rechteromlijning van het hoofd op x44,5-45 van r21 tot r32, de arm
#   (erachter) sluit erop aan (witte spleet sluit op r29). Gedeelde omlijning: K op x45 r22-32 (r29-32 was arm-selout d),
#   hoofdrand (44,22-23) k -> R zodat de lijn van (44,21) diagonaal naar x45 loopt (geen dubbele zwarte rand).
put('10 spleet_arm',[((44,22),RD),((44,23),RD)]+[((45,y),K) for y in range(22,33)])

# ===== 11. LAP LINKSONDER: losse K (28,48) -> d (lapvlak), inham (28,49) in de buitenlijn dicht (K).
put('11 lap',[((28,48),GD),((28,49),K)])
np.save('cur.npy',g)
from view import png; png(g,'banette_evo.png')
print(LOG)
