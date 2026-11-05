"""rijen.txt + snavel uit r3 -> raster.txt (64x64). Spaties in rijen.txt worden genegeerd ('.' = transparant)."""
H='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/kolibrie_pre/blender/A/'
r3=[l.rstrip('\n') for l in open(H+'kleur_r3/raster.txt')][:64]
g=[['.']*64 for _ in range(64)]
for l in open(H+'kleur_r4/rijen.txt'):
    if l.startswith('#') or not l.strip(): continue
    y,x0,*p=l.split(); p=''.join(p); y=int(y); x0=int(x0)
    for i,c in enumerate(p): g[y][x0+i]=c
# snavel bevroren (vorm en kleur), A (oude snavel-donker) -> 2 (bijna gelijk, A is nu iris donker)
SNAVEL={15:(12,12),16:(13,14),17:(14,17),18:(15,18),19:(16,18),20:(13,18),21:(15,17)}
for y,(a,b) in SNAVEL.items():
    for x in range(a,b+1): g[y][x]={'A':'2'}.get(r3[y][x],r3[y][x])
open(H+'kleur_r4/raster.txt','w').write('\n'.join(''.join(r) for r in g)+'\n')
