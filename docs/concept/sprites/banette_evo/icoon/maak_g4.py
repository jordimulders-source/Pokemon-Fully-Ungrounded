L=[list(l) for l in open('g3.txt').read().split('\n')[:32]]
links={11:".......OGGGGgggo",12:"......OGGGGggggo",13:"...OO.OGGGgggggo",14:"..OGGOOGGggggggo",
15:"...OGOGGgOgggggo",16:"...OOOGgOOOOgggo",17:"....OGggOryOgggo",18:"....OggOgggggggo",
19:"....OggOgggggggo",20:"....OgOggggggggo",21:"....OgOggggggggo",22:".....OOggggggggo"}
for y,s in links.items(): L[y][:16]=list(s)
# rechterdeel onder de ogen opnieuw: rood tot de rand X22
for y in range(18,23):
    for x in range(16,22): L[y][x]='r'
    L[y][22]='O'; L[y][23]='.' if y>18 else L[y][23]
# mondband zigzag
D={19:[11,15,19],20:[8,10,11,12,14,15,16,18,19,20],21:[8,9,10,12,13,14,16,17,18,20,21],22:[9,13,17,21]}
for y,xs in D.items():
    for x in xs: L[y][x]='O'
# zaadje: naad onder de mond
L[23][15]='o'
open('g4.txt','w').write('\n'.join(''.join(r) for r in L+L)+'\n')
for i,r in enumerate(L): print('%2d'%i,''.join(r))
