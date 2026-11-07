"""kleur4: ogen = Frost-ogen pixel voor pixel (Frost-index -> eigen index: 8->f, 9->d, a->c, 7->8, b->b, 5->4, 6->5, 3->6).
Oogzones: links x18-23 y35-42, rechts x25-31 y34-41 eerst naar basis 5, dan het sjabloon."""
CH='.123456789abcdef'
L=open('dj_rotom.txt').read().split('\n')
g=[list(r) for r in L[1:65]]
for y in range(35,42):
    for x in range(18,24): g[y][x]='5'
for y in range(34,42):
    for x in range(25,32): g[y][x]='5'
links=["5f4..","fdf4.","fccf6","8cc86","bfcf6","6bf6."]
rechts=["...f4.","..fdf6",".8dcf6",".fcc86","6fcfb6",".bfb6."]
for i,r in enumerate(links):
    for j,c in enumerate(r):
        if c!='.': g[36+i][18+j]=c
for i,r in enumerate(rechts):
    for j,c in enumerate(r):
        if c!='.': g[35+i][25+j]=c
L[1:65]=[''.join(r) for r in g]
open('dj_rotom.txt','w').write('\n'.join(L))
