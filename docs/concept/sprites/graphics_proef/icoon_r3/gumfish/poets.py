"""Gumfish: poetsen per zone op de gekozen onderlaag B35 (S 0,44; kop 1,4xS; lijf 1,16xS lang / 1,0xS hoog; staartvin 1,2xS;
dekkingsdrempel 0,35 zodat de rechterflank niet insleet). Elke pixel komt uit de onderlaag of uit een benoemde regel hieronder.
Plekken = frontpixels door dezelfde transformatie (bouw.naar_icoon), zie de commentaarregels. python3 poets.py -> icon_f1.png"""
import sys,os,numpy as np
from collections import Counter
from PIL import Image
H=os.path.dirname(os.path.abspath(__file__))+'/'
sys.argv=['bouw.py','B35','0.44','1.4','1.16','1.2','0.35']; __file__=H+'bouw.py'
exec(open(H+'bouw.py').read().split("if __name__")[0])
c=np.array(Image.open(H+'B35.png')); LOG=Counter()
def put(zone,pts,v):
    for x,y in pts:
        if c[y,x]!=v: c[y,x]=v; LOG[zone]+=1
def weg(zone,pts):
    for x,y in pts:
        if c[y,x]: c[y,x]=0; LOG[zone]+=1
# OOG: front (19,45) wit, (20,45),(19-20,46) donker -> (10,24) wit, (11,24),(10,25),(11,25) donker (2x2, minimum vis);
#      mondhoek front (19,48) -> (10,26) donker: het oog loopt in de mondhoek over, zoals in de front
put('oog',[(10,24)],3); put('oog',[(11,24),(10,25),(11,25),(10,26)],15)
#      onderste ooggrens front (20,47) -> (11,26): het front-oog is 2 breed x 3 hoog donker met de glans linksboven
put('oog',[(11,26)],15)
# MOND: lachlijn front (8,46)-(9,47)-(10..11,48)-(12..18,49)-(19,48) -> (4,26),(5..9,27),(10,26): U in 45-graden-trapjes
put('mond',[(4,26)]+[(x,27) for x in range(5,10)],15)
# LIPPEN (herkenningsteken, dik): bovenlip front rij 48 x12-18 -> rij 26 x5-9 roze; onderlip front rij 49-50 -> rij 27 x10-11, rij 28 x6-11;
#        onderkant van de lip (front rij 52 x12-14) -> omlijning (6,29)
put('lippen',[(x,26) for x in range(5,10)]+[(10,27),(11,27)]+[(x,28) for x in range(6,12)],10)
put('lippen',[(6,29)],14)
# BORSTVIN: bovenrand front (34-36,39) donker = vin over lijf -> (18,21),(19,21); rechterrand front (38,41-44) donker -> (20,22),(20,23);
#           de flank ligt in de front 2-3 px verder (x41 -> icoon x21-22): omlijning naar (21,22),(21,23)
put('borstvin',[(18,21),(19,21),(20,22),(20,23)],14)
#           flank: front x41 (rij 40-44) -> icoon x22, x39-40 lijfkleur tussen vinrand en flank -> x21; front (39,45) -> rand (21,24)
put('flank',[(21,22),(21,23),(20,24)],6); put('flank',[(22,22),(22,23),(21,24)],14)
#           linkerrand: de vin ligt over het lijf (deel over deel), dus ook links een binnenlijn zoals Gen 3-vissen (Carvanha, Wailmer);
#           de linkerbovenhoek loopt schuin zoals in de front (33,40)->(29,43): (17,21) top, (16,22) schuin, (15,23)-(15,25) links
put('borstvin',[(17,21),(16,22),(15,23),(15,24),(15,25)],14)
#           strepen (frontindex 11): 4-5 stralen worden er 3 (minder exemplaren), om de rij: rij 22 x17-18 (lichte bovenrand, front rij 40),
#           rij 24 x17-18, rij 26 x17-18; de rest lijfkleur
put('borstvin',[(19,23),(16,24)],6); put('borstvin',[(17,22),(18,22),(17,24),(18,24),(17,26),(18,26)],11)
# STAARTVIN: lichtroze rand front (51-55,27-30) -> (28,16),(28,17),(27,17)
put('staartvin',[(28,16),(28,17),(27,17)],11)
# KOPKRUIN volgens de frontrand: links (14,31)->(7,16), (11,34)->(5,18): trapje; rechts ligt de kruin een rij lager (front rij 32 x18-24 -> rij 17 x10-13)
weg('kopkruin',[(6,16),(5,17),(10,16),(11,16),(12,16),(13,16)])
put('kopkruin',[(6,17),(10,17),(11,17),(12,17)],15)
# RAND (rond, 45-graden-trapjes): alleen randpixels met twijfeldekking 0,30-0,60 (dekking.py) die de frontomtrek volgen:
#   buik loopt plat door tot front x25 (rij 53) -> (13,28) erbij;
#   vinonderkant hangt onder de buik (front (31-34,53-54)) -> (17,28) erbij;.
#   flank front (38,47) -> x20,6: (20,25) erbij; staartvin rechtsboven is in de front rond (57,28): (29,15) weg, (28,15)/(29,16) worden rand.
#   De oude randpixel wordt binnenkant in de kleur ernaast.
for (x,y),v,(ox,oy),f in [((20,25),14,(19,25),6),((13,28),14,(13,27),6),((17,28),14,(17,27),6)]:
    put('rand',[(x,y)],v); put('rand',[(ox,oy)],f)
weg('rand',[(29,15)]); put('rand',[(29,16)],15)
#   staartvin rechtsonder loopt in de front schuin terug (56,34)-(55,36): (29,19) weg, (28,19) rand
weg('rand',[(29,19)]); put('rand',[(28,19)],15)
if __name__=='__main__':
    im=Image.fromarray(c,'P'); im.putpalette(IP.flatten().tolist()); im.save(H+'icon_f1.png',transparency=0)
    print(dict(LOG))
