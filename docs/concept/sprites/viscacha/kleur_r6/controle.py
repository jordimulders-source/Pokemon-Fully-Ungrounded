"""Controle r6: silhouet t.o.v. het Gemini-masker (schaal 1:10,78), open randen, losse pixels, clusters < 3 px, kleuren, png = raster."""
from PIL import Image
D='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/viscacha/kleur_r6/'
r=[l.rstrip('\n') for l in open(D+'raster.txt')][:64]; a=[l.rstrip('\n') for l in open(D+'silhouet_auto.txt')][:64]
P=[(x,y) for y in range(64) for x in range(64)]
LIJN=set('128BF'); VLAK=set('345679ACDE')
print('t.o.v. Gemini-masker: ontbreekt',[(x,y) for x,y in P if a[y][x]=='#' and r[y][x]=='.'])
print('  extra buiten masker (dunne delen +):',[(x,y) for x,y in P if a[y][x]=='+' and r[y][x]!='.'].__len__(),'px; extra buiten masker en dunne delen:',[(x,y) for x,y in P if a[y][x]=='.' and r[y][x]!='.'])
nb4=lambda x,y:[(r[y+dy][x+dx] if 0<=y+dy<64 and 0<=x+dx<64 else '.') for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))]
print('open randen:',[(x,y,r[y][x]) for x,y in P if r[y][x]!='.' and '.' in nb4(x,y) and r[y][x] not in LIJN])
print('losse pixels:',[(x,y,r[y][x]) for x,y in P if r[y][x]!='.' and all(c=='.' for c in nb4(x,y))])
seen=set(); small=[]
for x,y in P:
    c=r[y][x]
    if c not in VLAK or (x,y) in seen: continue
    st=[(x,y)]; comp=[]; seen.add((x,y))
    while st:
        u,v=st.pop(); comp.append((u,v))
        for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
            q=(u+dx,v+dy)
            if 0<=q[0]<64 and 0<=q[1]<64 and q not in seen and r[q[1]][q[0]]==c: seen.add(q); st.append(q)
    if len(comp)<3: small.append((c,sorted(comp)))
print('clusters < 3 px:',len(small))
for c,comp in small: print('  ',c,comp)
used=sorted(set(''.join(r))-{'.'}); print('kleuren incl. transparant:',len(used)+1)
im=Image.open(D+'viscacha.png'); print('png == raster:',all(im.getpixel((x,y))==(0 if r[y][x]=='.' else int(r[y][x],16)) for x,y in P))
