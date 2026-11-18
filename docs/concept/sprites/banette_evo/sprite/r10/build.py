# Shuppetto r10: reparatieronde op r9 (r9.npy = ../r9/cur.npy), punten = opdracht r10. Registratie: spritepixel (i,j)
# = modelblok x 24+(i-1)*S, y 1+(j-4)*S, S = 968/62. Elke reparatie overgenomen uit het model (mask/mch/mpx); kleur naar Gen 3.
# python3 build.py -> cur.npy, banette_evo.png; python3 vel.py cur.npy vel.png; python3 controle.py cur.npy; python3 diff.py
import numpy as np; from scipy import ndimage as nd
from mask import frac
g=np.load('r9.npy').copy(); LOG={}
def put(name,pts):
    n=0
    for (x,y),v in pts:
        if g[y,x]!=v: n+=1
        g[y,x]=v
    LOG[name]=LOG.get(name,0)+n
def grid(name,x0,y0,rows):
    put(name,[((x0+dx,y0+dy),KEY[ch]) for dy,row in enumerate(rows) for dx,ch in enumerate(row) if ch not in ' _'])
K=1; GL,GM,GD=2,3,4; CYAAN,RM,RD,MOND,GEEL=5,6,7,8,9; BL,BM,BD,DRAAD,NAV,RL=10,11,12,13,14,15
KEY={'o':K,'k':K,'l':GL,'m':GM,'d':GD,'c':CYAAN,'r':RM,'R':RD,'b':MOND,'y':GEEL,'L':BL,'M':BM,'B':BD,'t':DRAAD,'n':NAV,'e':RL,'.':0}

# 1. ZIGZAGGRIJNS als één band. Bandmasker = spritepixels waarvan >=50% van het modelblok helderheid < 75 (mask.py),
#    component C in x15-41 y32-42; overgenomen zoals gemeten (BAND hieronder = mask.py 15 32 42 43 .5, alleen de
#    hoofdbuitenlijn en de oog-onderlijn eruit). Vulling MOND (donkerbruin); zwart alleen op de bandrand die aan huid grenst
#    (model: overal een zwarte lijn tussen band en tanden); tegen de hoofdbuitenlijn direct vulling (één lijn).
#    Huid die vrijkomt: middentint van de kant (modelklasse grijs -> m, rood -> r), schaduwkant volgt de buren uit r9.
BAND=[  # x15..41
"..................#....####",  # 32
".................####..###.",  # 33
".#...............#########.",  # 34
".##..##...##....##########.",  # 35
".##.###...###...#########..",  # 36
"..######.#####.#####.####..",  # 37
"..#################....##..",  # 38
"...################........",  # 39
"....##.######.#####........",  # 40
"........#####..###.........",  # 41
".........##.....##.........",  # 42
]
B=np.zeros(g.shape,bool)
for dy,row in enumerate(BAND):
    for dx,ch in enumerate(row):
        if ch=='#': B[32+dy,15+dx]=True
# 7. kinrand: de 1 px grijze strook tussen hoofdbuitenlijn en bandrand ((16,37-38),(17,39),(18,40)) hoort bij de band,
#    zodat de band direct op de ene buitenlijn aansluit (geen dubbele zwarte lijn met trapjes).
for p in [(16,37),(16,38),(17,39),(18,40)]: B[p[1],p[0]]=True
# linkermondhoek: zwarte streep omhoog naar (15,32) (model: maskercomponent E, (15,32-33) 0.3-0.4 zwart, diagonaal aan (16,34)).
for p in [(15,32),(15,33)]: B[p[1],p[0]]=True
from PIL import Image
_A=np.asarray(Image.open('../../model/model.png').convert('RGB')).astype(float); S=968/62
def modelrood(i,j):
    xa,ya=24+(i-1)*S,1+(j-4)*S; b=_A[int(round(ya)):int(round(ya+S)),int(round(xa)):int(round(xa+S))].reshape(-1,3)
    b=b[b.sum(1)/3>75]
    if len(b)==0: return None
    return ((b[:,0]-b[:,1])>60).mean()>.5
r9=g.copy(); fig=r9>0
P=np.pad(fig,1); nearT=np.zeros_like(fig)
for dy in (-1,0,1):
    for dx in (-1,0,1): nearT|=~P[1+dy:65+dy,1+dx:65+dx]
OUTL=(r9==K)&nearT
GRIJS={GL,GM,GD}; ROOD={RM,RD,RL}
def huid(i,j):
    rood=modelrood(i,j)
    if rood is None: rood=i>=25
    fam=ROOD if rood else GRIJS
    for R in (1,2,3):
        vals=[int(r9[y,x]) for y in range(j-R,j+R+1) for x in range(i-R,i+R+1) if r9[y,x] in fam and not B[y,x]]
        if vals: return max(set(vals),key=vals.count)
    return RM if rood else GM
