# Shuppetto r7: verder op r6 (r6.npy = ../r6/cur.npy). Registratie: spritepixel (i,j) = modelblok x 24+(i-1)*S,
# y 1+(j-4)*S, S = 968/62. Per reparatiepunt van keuring_r6 een zone; LOG telt gewijzigde pixels per zone.
# Elke reparatie = overgenomen uit het model (mgrid/mch/mpx per spritepixel); kleur/schaduw naar Gen 3.
# python3 build.py -> cur.npy, banette_evo.png; python3 vel.py cur.npy vel.png; python3 controle.py cur.npy; python3 diff.py
import sys,numpy as np
g=np.load('r6.npy').copy()
LOG={}
def put(name,pts):
    n=0
    for (x,y),v in pts:
        if not(0<=x<64 and 0<=y<64): continue
        if g[y,x]!=v: n+=1
        g[y,x]=v
    LOG[name]=LOG.get(name,0)+n
def grid(name,x0,y0,rows):
    pts=[]
    for dy,row in enumerate(rows):
        for dx,ch in enumerate(row):
            if ch in ' _': continue
            pts.append(((x0+dx,y0+dy),KEY[ch]))
    put(name,pts)
K=1; GL,GM,GD=2,3,4; CYAAN,RM,RD,MOND,GEEL=5,6,7,8,9; BL,BM,BD,WIT,NAV,RL=10,11,12,13,14,15
KEY={'k':K,'l':GL,'m':GM,'d':GD,'c':CYAAN,'r':RM,'R':RD,'b':MOND,'y':GEEL,'L':BL,'M':BM,'B':BD,'w':WIT,'n':NAV,'e':RL,'.':0}
V=sys.argv[1] if len(sys.argv)>1 else 'A'
O='e'   # irisring: lichtrood/oranjerood (anders dan het hoedrood), model ~ (170,86,78)

# ===== 1a. OOG RODE KANT (model: amandel/strik van linksonder (26,31) schuin omhoog naar de buitenhoek (36,22);
#   bovenrand dipt boven de iris (32-33,25); bruine kas in twee lobben (linksonder 27-30,28-30; rechtsboven 34-35,24-26);
#   irisring rond het geel; geel-spleet-geel (31,32,33) behouden, iris als ovaal).
grid('1a oog_rood',25,22,[
#  5678901234567
  "rrrrrrrrrrrkr",   # 22  buitenpunt (36,22)
  "rrrrrrrrrrkkr",   # 23
  "rrrrrkkrrkbkr",   # 24  bovenrand links (30-31), dip, schuin omhoog (34,24)-(35,23)
  "rrrrrkkkkbbkr",   # 25  dip boven de iris (32-33)
  "rrrrrk"+O+"y"+O+"bbkr",   # 26
  "rrrrk"+O+"yky"+O+"krr",   # 27
  "rrrkb"+O+"yky"+O+"krr",   # 28
  "rrkbbb"+O+"y"+O+"krrr",   # 29
  "rkbkkkkkkrrrr",   # 30  onderrand
  "rkkrrrrrrrrrr",   # 31  punt linksonder
  ])
# ===== 1b. OOG GRIJZE KANT (model: driehoekige kas, punten linksboven (16,26) en rechtsboven (19-20,26), dip (17-18,27),
#   rechterzijde schuin naar de spitse onderkant (21-22,31); donkere kas; rode iris met geel-spleet-geel).
I2='r' if V=='A' else O
grid('1b oog_grijs',15,25,[
#  567890123
  "m_m_mmm__",   # 25
  "mkmmkkm__",   # 26
  "mkkbbkm__",   # 27
  "mkb"+I2+I2+"bk__",   # 28
  "mk"+I2+"yky"+I2+"k_",   # 29
  "mk"+I2+"yky"+I2+"k_",   # 30
  "mmk"+I2+I2+I2+"kk_",   # 31
  "__mkkkkd_",   # 32
  ])

# ===== 2. BELLEN: model = bollen met glans linksboven en een zwarte liggende sleuf met staartje laag in het midden.
#   Rand k met lichtere selout (d) op de hoek linksboven; binnen bolschaduw (glans l, lijf m, sikkel d rechtsonder).
grid('2 bel_links',5,33,[
#  567890
 ".kkkk.",   # 33
 "kmllmk",   # 34  hoekpixels binnen in m/d: ronde omtrek
 "kllllk",   # 35
 "klkkmk",   # 36  sleuf (7-8)
 "kdmkdk",   # 37  staartje (8)
 ".kkkk.",   # 38
 ])
