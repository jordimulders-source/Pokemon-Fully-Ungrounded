g=[list(r) for r in open('../../ronde1/bron/raster_grid.txt').read().split()]
sil=[l.strip() for l in open('../../../silhouet_hand/ronde5/silhouet.txt') if l.strip()]
rows={}
for line in open('nieuw.txt'):
    line=line.split('#')[0].strip()
    if not line: continue
    y,x,s=line.split(); rows.setdefault(int(y),[]).append((int(x),s))
for y,parts in rows.items():
    lim=49 if y<=28 else 64
    for x in range(lim): g[y][x]='.' if sil[y][x]=='.' else '?'
    for x0,s in parts:
        for i,ch in enumerate(s): g[y][x0+i]=ch
bad=[(x,y,g[y][x]) for y in range(64) for x in range(64) if (g[y][x]=='?') or ((g[y][x]!='.')!=(sil[y][x]=='#'))]
print('fouten',bad)
open('raster_grid.txt','w').write('\n'.join(''.join(r) for r in g)+'\n')
from PIL import Image
PAL={'.':'98d0a0','k':'1a0f0b','m':'241712','d':'4c3121','b':'6a4630','l':'8a603e','g':'6b5442','h':'8a6c55',
 's':'54443c','e':'4a3324','r':'6e2418','i':'a8462a','w':'f2ead6','n':'b0a28a','p':'c08a80','q':'8e4f58'}
ORDER='.kmdblghserjwnpq'.replace('j','i')
ORDER='.kmdblghseriwnpq'
assert len(ORDER)==16 and set(ORDER)==set(PAL)
flat=[]
for ch in ORDER: flat+=[int(PAL[ch][i:i+2],16) for i in (0,2,4)]
im=Image.new('P',(64,64)); im.putpalette(flat+[0]*(768-len(flat)))
unknown={c for r in g for c in r if c not in PAL}; print('onbekend',unknown)
im.putdata([ORDER.index(g[y][x]) for y in range(64) for x in range(64)])
im.save('../olinguito.png',transparency=0)