mond=[]
for j in range(32,43):
    for i in range(15,42):
        if OUTL[j,i]: continue
        if B[j,i]:
            nb=[(i+1,j),(i-1,j),(i,j+1),(i,j-1)]
            rand=any((not B[y,x]) and (not OUTL[y,x]) and r9[y,x]!=0 for x,y in nb)
            mond.append(((i,j),K if rand else MOND))
        elif r9[j,i] in (K,MOND):
            mond.append(((i,j),huid(i,j)))
put('1 mondband',mond)
# 7. kin onder de band: model rij 41-44 x19-28 helemaal 'd' (mch.py 18 40 30 45) -> één vlak GD, geen m-strook die parallel
#    aan de buitenlijn loopt (dat gaf zwart+d+zwart = dubbele lijn). Tandpunt (21,40) blijft m (model m).
put('7 kinrand',[(p,GD) for p in [(22,42),(23,42),(24,43),(25,43),(26,43),(26,42),(27,42)]])
put('7 kinrand',[(p,GM) for p in [(19,41),(20,41),(21,41),(22,41)]])   # onderste grijze tand (punt (21,40)) als driehoekje in middentint, zoals de rode tand rechts

# 2. BELLETJES ROND: 6x6 cirkel i.p.v. doosje: hoekpixels (en de 4 diagonale) weg, rand 2-1-1-2; glans l linksboven,
#    sikkel d rechtsonder, liggend sleufje 2x1 laag in het midden (model: donkere vlek midden-onder, steeltje omlaag).
#    Achter de rechterbel loopt de kruisarm door: vrijgekomen hoeken onderaan = armkleur (model rij 21-22: d/m).
def bel(x0,y0,bg):   # x0,y0 = linkerbovenhoek van het 6x6 vak
    rows=["..kk..",
          ".klmk.",
          "kllmdk",
          "kmkkdk",
          ".kddk.",
          "..kk.."]
    pts=[]
    for dy,row in enumerate(rows):
        for dx,ch in enumerate(row):
            p=(x0+dx,y0+dy)
            pts.append((p,bg.get(p,0) if ch=='.' else KEY[ch]))
    put('2 bellen',pts)
bel(5,33,{})
bel(49,17,{(49,21):GD,(50,22):GD,(54,21):GM,(53,22):GM,(49,22):GD,(54,22):GL,(49,18):K,(54,18):K})
# rechts: (49,18)/(54,18) blijven zwart = rechterrand van het mes links (model: mesrand x49.5) en bovenrand kruisarm rechts;
# anders staan (48,17-18) en (55,18) als losse zwarte stompjes. De bel blijft rond aan de bovenkant (hoeken (50,17),(53,17) weg).

# 3. SHUPPET-KOPPEN EN -OGEN uit het model (sl/sr-rasters, mbl.py): kop rond (zijkant 3 px recht, hoek (4,44)/(14,44) weg),
#    geen 'brilletje' (geen doorlopende marine rij boven en onder de ogen). Per oog: bovenlid 1 px marine, binnenhoek marine,
#    lichtblauwe iris, één zwarte pupil; onderkant iris direct tegen de huid (model: lichte iris, lid boven/buiten donker).
#    Verre oog (aan de kopkant) 2 px breed, nabije oog 4 px (model 2 / 4 px). Buitenlijnkleur wordt in 4 gezet ('o').
SH={'o':K}
put('3 Shuppets',[((x,y),0) for x,y in [(4,44),(14,44)]])
grid('3 Shuppets',5,44,["oLLMMMMMo"])
grid('3 Shuppets',4,45,["onnMMMMnnno",
                        "ocknMMnckco",
                        "occMMMMccno"])
grid('3 Shuppets',47,50,[".onLLMMnnnMo",
                         "ocknMMnckcMo",
                         "occMMMMccnBo",
                         ".oMMMMMBBBo"])

# 4+5. SHUPPET-BUITENLIJN en TOUWTJES. Shuppet = blauwe vulling (L/M/B/iris) + marine/zwarte pixels die er 8-buur van zijn,
#    binnen de twee Shuppet-vakken; overige marine pixels = touwtjes -> eigen lichte tint DRAAD (palet 13, was ongebruikt wit).
#    Losse touwpixels die een Shuppet raken (TOUW_EXTRA) staan hieronder met de hand. Buitenlijn: één regel per rand via de
#    naar buiten wijzende normaal n (som van de richtingen naar buitenpixels): nx+ny<0 (boven/links = lichtkant) -> marine
#    selout, anders zwart. Zo wisselt de lijn alleen op de diagonaal rechtsboven/linksonder, nooit om en om.
ZONES=[(0,37,18,58),(44,42,63,63)]
TOUW_EXTRA={(58,53),(58,54),(58,55),(11,41)}
FILL=np.isin(g,[BL,BM,BD,CYAAN])
def inzone(x,y): return any(x0<=x<x1 and y0<=y<y1 for x0,y0,x1,y1 in ZONES)
SHUP=np.zeros(g.shape,bool)
for y in range(64):
    for x in range(64):
        if not inzone(x,y) or (x,y) in TOUW_EXTRA: continue
        if FILL[y,x]: SHUP[y,x]=True
        elif g[y,x] in (NAV,K) and FILL[max(0,y-1):y+2,max(0,x-1):x+2].any(): SHUP[y,x]=True