grid('13 bel_rechts',49,17,[
#  901234
 ".kkkk.",   # 17
 "kmllmk",   # 18
 "kllllk",   # 19
 "klkkmk",   # 20  sleuf (51-52)
 "kdmkdk",   # 21  staartje (52)
 ])

# ===== 3. GRIJZE LAP ONDER DE MOND (model rij 46-48: zwarte naad, lap met twee tongen die schuin naar linksonder wijzen,
#   scheur (29,47); tippen (25,48) en (30,48)); kaaklijn linksonder als gelijkmatige diagonaal i.p.v. plankje op rij 45.
put('3 lap',[((23,44),K),((23,45),0),((26,45),GD),((23,43),GD)])
grid('3 lap',24,46,[
#  456789012
 "__kkkkkkk",   # 46
 ".kdddkddk",   # 47
 "kddkkkdkk",   # 48
 ".kkkkkkkk",   # 49
 ])

# ===== 4. KRUISSTEKEN OP DE RODE HOED: model naad (36,6)->(42,12) met kruisjes rond (37,7), (39,9), (41,11); de grond rond de
#   bovenste steken is in het model middenrood (geen donkere band) -> RM, zodat de steken (RD) lezen; in de donkere band k.
pts=[]
for y in range(5,10):
    for x in range(38 if y<7 else 39,44):
        if g[y,x]==RD and not (y==5 and x>=43): pts.append(((x,y),RM))
put('4 steken',pts)
put('4 steken',[((44,8),RM),((45,8),RM),((47,9),RM),((48,10),RM)])   # krulrand 2 px breed: (48,9) niet meer los (punt 8)
SEAM=[(36,6),(37,7),(38,8),(39,9),(40,10),(41,11),(42,12)]
TICK=[(38,6),(36,8),(40,8),(38,10),(42,10),(40,12)]
put('4 steken',[(p,(RD if g[p[1],p[0]] in (RM,RL) else K)) for p in SEAM+TICK])
put('4 steken',[((40,12),K)])

# ===== 5. SCHADUW RECHTERRAND ROOD LIJF: sikkel smal boven (1 px, r13-18), 2 px (r19-23), 3 px naast de mondhoek (r24-32),
#   2 px waar de rand terugwijkt (r33-39), breed rechtsonder (r40-44, ongewijzigd).
XS={13:43,14:42,15:42,16:42,17:42,18:42,19:41,20:41,21:42,22:43,23:43}
pts=[]
for y,xs in XS.items():
    for x in range(38,46):
        if g[y,x] in (RM,RD): pts.append(((x,y),RD if x>=xs else RM))
put('5 rand',pts)

# ===== 6. LINKERKRUIS: inkepingen tussen de armen dieper (boven (6-7,18-20), links (3-4,22)), donkere onderzijde/eindvlakjes
#   van de latten (model: eindvlak linksboven (4,19-20), linksonder (2,25), onderkant arm rechtsboven (8-9,20)).
grid('6 kruis',1,17,[
#  1234567890
 "_______kkk",   # 17
 "___kk.kllk",   # 18
 "__kdlkkllk",   # 19
 "__kdllkddk",   # 20
 "___kdllmdk",   # 21
 "__..kllmdk",   # 22
 "__kkllmmdk",   # 23
 "kkllmmkddk",   # 24
 "kdmmkkkkkd",   # 25
 ])

# ===== 7. MOND: tandpunten scherper (model): grijze boventand (21-25,35)->(24,38); rode boventand links tot punt (30,38);
#   rode boventand rechts tot punt (37,34); rode ondertand smal naar de punt (35,37).
grid('7 mond',20,35,[
#  01234567890123456789
 "kmmmmk____________",   # 35  (21,35) grijs
 "_kmmmk____________",   # 36
 "__kmmk____________",   # 37
 "___kmk____krk_____",   # 38  punt (24,38); rode tand (30,38)
 "____k_____k_______",   # 39
 ])
put('7 mond',[((30,37),RM),((31,37),K)])
grid('7 mond',33,32,[
#  345678
 "krrrrk",   # 32
 "bkrrrk",   # 33  (34,33) k
 "bbkkrk",   # 34  punt (37,34)
 "bbbbkb",   # 35
 ])
put('7 mond',[((37,38),K)])

# ===== 8. LOSSE TINTPIXELS: samenvoegen met het omliggende vlak / de omlijning.
put('8 los',[((15,19),GM),((16,19),GM),((46,22),K),((46,31),K),((48,17),K),((48,18),K),((33,8),RL)])

np.save('cur.npy',g)
from view import png; png(g,'banette_evo.png')
for k,v in LOG.items(): print('%-24s %3d'%(k,v))
