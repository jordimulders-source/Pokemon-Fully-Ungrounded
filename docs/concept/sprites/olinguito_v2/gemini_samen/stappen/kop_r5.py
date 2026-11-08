# r5-basis: r4, kopvak leeg; rechts van de kop (rij 37-45) r2-pixels terug (hals/poten zoals r2)
r4=[list(l.rstrip('\n')) for l in open('raster_r4.txt')]
r2=[list(l.rstrip('\n')) for l in open('raster_r2.txt')]
for y in range(18,46):
    for x in range(0,34):
        r4[y][x]=r2[y][x] if (y>=37 and x>=24) or (y>=29 and x==33) else '.'
open('stappen/r5_basis.txt','w').write('\n'.join(''.join(r) for r in r4)+'\n')
