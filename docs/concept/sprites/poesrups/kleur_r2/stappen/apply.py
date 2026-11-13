import sys,importlib
src,dst=sys.argv[1],sys.argv[2]; mods=sys.argv[3:]
R=[list(l.rstrip('\n')) for l in open(src)][:64]
for m in mods:
    W=importlib.import_module(m).W
    for y,v in W.items():
        segs=v if isinstance(v,list) else [v]
        for x0,s in segs:
            for i,c in enumerate(s):
                if c=='=': continue
                o=R[y][x0+i]
                if (o=='.')!=(c=='.'): print('SILHOUET!',m,y,x0+i,o,c)
                R[y][x0+i]=c
open(dst,'w').write('\n'.join(''.join(r) for r in R)+'\n')
