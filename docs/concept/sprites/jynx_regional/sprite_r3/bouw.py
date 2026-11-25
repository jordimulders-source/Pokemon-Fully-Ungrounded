# Regionale Jynx r3 = eindkeuring Dragonfly Cave op r2: alleen buitenlijn (selout/zwart naar lichtrichting) en
# binnenlijnen 1 px (dubbele lijnen uit de reductie). Niets hertekend, geen nieuwe vormen, silhouet-diff 0, gezicht 0.
# Bouwen: cd docs/concept/sprites/jynx_regional && python3 sprite_r3/bouw.py   (variant: ... bouw.py kinschaduw)
import sys, numpy as np
sys.path.insert(0,'gereedschap'); from gemeen import *
import gemeen
r2=np.asarray(Image.open('sprite_r2/jynx_regional_r2.png')).astype(int); o=r2.copy()
PAL2=list(PAL); PAL2[15]=(200,154,104); gemeen.PAL[:]=PAL2      # palet r2 (plek 15 = haar licht), ongewijzigd
K,L,S_,M_,P_,D=1,2,3,4,5,6
tel={}
def zet(n,lst,k,moet):
    for X,Y in lst:
        assert CH[o[Y,X]]==moet,(n,X,Y,CH[o[Y,X]]); o[Y,X]=k
    tel[n]=tel.get(n,0)+len(lst)

# 1. Buitenlijn: rand naar boven/links = gekleurde selout, rand naar onder/rechts = zwart (normaal uit het
#    afgevlakte silhouet, rand.py: ny < -0,8 of d > 0,35 -> selout; ny > 0,6 -> zwart).
zet('buitenlijn: bovenrand haar rechts zwart->selout',[(39,7),(40,7)],D,'K')
zet('buitenlijn: bovenkant haarpunt rechts zwart->selout',[(53,40),(54,40),(55,40),(56,40)],D,'K')
zet('buitenlijn: linkerrand haar onder vleugel zwart->selout',[(15,30)],D,'K')
zet('buitenlijn: onderrand rokpunt links selout->zwart',[(10,54),(11,54)],K,'l')
zet('buitenlijn: onderkant rokzoom boven linkervoet selout->zwart',[(19,55),(18,56)],K,'l')

# 2. Binnenlijnen 1 px: waar de reductie één modellijn over twee spritepixels verdeelde, blijft de pixel met
#    de meeste modelzwart-dekking (dekking.py) lijn; de andere wordt het vlak ernaast.
zet('binnenlijn: haarlok/kraag links (D K44 houdt, l K31 -> kraag)',[(19,27),(19,28),(19,29),(19,30)],P_,'l')
zet('binnenlijn: rokvouw bij de zoom links (1 px diagonaal)',[(22,53),(23,54)],M_,'l')
zet('binnenlijn: bovenkant linkerpoot (zoom is de lijn, poot vlak)',[(22,56),(23,56)],S_,'l')
zet('binnenlijn: vouwknik rechts x33/x34 (1 px diagonaal)',[(34,48),(33,49)],M_,'l')

if len(sys.argv)>1 and sys.argv[1]=='kinschaduw':
    # VARIANT ter keuze (voorstel Claude, niet uit het model; Gen 3-Jynx heeft een slagschaduw van het gezicht op de borst,
    # rij 26-28): gebogen sikkel in kraag-midden onder de kinboog, 1 px, volgt de kincontour.
    zet('variant kinschaduw',[(20,27),(21,27),(22,28),(23,28),(26,28),(27,28),(28,28),(23,29),(24,29),(25,29),(26,29)],M_,'+')
    NAAM='sprite_r3/jynx_regional_r3_variant_kinschaduw.png'
else: NAAM='sprite_r3/jynx_regional_r3.png'

assert ((o>0)==(r2>0)).all(), 'silhouet gewijzigd'
gez=np.zeros_like(o,bool); gez[9:28,18:34]=True
assert all(o[Y,X]==r2[Y,X] for Y,X in zip(*np.where(gez)) if r2[Y,X] in (1,9,10,11,12,13,14)), 'gezicht gewijzigd'
opslaan(o,NAAM)
print(NAAM); [print(' %3d  %s'%(v,n)) for n,v in tel.items()]
print('totaal anders dan r2: %d px | silhouet-diff %d | kleuren incl. transparant %d'%((o!=r2).sum(),((o>0)!=(r2>0)).sum(),len(set(o.ravel()))))
