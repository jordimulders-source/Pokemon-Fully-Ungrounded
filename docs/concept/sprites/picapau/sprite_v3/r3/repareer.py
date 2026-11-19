# Per-pixel reparaties op schoon.npy, elk benoemd en naar het model (zie _m_*.png modeluitsneden op spriteraster).
# codes: 1 zwart, 2/3/4 geel licht/mid/donker, 5/6 wang licht/donker, 7/8/9 staart licht/mid/donker,
# 10/11 grijs licht/donker, 12/13 vleugel licht/donker, 14 creme, 16 wit, 17 selout bruin (= kleur 13)
import numpy as np; from PIL import Image
o=np.load('schoon.npy').copy(); kaal=np.load('kaal_11.npy')
R={}
def zet(zone,lst):
    for x,y,v in lst: R.setdefault(zone,[]).append((x,y,o[y,x],v)); o[y,x]=v
zet('oog',[(30,19,16)])                                   # glans wit (model: lichte glans linksboven in het oog)
zet('ver oog/snavel',[(21,17,17),(23,19,11)])             # zwart boven de snavel terug naar 2 px (21,18)+(22,18); rest = koprand-selout / snavelbovenlijn
zet('snavel',[(24,25,3),(19,18,11),(20,18,11),(20,19,11)])   # + snavelpunt/bovenrand: buitenrand in donkergrijs i.p.v. lichtgrijs                                 # losse zwarte pixel onder de snavel (model: geel)
zet('verre wang',[(20,23,6),(21,23,5)])                             # model: rode verre wang aan de koprand, ring had hem zwart gemaakt
zet('wang',[(31,23,5),(32,23,5),(29,24,5),(34,25,6),(33,26,6),(32,27,6)])  # model wang vlak rood; donkere tint naar rechtsonder (Gen 3-schaduw)
zet('kuif',[(32,11,4),(33,11,17),(30,12,4),(31,12,4),(32,12,4)])  # model: geen zwart blok tussen de kuiven, donkergele schaduwlijn
zet('kuifpunt A',[(38,11,1),(37,12,4),(38,12,4)])         # model: punt naar rechtsboven op rij 11-12
zet('kuifpunt B',[(37,15,4),(38,15,1),(38,16,4),(39,16,1),(39,17,4),(40,17,4),(41,17,1)])  # model: rand rij 15 op x38, punt rij 16-18 tot x41
zet('verre vleugel',[(21,32,1),(21,33,1),(21,34,1),(22,32,13),(22,33,13),(22,34,13),(22,35,13),(22,36,13),(22,37,1)])  # model: bruine strook x21-22 rij 28-37 met zwarte rand
zet('vleugelstippen',[(41,27,14),(40,31,14),(43,32,14)])  # stip 2 (model x42 r27, op de rand -> 1 px naar binnen), stip 3 en 4 aangevuld tot model-dekking
zet('buikrand',[(33,44,4),(38,44,4)])                     # losse zwarte bult / bruine pixel in het geel (model: donkergeel)
zet('poten',[(30,48,10),(31,48,11),(35,48,11),(36,47,1),(29,49,1),(31,49,10),(32,49,10),(33,49,10),(34,49,11),(35,49,11)])
zet('poten rij 50',[(x,50,1) for x in range(31,37)])      # model: zwarte onderrand onder de rechtervoet (y 620-628 = rij 49.8-50.2)
zet('staart',[(43,45,9)]+[(45+i,44+i,9) for i in range(6)]+[(51,51,8),(52,51,9)])  # model: geen zwart in de staart; bovenrand donker roodbruin; staart loopt door tot x52 r51
# staarttinten per spritepixel uit het model (rood-gemiddelde): <145 donker, 145-175 mid, >=175 licht
n=np.asarray(Image.open('natief.png').convert('RGB')).astype(int)
for y in range(40,53):
    for x in range(38,55):
        if o[y,x] in (7,8,9) and kaal[y,x] in (7,8,9) and o[y,x]==kaal[y,x]:
            r=n[1+3*y:4+3*y,1+3*x:4+3*x,0].mean(); v=9 if r<145 else (8 if r<175 else 7)
            if v!=o[y,x]: zet('staarttinten',[(x,y,v)])
np.save('r1.npy',o)
tot=0
for z,l in R.items(): print('%-16s %2d px'%(z,len(l))); tot+=len(l)
print('totaal',tot)
