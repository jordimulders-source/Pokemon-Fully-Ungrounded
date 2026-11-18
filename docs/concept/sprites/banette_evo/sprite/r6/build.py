# Shuppetto r6: verder op r5 (r5.npy = ../r5/cur.npy). Registratie: spritepixel (i,j) = modelblok x 24+(i-1)*S,
# y 1+(j-4)*S, S = 968/62. Per reparatiepunt van keuring_r5 een zone; LOG telt gewijzigde pixels per zone.
# python3 build.py [oogvariant] -> cur.npy, banette_evo.png; python3 vel.py; python3 controle.py cur.npy; python3 diff.py
import sys,numpy as np
g=np.load('r5.npy').copy()
LOG={}
def put(name,pts):
    n=0
    for (x,y),v in pts:
        if not(0<=x<64 and 0<=y<64): continue
        if g[y,x]!=v: n+=1
        g[y,x]=v
    LOG[name]=LOG.get(name,0)+n
def grid(name,x0,y0,rows,key=None):
    key=key or KEY; pts=[]
    for dy,row in enumerate(rows):
        for dx,ch in enumerate(row):
            if ch in ' _': continue
            pts.append(((x0+dx,y0+dy),key[ch]))
    put(name,pts)
K=1; GL,GM,GD=2,3,4; CYAAN,RM,RD,MOND,GEEL=5,6,7,8,9; BL,BM,BD,WIT,NAV,RL=10,11,12,13,14,15
KEY={'k':K,'l':GL,'m':GM,'d':GD,'c':CYAAN,'r':RM,'R':RD,'b':MOND,'y':GEEL,'L':BL,'M':BM,'B':BD,'w':WIT,'n':NAV,'e':RL,'.':0}


# ===== 2. LINKERBEL: model: rand x5,0-10,1 y33,2-38,3 (6x6), glans linksboven, gat midden (7-8, 35-36); de spleet naar de
#   onderrand (model: steel x8 tot y37,5) valt weg: op 64 px plakt hij gat en onderrand aan elkaar (keuring r5: 'klontje'). Rand K, binnen w/l/m (3 tinten), gat K los van de zijrand (x6 en x9 grijs).
grid('2 bel_links',5,33,[
#  567890
 ".kkkk.",   # 33
 "kwlllk",   # 34
 "klkkmk",   # 35
 "klkkmk",   # 36
 "kmmmmk",   # 37
 ".kkkk.",   # 38
 ])
# ===== 13. RECHTERBEL: zelfde opbouw (binnen x50-53 y18-21, rand blijft r5); gat (51-52, 19-20), zonder spleet (los van de onderrand).
grid('13 bel_rechts',50,18,[
#  0123
 "wlll",   # 18
 "lkkm",   # 19
 "lkkm",   # 20
 "mmmm",   # 21
 ])

# ===== 3. BUITENLIJN LINKSONDER GEZICHT/KIN: x13 r33-36 was d (tussen k erboven en k eronder) -> K; gat (16,39) dicht met K
#   (model: zwart op (16,39)); de 1 px tandstrook d (16,37-38),(17,39),(18,40) blijft tussen buitenlijn en mondrand.
put('3 kin',[((13,y),K) for y in range(33,37)]+[((16,39),K)])

# ===== 5. STEEKLIJN MUTS: model donkere naad (36,6)-(38,7)-(39,8)-(39,9)-(40,10)-(41,11)-(41/42,12) -> één doorlopende
#   1 px diagonaal in RD; losse steekpixels van r5 ((37,7),(38,9),(40,7),(40,9)) eruit (RM).
SEAM=[(37,6),(38,7),(39,8),(39,9),(40,10),(41,11),(42,12)]
put('5 steken',[((p),RM) for p in [(36,6),(37,7),(38,9),(40,7),(40,9),(38,8)] if p not in SEAM])
put('5 steken',[((p),RD) for p in SEAM])

# ===== 6+8. SCHADUW ROOD: sikkel die de vorm volgt i.p.v. een band van 5-7 px (kleur mag naar Gen 3 afwijken; het model
#   heeft een rechte grens op x38). Krul (rechts van de steeklijn, r5-12): licht (r) op de bovenkant, 2 px diep bij de voet
#   (x<=46), 1 px naar de punt; rest donker (onderkant boven het gat). Lijf: donker vanaf xs(y) tot de buitenlijn:
#   2 px boven (r13-17), 3 px (r18-35), lob onder de mond diagonaal, onderkant breed. Losse lichtrode kolom (41,36-40) -> R.
RED=(RM,RD)
def top(x):
    for y in range(64):
        if g[y,x]: return y
seam_x={y:x for x,y in SEAM}
pts=[]
for x in range(40,52):
    t=top(x); Lx=2 if x<=46 else 1
    for y in range(t+1,13):
        if g[y,x] in RED and x>seam_x.get(y,99 if y<6 else 0):
            pts.append(((x,y),RM if y-t<=Lx else RD))
put('6 krul',pts)
put('6 krul',[((49,12),RM),((50,12),RM)])   # (49,11) volgt na de lijfstap; hoek waar de krul omlaag draait: lichte binnenkant sluit aan op de punt (49-50,13)
XS={12:43,13:42,14:41,15:41,16:41,17:41,18:40,19:40,20:40,21:41,22:42,23:42}
for y in range(24,36): XS[y]=42
for y in range(36,40): XS[y]=41
XS.update({40:37,41:35,42:34,43:34,44:0,45:0})
pts=[]
for y,xs in XS.items():
    for x in range(30 if y>=40 else 36,46):
        if g[y,x] in RED:
            pts.append(((x,y),RD if x>=xs else RM))
