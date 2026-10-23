# Cuychu ronde 6: C2/C3 meest linkse pootkussen (11,51) weg; de lok eindigt in een punt zoals de andere lokken (141/1).
# Basis: ../../ronde5/variant_pluk (goedgekeurd, leidend). Onderrand gelijk in beide frames.
from fu import *
old,pal=load('cuyby_evo/ronde5/variant_pluk'); a=old.copy()
OUT={1,6}
for f in (0,1):
    assert ''.join('%x'%old[64*f+51,x] for x in range(8,13))=='111e1'
    put(a,f,9,51,['141.',   # y51: x9 1, x10 haar 4, x11 kussen e -> omlijning 1, x12 weg
                  '.1..'])  # y52: punt van de lok op x10, (11,52) weg
zones=[(f,9,51,12,52) for f in (0,1)]
r,outside=report(old,a,zones,OUT); print('\n'.join(r)); assert outside==0
save(a,pal,'cuyby_evo/ronde5/variant_pluk','cuyby_evo/ronde6')
