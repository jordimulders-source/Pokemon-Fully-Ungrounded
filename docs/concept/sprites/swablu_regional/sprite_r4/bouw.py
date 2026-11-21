# Swablu (onweerswolk) r4: Jordi over r3: "nee de lijnen zijn veel te hard nu, het ligt aan dat er meer dan 2 kleurtinten moeten zijn om minder blur
# te hebben. De belijning moet juist zachter en niet zwart. Kijk desnoods naar de snavel van de echte swablu qua vorm en hoe die belijnd is".
# Studie echte Swablu (graphics/pokemon/swablu/anim_front.png, bovenste frame): kop omlijnd met donker blauwgroen (56,104,128), geen zwart;
# zwart alleen onderaan lijf/poten en de rechterkant van de kuif (schaduwzijde, buitenkant); wolk: wit/lichtlila/lila + grijze selout (128,128,144),
# geen zwart; snavel: wit vlak, onderkant lila schaduw, grijze onderlijn, bovenkant open (wit raakt de kop met een lila stip), geen ring.
# Basis = r3; silhouet bevroren (alpha-diff 0); alleen kleur/lijn/schaduw. Draaien vanuit swablu_regional/.
import sys, numpy as np
from PIL import Image
sys.path.insert(0,'gereedschap')
import gemeen as G
G.PAL=[(152,208,160),(13,17,24),
     (68,78,96),(96,108,126),(126,138,156),(164,176,192),(210,216,228),   # 2 wolk diep, 3 donker, 4 midden, 5 licht, 6 wit
     (68,90,110),(106,130,152),(150,174,194),                            # 7 vogel donker, 8 midden, 9 licht
     (200,158,40),(248,214,64),                                          # 10 oker, 11 geel
     (46,60,78),                                                         # 12 selout donker (kop, sprieten, onderwolk): vervangt het zwart
     (214,220,230),(250,251,253)]                                        # 13 snavelwit, 14 glans
G.CH='.K01234abcoySwW'
SEL=12
o=np.asarray(Image.open('sprite_r3/swablu_r3.png')).astype(int); start=o.copy()
tel={}
def zet(lijst,naam):
    v=o.copy()
    for X,Y,k in lijst:
        assert start[Y,X]!=0,(X,Y,'silhouet'); o[Y,X]=k
    tel[naam]=tel.get(naam,0)+int((v!=o).sum())
N4=((-1,0),(1,0),(0,-1),(0,1)); N8=[(dy,dx) for dy in (-1,0,1) for dx in (-1,0,1) if dy or dx]
OOG={(28,27),(29,28),(28,29),(29,29)}
SNAVEL={(x,y) for x in range(21,27) for y in range(27,33)}
SPRIET={(x,y) for x in range(24,35) for y in range(16,24)}
def materiaal(Y,X):
    tel_={'vogel':0,'bol':0,'basis':0}
    for dy,dx in N8:
        k=start[Y+dy,X+dx]
        if k in (7,8,9): tel_['vogel']+=1
        elif k in (5,6): tel_['bol']+=1
        elif k==4: tel_['bol' if any(start[Y+dy+ey,X+dx+ex] in (5,6) for ey,ex in N4) else 'basis']+=1
        elif k in (2,3): tel_['basis']+=1
    return max(tel_,key=tel_.get)
# --- 1. zwart -> gekleurde selout. Zwart blijft alleen aan de buitenkant schaduwzijde van de onderwolk/het staartje (achtergrond onder of rechts, y>=38)
#        en in het oog (zoals de echte Swablu). Kop, sprieten en onderwolk-binnenlijnen -> selout donker (46,60,78); lijnen van/tussen de lichte bollen -> wolk donker. ---
v=[]
for Y,X in zip(*np.where(start==1)):
    if (X,Y) in OOG or (X,Y) in SNAVEL: continue
    fg=start>0
    bD=not fg[Y+1,X]; bR=not fg[Y,X+1]
    if Y>=38 and (bD or bR): continue
    if (X,Y) in SPRIET: v.append((X,Y,SEL)); continue
    m='vogel' if any(start[Y+dy,X+dx] in (7,8,9) for dy,dx in N4) else materiaal(Y,X)   # lijn die de kop raakt = kopomlijning (één tint)
    v.append((X,Y,3 if m=='bol' else SEL))
zet(v,'zwart -> selout')
# --- 2. wolk-diep lijnen tussen kop en onderwolk (rij 37) en inkepingen: tegen het lijf -> selout donker blijft (2 -> 12 alleen waar het lijf raakt);
#        de diagonaal linker bol/onderwolk ((19,35)(18,35)(17,35)(16,36)(15,36)) -> wolk donker (zachter, selout van de bol) ---
zet([(x,37,SEL) for x in range(23,34) if start[37,x]==2],'onderrand kop: selout')
zet([(19,35,3),(18,35,3),(17,35,3),(16,36,3),(15,36,3)],'rand bol/onderwolk links: zachter')
# --- 3. snavel zoals de echte Swablu: geen gesloten ring. Op de plek en maat van het model: wit vlak (13) met glans (14) linksboven,
#        onderkant/onderkaak lichte schaduw (wolk licht), mondlijn en onderlijn wolk midden, rechterrand wolk donker; bovenkant open:
#        de bovenrand wordt snavelwit/licht (wit raakt de kop zoals bij Swablu), alleen de hoek linksboven houdt een donkere stip. ---
zet([(21,27,SEL),(22,27,4),(23,27,5),(24,27,5),(25,27,8),          # bovenrand open: links selout-stip, dan grijs -> licht -> kop
     (21,28,SEL),(21,29,4),(21,30,4),                               # linkerrand: zachte grijze lijn (model: donkergrijs L 103-114)
     (26,28,4),(26,29,3),(26,30,3),(25,30,4),                       # rechterrand: grijs, onderaan donkerder (schaduwzijde)
     (21,31,4),(22,31,4),(26,31,3),                                 # mondlijn grijs
     (22,32,3),(23,32,3),(24,32,3),(25,32,3)],'snavel als echte Swablu')
# --- 4. tussenstap: vlakken binnen één materiaal die twee tinten verspringen (wit naast midden, midden naast diep, licht naast donker)
#        krijgen de tussentint op de donkerste pixel van de grens, zodat het niet hard wordt (3 tinten per materiaal). Lijnen/selout niet. ---
v=[]
for Y,X in zip(*np.where(o>0)):
    k=o[Y,X]
    for groep in ((4,5,6),(2,3,4),(7,8,9)):
        if k==groep[0] and any(o[Y+dy,X+dx]==groep[2] for dy,dx in N4) and not any(o[Y+dy,X+dx] in (0,1,SEL) for dy,dx in N4):
            v.append((X,Y,groep[1])); break
zet(v,'tussenstap')
G.opslaan(o,'sprite_r4/swablu_r4.png')
G.rgb(o,(255,255,255)).resize((512,512),Image.NEAREST).save('sprite_r4/swablu_r4_8x.png')
print('stappen',tel); print('anders dan r3: %d px'%(o!=start).sum(),'| alpha-diff met r3:',int(((o>0)!=(start>0)).sum()),'| kleuren excl. transp.',len(set(o.ravel()))-1,'| zwart over:',int((o==1).sum()))
if 'toon' in sys.argv: G.toon(o,15,50,10,52)
