"""g5: g4 + smaller (breedte 27), oorpunt links, mond begint X9. Frame 1 = rijen 0-31."""
import sys
L=[list(l) for l in open('g4.txt').read().split('\n')[:32]]
R={13:"...OO.OGGGgggggorrrrrrO.OoOGGO..",
14:"...OGOOGGggggggorrrrrrOOOOGGO...",
15:"...OGOGGgOgggggorrrrrrrOGOGO....",
16:"...OOOGgOOOOgggoOOOOrrrOGOOGO...",
17:"....OGggOryOgggorOyyOrrOOO.OGO..",
20:"....OgOgggOOOgOOOrOOOrO.........",
21:".....OgggOOgOOOoOOOrOOO.........",
}
for y,s in R.items():
    assert len(s)==32,(y,len(s)); L[y]=list(s)
open('g5_f1.txt','w').write('\n'.join(''.join(r) for r in L)+'\n')
for i,r in enumerate(L[6:31]): print('%2d'%(i+6),''.join(r))
