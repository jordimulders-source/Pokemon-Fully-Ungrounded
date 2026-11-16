# Stap 2: kwantisering opschonen. Alleen per pixel, elke wijziging staat hieronder met reden.
# (i = x-29 in het natieve model, r = natieve rij)
rows=[list(l.rstrip('\n')) for l in open('sprite_r6/geest_kwant.txt')]
R0=6
def s(i,r,c): rows[r-R0][i]=c
E=[
 (7,13,'6','mondrand links dicht (model 56a562, half donker)'),
 (13,12,'6','mondrand rechtsboven dicht tegen het rechteroog (Weepinbell: gesloten rand)'),
 (2,17,'5','losse donkere pixel in de linkerkwab'),
 (3,19,'5','ruis: dambordpatroon linkerkwab'),
 (10,18,'5','losse donkere pixel in het lijf'),
 (17,20,'6','witte gaatjespixel tussen lijf en arm -> lijn'),
]
for i,r,c,_ in E: s(i,r,c)
# donkergroene buitenlijn: elke geestpixel die aan leeg grenst wordt 6 (niet de onderste rij: die zit in de schoorsteen)
H=len(rows); W=len(rows[0])
g=[r[:] for r in rows]
for y in range(H-1):
    for x in range(W):
        if g[y][x] in '52W':
            for dx,dy in((1,0),(-1,0),(0,1),(0,-1)):
                xx,yy=x+dx,y+dy
                if not(0<=xx<W and 0<=yy<H) or g[yy][xx]=='.':
                    rows[y][x]='6'; break
open('sprite_r6/geest_schoon.txt','w').write('\n'.join(''.join(r) for r in rows)+'\n')
for y,r in enumerate(rows): print('%2d'%(y+R0),''.join(r))
