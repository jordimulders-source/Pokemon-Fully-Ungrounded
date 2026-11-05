"""Ronde 1f: opgeheven been s px naar rechts, vanaf 1e. Gebruik: python3 been.py 3 5 7 9 11
- rij 4-30 (been, x22-36): verschoven, oude plek leeg;
- rij 31-35 (dijwortel/heup, x24..rechterrand): kopie s px naar rechts over de romp heen, rechts afgekapt op x43
  (1 px lucht tot de spiraal op x45); de staart (x>=39 rij 35-38, spiraal) blijft 0 px diff;
- bovenrand van de romp waar het been stond: omlijning D (rij 31) + afgeronde oksel bij de dij.
Daarna met de hand nagelopen per variant (zie NOTITIES.md)."""
import os, sys
from PIL import Image
H=os.path.dirname(os.path.abspath(__file__)); R=os.path.dirname(H)
TEK='.KDSVLFfPpBbGMmW'
PAL=[(152,208,160),(28,20,40),(50,48,98),(80,82,150),(114,118,190),(156,162,222),(72,56,100),(44,34,64),(214,170,204),(166,122,166),(184,230,255),(104,176,236),(40,98,176),(228,221,240),(170,164,198),(252,252,252)]
src=[list(l.rstrip('\n')) for l in open(os.path.join(R,'../ronde1e/raster.txt'))]
def bouw(s):
    g=[r[:] for r in src]
    leg={(x,y):src[y][x] for y in range(4,31) for x in range(22,37) if src[y][x]!='.'}
    for (x,y) in leg: g[y][x]='.'
    for (x,y),c in leg.items():
        if x+s<=43 or y<=27: g[y][x+s]=c
    for y in range(31,36):
        xs=[x for x in range(24,39) if src[y][x]!='.']
        for x in xs:
            X=x+s
            if X<=43: g[y][X]=src[y][x]
    # rechterrand afkappen op x43 (rij 28-35): rand = K, op rij 35 D (gaat over in de staart)
    for y in range(28,36):
        if g[y][43]!='.' and g[y][43] not in 'KD': g[y][43]='K' if y<35 else 'D'
        for x in (44,):
            if src[y][x]=='.' : g[y][x]='.'
    # bovenrand romp waar het been stond: D op de bovenste rij met lucht erboven
    for x in range(21,23+s):
        for y in range(29,36):
            if g[y][x]!='.' and g[y-1][x]=='.' and g[y][x] in 'LVS': g[y][x]='D'
    # afgeronde oksel: pixel links van de dijwortel op de rij boven de rug
    # oude binnenomlijning (rechterrand van de oude dijwortel) in de romp -> vacht
    for y in range(31,36):
        for x in range(24,24+s):
            if g[y][x] in 'KD' and g[y][x-1]!='.' and g[y][x+1]!='.' and g[y-1][x]!='.': g[y][x]='V'
    # rug als lichte boog: laatste s//3 kolommen voor de dij een rij hoger (oksel rond), lichtband onder de rugrand
    k=max(1,s//3)
    for x in range(23+s-k,23+s):
        g[30][x]='D'; g[31][x]='L'
    for x in range(24,23+s-k):
        if g[32][x] in 'VS': g[32][x]='L'
    return g
def save(g,d):
    os.makedirs(d,exist_ok=True)
    open(os.path.join(d,'raster.txt'),'w').write('\n'.join(''.join(r) for r in g)+'\n')
    im=Image.new('P',(64,64)); im.putpalette([v for c in PAL for v in c]); im.putdata([TEK.index(c) for r in g for c in r])
    im.save(os.path.join(d,'nachtaap_fase3.png'),transparency=0)
    with open(os.path.join(d,'normal.pal'),'w') as f: f.write('JASC-PAL\r\n0100\r\n16\r\n'+''.join('%d %d %d\r\n'%c for c in PAL))
for a in sys.argv[1:]:
    s=int(a); save(bouw(s),os.path.join(R,'v%d'%s))
