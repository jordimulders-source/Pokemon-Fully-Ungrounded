# apply.py src dst mod... : zet handgeschreven rijsegmenten (W={y:[(x0,tekst)]}) op het raster; '=' = laten staan; meldt silhouetfouten
import sys,importlib
src,dst=sys.argv[1],sys.argv[2]
R=[list(l.rstrip('\n').ljust(64,'.')[:64]) for l in open(src)][:64]
for m in sys.argv[3:]:
    W=importlib.import_module(m).W
    for y,segs in W.items():
        for x0,s in segs:
            for i,c in enumerate(s):
                if c=='=': continue
                o=R[y][x0+i]
                if (o=='.')!=(c=='.'): print('SILHOUET!',m,'x',x0+i,'y',y,o,'->',c)
                R[y][x0+i]=c
open(dst,'w').write('\n'.join(''.join(r) for r in R)+'\n')
