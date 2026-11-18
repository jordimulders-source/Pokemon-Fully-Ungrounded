# Buikvariant (Jordi 17 nov: "Maak nog een extra versie ernaast waar de buik de kleur krijgt van het vruchtvlees. Dus wit
# met zwarte spikkels"). Buikzone = de buikkant van keel, borst en buik tussen de poten: van de voorste buitenlijn
# (onderkaak/nek, verre arm) tot de eerste lange modelrib (23,29)->(28,36) en de voorrand van de nabije onderarm; onder
# begrensd door de bovenlijn van de verre achterpoot (24-25,42). Per rij x-bereik, alleen groene pixels (zwart blijft).
# Kleuren uit het teju-palet: W vruchtvlees, w schaduw (rechts/onder en tegen de rib = schaduwkant), s pitjes.
import numpy as np
RIJEN={30:(17,22),31:(17,23),32:(18,24),33:(18,25),34:(21,26),35:(22,26),36:(23,27),37:(24,29),38:(24,30),39:(25,30),
       40:(25,30),41:(25,29),42:(26,29),43:(26,28)}
def zone(o):
    Z=np.zeros((64,64),bool)
    for y,(a,b) in RIJEN.items():
        for x in range(a,b+1):
            if o[y,x] in (6,7,8,9): Z[y,x]=True
    return Z
# pitjes: losse s, nooit 8-buren van elkaar of van zwart/rand, ±1 per 7 px zoals de bek van de teju (7 pitjes op ±50 px).
PIT=[(19,31),(22,32),(20,33),(24,34),(23,36),(26,37),(29,38),(25,39),(28,40),(27,42)]
def buik(o):
    o=o.copy(); Z=zone(o)
    for y,x in zip(*np.where(Z)):
        # schaduwkant: rechterrand van de zone (tegen rib/onderarm) en de onderste 2 rijen
        a,b=RIJEN[y]; rechts=(x==b) or (x+1<64 and not Z[y,x+1] and o[y,x+1]!=0)
        o[y,x]=10 if (rechts or y>=42) else 11
    for x,y in PIT:
        assert Z[y,x], (x,y)
        o[y,x]=15
    return o