touw=[((x,y),DRAAD) for y in range(64) for x in range(64) if g[y,x]==NAV and not SHUP[y,x]]
put('5 touwtjes',touw)
lijn=[]
for y in range(64):
    for x in range(64):
        if not SHUP[y,x] or FILL[y,x]: continue
        nx=ny=0; buiten=False
        for dy in (-1,0,1):
            for dx in (-1,0,1):
                if dx==dy==0: continue
                X,Y=x+dx,y+dy
                out=not(0<=X<64 and 0<=Y<64) or not SHUP[Y,X]
                if out:
                    nx+=dx; ny+=dy
                    if dx==0 or dy==0: buiten=True
        if buiten: lijn.append(((x,y),NAV if nx+ny<0 else K))
put('4 Shuppet-buitenlijn',lijn)

# 6. TOP RODE MUTS: dambord en los glansvlekje weg (model: effen rood, geen glans) -> binnenvlak x31-43 y5-12 middenrood,
#    schaduwkant rechts donkerrood volgens het model (mch: rij 9 x>=44, rij 10 x>=42, rij 11-12 x>=42, 1 px van de naad af). Stiklijn van het
#    model ((35.5,5.8) -> (40.3,9.8)) als 1 px diagonale lijn van steekjes van 2 px met 1 px tussenruimte, in donkerrood.
TRANSP=(g==0); Pp=np.pad(TRANSP,1,constant_values=True)
ADJT=Pp[:-2,1:-1]|Pp[2:,1:-1]|Pp[1:-1,:-2]|Pp[1:-1,2:]
SCHADUW={5:99,6:99,7:99,8:99,9:44,10:42,11:42,12:42}
muts=[]
for y in range(5,13):
    for x in range(31,44):
        if g[y,x] not in (RM,RD,RL) or ADJT[y,x]: continue
        muts.append(((x,y),RD if x>=SCHADUW[y] else RM))
put('6 mutstop',muts)
put('6 mutstop',[(p,RD) for p in [(36,6),(37,7),(39,9),(40,10)]])

# 8. STIKNAAD grijs/rood: model (dwarsprofiel x21-28 per modelrij) heeft dwarssteken op y 16.6-17.4, 19.3, 22.4, 27, 33;
#    regelmatig overgenomen als 5 zwarte tikjes van 3 px dwars over de naad op rij 14, 17, 20, 23, 26 (naadpixel +-1).
#    Oude tikjes (23-25,18) en (22-24,22) terug naar huid/naadlijn. Rij 29/32 niet: daar raakt een tikje de oogrand.
put('8 naad',[((24,25),RM),((23,18),GM),((24,18),GM),((25,18),GD),((22,22),GM),((23,22),GM),((24,22),GD)])
put('8 naad',[((x,y),K) for y,xs in [(14,26),(17,26),(20,24),(23,23),(26,24)] for x in (xs-1,xs,xs+1)])   # rij 26 1 px naar rechts: los van de oogrand (19-20,26)

# 9. ROOD GEZICHT: lichtere zone linksboven (Gen 3-volume), klein ovaal (14 px) los van naad en rand, in RL.
LICHT={14:(31,32),15:(30,33),16:(30,33),17:(30,32),18:(31,31)}   # 1 px lucht naar de naadtikjes
put('9 rood licht',[((x,y),RL) for y,(a,b) in LICHT.items() for x in range(a,b+1) if g[y,x]==RM])

# 10. LINKERKRUIS: geen schuine d-strepen (4,19),(4,20),(5,21) en geen verticale d-kolom x9 rij 20-23 langs de hoedlijn;
#     licht boven (l), mid in het midden (m), donker alleen onderaan (rij 24-25). Hoedlijn x10 rij 17-24 blijft zwart; de
#     arm is nu licht/mid tegen de donkere hoedrand (x11 d), dus de grens leest.
put('10 kruis',[(p,GM) for p in [(4,19),(4,20),(5,21),(8,20),(9,20),(9,21),(9,22),(9,23)]])

np.save('cur.npy',g)
from view import png; png(g,'banette_evo.png')
for k,v in LOG.items(): print('%-24s %3d'%(k,v))
