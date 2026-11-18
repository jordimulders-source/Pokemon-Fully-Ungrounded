# Pitahaya-draak fase 3, r6: keurderpunten op r5. Gebruik: python3 maak_r6.py R5.png UIT.png [--buik]
import sys,numpy as np; sys.path.insert(0,'.')
from PIL import Image; from tekstraster import CH,schrijf
B=Image.open(sys.argv[1]); o=np.asarray(B).astype(int).copy(); r5=o.copy(); pal=B.getpalette(); LOG=[]
def meld(naam,voor):
    d=list(zip(*np.where(o!=voor)))
    for y,x in d: LOG.append((naam,x,y,CH[voor[y,x]],CH[o[y,x]]))
    print('%-70s %3d px'%(naam,len(d)))
BUIK='--buik' in sys.argv
if BUIK:
    from buik import buik
    voor=o.copy(); o=buik(o); meld('buik: slagschaduw onder kaak, sikkel i.p.v. band, pitjes van de rand',voor)
    from buik import zone; Zb=zone(o)
else: Zb=np.zeros((64,64),bool)
# 4. losse korrels borst -> G (in de buikvariant alleen buiten de buikzone)
voor=o.copy()
for x,y in ((21,33),(26,33),(22,33)):
    if not Zb[y,x]: o[y,x]=7
meld('borst: losse korrels (21,33),(26,33),(22,33) -> G',voor)
# 5. verre hand: linkerrand (10,43) zwart -> g
voor=o.copy(); o[43,10]=6; meld('verre hand: (10,43) -> g',voor)
OUT=[a for a in sys.argv[1:] if not a.startswith('--')][1]; n=(o!=r5).sum()
schrijf(o,pal,OUT); print(OUT,'t.o.v. r5',n)
with open(OUT[:-4]+'_afwijkingen.txt','w') as f:
    f.write('# %s: elke pixel die afwijkt van %s: stap | x | y | r5 -> r6 (tekens: %s)\n# totaal %d px\n'%(OUT,sys.argv[1],CH,n))
    for r in LOG: f.write('%s | %d | %d | %s -> %s\n'%r)