put('6 lijf',pts)
# lob onder de mond (r38-40, x34-39): schaduw rechtsonder diagonaal
put('6 lijf',[((38,39),RD),((39,39),RD)])
put('8 kolom41',[((41,y),RD) for y in range(36,41)])
put('5 steken',[((p),RD) for p in SEAM])   # steeklijn na de lijfschaduw, zodat (42,12) donker blijft
put('6 krul',[((49,11),RM)])

# ===== 7. GRIJZE FLAP RECHTS: licht links/boven, donker naar de schaduwkant, grens diagonaal met de flap mee (geen d|l|d).
grid('7 flap',46,19,[
#  6789
 "_dl_",   # 19
 "_dl_",   # 20
 "_dl_",   # 21
 "dll_",   # 22  (46,22) grenst aan lucht -> selout d
 "llm_",   # 23
 "llm_",   # 24
 "lmm_",   # 25
 "lmm_",   # 26
 "lmd_",   # 27
 "mmd_",   # 28
 "mdd_",   # 29
 "md__",   # 30
 "d___",   # 31
 ])

# ===== 9. MIDDEN LINKERKRUIS: losse d (7,23) en (6,24) -> m; onderschaduw als één groep d rechtsonder (8-9,24)+(9,23).
put('9 kruis',[((7,23),GM),((6,24),GM),((9,23),GD)])


# ===== 10. GEZICHT GRIJS (x15-23, r17-36): Gen 3-volume op de vlakke middentint: licht (l) als ovale vlek linksboven onder de
#   hoed, schaduwsikkel (d) rechts langs de naad en onder langs de mondrand, breder naar rechtsonder. Alleen m-pixels.
LICHT={19:(17,19),20:(17,20),21:(16,19),22:(16,18),23:(16,17)}   # ovale vlek, los van de vouwlijn x14
pts=[((x,y),GL) for y,(a,b) in LICHT.items() for x in range(a,b+1) if g[y,x]==GM]
DONKER={25:[22],26:[22],27:[22],28:[22],29:[22],30:[22],31:[22],32:[21,22],33:[20,21,22]}   # sikkel langs de naad, breder naar de mond
pts+=[((x,y),GD) for y,xs in DONKER.items() for x in xs if g[y,x]==GM]
put('10 gezicht',pts)

# ===== 11. OVERGANG LIJF-DRUPPEL: model donker op (34,45) 78 en (35,45) 112 -> K.
put('11 druppel',[((33,45),K),((34,45),K),((35,45),K)])   # (33,45) (model 156) erbij: lijn sluit aan op de buitenlijn (32,46)

# ===== 12. ARM LINKER-SHUPPET: (8,53) navy binnen zwart (7,53) -> L; dambordje (8-11,54) -> M M M B; (8-9,55) M.
put('12 arm',[((8,53),BL),((8,54),BM),((9,54),BM),((10,54),BM),((11,54),BD)])

# ===== 1. SHUPPET-OGEN. Model (mgrid): L-Shuppet verre oog x4,2-7,4 y44,9-47,8 (raakt de kopomlijning x4), nabije oog
#   x9,8-13,0 y44,4-47,4; R-Shuppet verre oog x47,5-50,3 y50-52,8, nabije x52-56,2 y50-53,2. Opbouw als het oog van de echte
#   Shuppet (anim_front): donker bovenooglid, lichte iris met glans linksonder, donker deel rechtsboven tegen de rand,
#   rand rondom maar met afgeronde hoeken; de onderrand in de donkere huidtint (B) i.p.v. zwart, zodat de twee ogen
#   geen doorlopend zwart 'brilmontuur' vormen; huid (M) tussen de ogen.
V=sys.argv[1] if len(sys.argv)>1 else 'A'
#   Beide ogen 4 px breed (rand incl.), 2x2 binnen, ronde hoeken (hoekpixels huid), 2 px huid ertussen (model: gat 2,4 px).
#   Binnen als de echte Shuppet: donker (n) rechtsboven tegen de rand, lichtst (w) linksonder. Variant B: glans linksboven,
#   pupil rechtsonder.
IN={'A':('cn','wc'),'B':('wc','cn')}[V]
a,b=IN
grid('1 shuppet_ogen_L',4,44,[
#  45678901234
 "_kkLMMMkkMk",          # 44  verre oog: bovenlid = kopomlijning (5-6,44); nabije oog: bovenlid (11-12,44)
 "k"+a+"kMMk"+a+"kk",     # 45  (14,45-46) kopomlijning B -> K (punt 4)
 "k"+b+"kMMk"+b+"kk",     # 46
 "kkkMMMMkkBk",          # 47
 ])
grid('1 shuppet_ogen_R',47,50,[
#  789012345678
 "_kkLLMMkkMB_",         # 50  verre oog: bovenlid = kopomlijning (48-49,50); nabije oog (54-55,50)
 "k"+a+"kMMk"+a+"kB_",    # 51
 "k"+b+"kMMk"+b+"kB_",    # 52
 "_kkMMBMkkk__",         # 53
 ])
np.save('cur.npy',g)
from view import png; png(g,'banette_evo.png')
for k,v in LOG.items(): print('%-24s %3d'%(k,v))
