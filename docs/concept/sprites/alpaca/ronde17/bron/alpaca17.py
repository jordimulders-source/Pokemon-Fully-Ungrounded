# Alpaca ronde 17: C2 verre voorpoot 1 px lager, C4 knie in de nabije voorpoot.
# Basis: ../../ronde16/variant_hals (goedgekeurd, leidend). Lijf en poten zijn in beide frames gelijk.
import numpy as np
from fu import *
old,pal=load('alpaca/ronde16/variant_hals'); a=old.copy()
OUT={1,6,10}
for f in (0,1):
    fr=a[64*f:64*f+64]; o=old[64*f:64*f+64]
    # --- C2: handschoen + manchet van de verre voorpoot (x24-31, y43-50) 1 rij omlaag; de poot wordt 1 rij langer
    #     (rij y42 '644551' herhaald op y43). Voet nu op y51: 3 px hoger dan de nabije (y54), was 4.
    blk=o[43:51,24:32].copy()
    glove=blk>0
    glove[50-43,31-24]=False   # (31,50) is de omlijning van de nabije achtervoet, niet van de handschoen
    fr[43:51,24:32][glove]=0
    sub=fr[44:52,24:32]; sub[glove]=blk[glove]
    fr[43,25:31]=o[42,25:31]
    # --- C4: knie nabije voorpoot. Rij y42 schuift 1 px naar achteren (gelijk aan y41), y43 eronder krijgt
    #     omlijning op x18 (anders open rand). Bovenbeen steiler, onderbeen schuin naar voren: een knik op y42.
    assert ''.join('%x'%v for v in o[42,18:23])=='62410' and ''.join('%x'%v for v in o[43,17:22])=='62341'
    fr[42,18:23]=[0,6,2,4,1]
    fr[43,18]=6
zones=[(f,17,42,31,51) for f in (0,1)]
r,outside=report(old,a,zones,OUT); print('\n'.join(r)); assert outside==0
save(a,pal,'alpaca/ronde16/variant_hals','alpaca/ronde17')
