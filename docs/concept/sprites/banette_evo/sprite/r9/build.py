# Shuppetto r9: kleine reparatieronde op r8 (r8.npy = ../r8/cur.npy), punten = keuring_r8. Registratie: spritepixel (i,j)
# = modelblok x 24+(i-1)*S, y 1+(j-4)*S, S = 968/62. Elke reparatie overgenomen uit het model (mch/mpx); kleur naar Gen 3.
# python3 build.py -> cur.npy, banette_evo.png; python3 vel.py cur.npy vel.png; python3 controle.py cur.npy; python3 diff.py
import numpy as np
g=np.load('r8.npy').copy(); LOG={}
def put(name,pts):
    n=0
    for (x,y),v in pts:
        if g[y,x]!=v: n+=1
        g[y,x]=v
    LOG[name]=LOG.get(name,0)+n
def grid(name,x0,y0,rows):
    put(name,[((x0+dx,y0+dy),KEY[ch]) for dy,row in enumerate(rows) for dx,ch in enumerate(row) if ch not in ' _'])
K=1; GL,GM,GD=2,3,4; CYAAN,RM,RD,MOND,GEEL=5,6,7,8,9; BL,BM,BD,WIT,NAV,RL=10,11,12,13,14,15
KEY={'k':K,'l':GL,'m':GM,'d':GD,'c':CYAAN,'r':RM,'R':RD,'b':MOND,'y':GEEL,'L':BL,'M':BM,'B':BD,'w':WIT,'n':NAV,'e':RL,'.':0}

# 1. bellen: model links donker op (7-8,35) en (7-8,36) (49/42), rij 37 weer grijs (103/86); rechts idem een rij hoger.
#    Gat + spleet een rij hoger en gecentreerd = 2x2 donker in het midden van de bel (zoals het model op deze schaal);
#    oude spleetpixel (8,37)/(52,21) -> beltint d. Glans linksboven (rij 1 + kolom 1) en schaduw rechts blijven.
BEL=["llld","lkkd","lkkd","dddd"]   # (9,34)/(53,18) d: anders los m-pixeltje; schaduwkolom rechts doorlopend
grid('1 bel links',6,34,BEL)
grid('1 bel rechts',50,18,BEL)

# 2. open rand kapflap: model rij 29 x11-12 donker (b), rij 30 wit -> flap houdt op rij 29 op; (12,29) zwart.
put('2 kapflap',[((12,29),K)])

# 3. steken rode kap: model naad (36,6)rand -> (38,7) -> (39,8) -> (39/40,9) -> (40,10), onderaan kruisje rond (41,11-12).
#    Dambord weg (terug naar middenrood), doorlopende 1 px naad in R, 2 dwarssteekjes haaks op de naad, kruisje R i.p.v. zwart.
put('3 steken',[(p,RM) for p in [(37,7),(39,7),(38,8),(37,9),(39,9)]])
put('3 steken',[(p,RD) for p in [(37,6),(38,7),(39,8),(40,9),(40,10)]])           # naadlijn vanaf de rand (36-37,5), model x37->40
put('3 steken',[(p,RD) for p in [(39,6),(37,8),(41,8),(39,10)]])                  # dwarssteekjes haaks bij (38,7) en (40,9) (model: takjes rij 8 links, rij 9 rechts)
put('3 steken',[(p,RD) for p in [(42,10),(41,11),(40,12),(42,12)]])               # kruisje (arm (40,10) = naad) R i.p.v. zwart

# 4. Shuppet-ogen: 3 px brede amandel (iris 3x2, hoeken weg, geen zwart hoekje bovenaan), lichtblauw, pupil midden-onder.
#    Model popL rechteroog: leden (11-12,44) en (10-12,47), iris rij 46 x10-12, eind (13,45-46); popR rechteroog tot ~x57.
#    Ooglijn in marine (model: leischaduw ~70,85,110, geen zwart kader); waar de ooghoek op de buitenlijn valt blijft die zwart.
#    Pupil zwart (donkerste punt), zodat hij van de ooglijn loskomt.
RANDK={(4,45),(4,46),(14,45),(14,46),(47,51),(47,52),(58,51),(58,52)}
def oog(a,y,pup):   # iris kolommen a..a+2, rijen y,y+1
    lijn=[(a+i,y-1) for i in range(3)]+[(a+i,y+2) for i in range(3)]+[(a-1,y),(a-1,y+1),(a+3,y),(a+3,y+1)]
    pts=[(p,K if p in RANDK else NAV) for p in lijn]
    pts+=[((a+i,y+j),CYAAN) for i in range(3) for j in range(2)]
    pts+=[((a+1,y+1),K)] if pup else []
    put('4 ogen',pts)
oog(5,45,1); oog(11,45,1)            # popL: midden x9 blijft lijf
oog(48,51,1); oog(55,51,1)           # popR: midden x52-53 lijf
put('4 ogen',[((56,49),BM),((54,50),BM),((54,53),BM),((53,51),BM),((53,52),BM),((9,45),BM),((9,46),BM)])

# 5. rechter mondhoek: model kolom 42 rij 27-31 = donkerrood (142-148,58,59), zwart alleen x40-41 -> (42,27-31) R; lijn 1 px.
put('5 mondhoek',[((42,y),RD) for y in range(27,32)])

# 6. kruis bovenarm rechts: (55,20-22) lichte kruistint, zwarte bellijn (54) is de grens.
put('6 kruis',[((55,y),GL) for y in (19,20,21,22)])   # (55,19) mee: anders los d-pixeltje tussen twee zwarte (model m)

np.save('cur.npy',g)
from view import png; png(g,'banette_evo.png')
for k,v in LOG.items(): print('%-16s %3d'%(k,v))
