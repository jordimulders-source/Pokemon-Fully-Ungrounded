# Buikvariant r6 (Jordi 17 nov: "Maak nog een extra versie ernaast waar de buik de kleur krijgt van het vruchtvlees. Dus wit
# met zwarte spikkels"). Zone = r5 (RIJEN, zie ../sprite_r5/NOTITIES.md). r6 (keurder): slagschaduw onder de kaak
# (rij 30 helemaal w, (17-18,31) w); schaduw rechts als sikkel i.p.v. 1 px-band: breedte per rij hieronder (smal boven,
# 2 px tegen de onderarm, onderaan rij 42-43 helemaal); pitjes los, niet tegen de buitenlijn, niet in de sikkel.
import numpy as np
RIJEN={30:(17,22),31:(17,23),32:(18,24),33:(18,25),34:(21,26),35:(22,26),36:(23,27),37:(24,29),38:(24,30),39:(25,30),
       40:(25,30),41:(25,29),42:(26,29),43:(26,28)}
SIKKEL={30:99,31:0,32:0,33:1,34:1,35:1,36:2,37:2,38:2,39:2,40:2,41:3,42:99,43:99}   # px w aan de rechterkant
PIT=[(20,31),(22,32),(20,33),(24,34),(24,36),(26,37),(28,38),(26,39),(28,40),(27,42)]
def zone(o):
    Z=np.zeros((64,64),bool)
    for y,(a,b) in RIJEN.items():
        for x in range(a,b+1):
            if o[y,x] in (6,7,8,9,10,11,15): Z[y,x]=True
    return Z
def buik(o):
    o=o.copy(); Z=zone(o)
    for y,x in zip(*np.where(Z)):
        b=max(xx for xx in range(64) if Z[y,xx])
        o[y,x]=10 if (b-x<SIKKEL[y]) else 11
    o[31,17]=o[31,18]=10
    for x,y in PIT:
        assert Z[y,x],(x,y); o[y,x]=15
    return o
