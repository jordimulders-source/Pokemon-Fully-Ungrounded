# Nachtaap ronde 12: A6 zuil van romp + verre arm breken. Basis: ../../ronde11 (goedgekeurd, leidend; zonder elleboog).
# Onderarm (y49-50) knikt 1 px naar buiten, naar de hand toe; de heup (romp-zijkant) wordt daar 1 px breder.
# Geen bult en geen pols terug (dat was de afgekeurde elleboog).
from fu import *
old,pal=load('nachtaap/ronde11'); a=old.copy()
OUT={1,2}
for f in (0,1):
    for y in (49,50):
        assert ''.join('%x'%old[64*f+y,x] for x in range(31,37))=='313310'
        put(a,f,32,y,['31331'])
# schaduwkant van de verre arm (rechterkolom) een tint donkerder (3 -> 2): de arm krijgt een eigen ronding
# en is niet meer één vlak met de romp-zijkant.
for f in (0,1):
    for y in range(42,51):
        x=34 if y<49 else 35
        assert a[64*f+y,x]==3,(f,x,y,a[64*f+y,x]); a[64*f+y,x]=2
zones=[(f,32,49,36,50) for f in (0,1)]+[(f,34,42,34,48) for f in (0,1)]
r,outside=report(old,a,zones,OUT); print('\n'.join(r)); assert outside==0
save(a,pal,'nachtaap/ronde11','nachtaap/ronde12')
