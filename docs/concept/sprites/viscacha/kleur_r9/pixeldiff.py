"""Pixeldiff r9 t.o.v. r8 (indexen), per zone. Paletwijzigingen staan apart onderaan."""
import sys; sys.path.insert(0,'.')
from palet import PAL as P9
sys.path.insert(0,'../kleur_r8'); import importlib.util
sp=importlib.util.spec_from_file_location('p8','../kleur_r8/palet.py'); m=importlib.util.module_from_spec(sp); sp.loader.exec_module(m); P8=m.PAL
a=[l.rstrip('\n') for l in open('../kleur_r8/raster.txt')][:64]; b=[l.rstrip('\n') for l in open('raster.txt')][:64]
Z=[('rugboog (selout, lijf, nekplooi)',lambda x,y:28<=x<=40 and 28<=y<=30 and (x,y) not in H),
   ('hooglicht B (rug + voorhoofd)',lambda x,y:(x,y) in H),
   ('staart (x47-62, r23-49)',lambda x,y:47<=x<=62 and 23<=y<=49),
   ('verre voorpoot (x12-19, r44-49)',lambda x,y:12<=x<=19 and 44<=y<=49),
   ('bil-sikkel (x42-47, r33-47)',lambda x,y:42<=x<=47 and 33<=y<=47),
   ('B->2 samengevoegd (oor, buiten de zones)',lambda x,y:a[y][x]=='B' and b[y][x]=='2')]
H={(x,y) for y in range(64) for x in range(64) if b[y][x]=='B'}
D=[(x,y) for y in range(64) for x in range(64) if a[y][x]!=b[y][x]]
out=[]; rest=list(D)
for n,f in Z:
    z=[p for p in rest if f(*p)]; rest=[p for p in rest if p not in z]
    out.append('%-45s %3d'%(n,len(z)))
out.append('%-45s %3d %s'%('BUITEN DE ZONES',len(rest),rest))
out.append('totaal gewijzigde pixels (index): %d'%len(D))
out.append('\nPalet r8 -> r9 (alle pixels met deze index veranderen mee van kleur):')
for i,(c,d) in enumerate(zip(P8,P9)):
    if c!=d: out.append('  %X: %s -> %s'%(i,c,d))
open('pixeldiff.txt','w').write('\n'.join(out)+'\n'); print('\n'.join(out))
