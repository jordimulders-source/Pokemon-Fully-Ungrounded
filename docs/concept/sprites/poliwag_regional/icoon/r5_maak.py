"""Ronde 5 (af): r3 + mond zonder roze (max 11 kleuren) + hele icoon 2 px naar links (midden x 15).
r4 probeerde de onderste omlijning in index 14: voeten verdwenen in het zwarte lijf, dus teruggedraaid."""
rows=[list(r) for r in open('r3_raster.txt').read().split('\n')[:64]]
for y in (18,49):
    rows[y]=['8' if c=='7' else c for c in rows[y]]
rows=[r[2:]+['.','.'] for r in rows]
open('r5_raster.txt','w').write('\n'.join(''.join(r) for r in rows)+'\n')
for i in list(range(12,29))+list(range(43,61)): print('%2d '%i+''.join(rows[i]))
