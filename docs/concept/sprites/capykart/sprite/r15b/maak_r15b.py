"""Capykart r15b = r15 + hoepelranden dicht (controle oude index per pixel)."""
import os
from PIL import Image
H=os.path.dirname(os.path.abspath(__file__)); R15=os.path.join(H,'../r15')
W=[(21,35,5,1),(22,35,5,1),(23,35,5,1),(24,36,5,1),(25,36,5,1),(26,37,5,1),(27,37,5,1),
   (48,34,5,1),(48,35,5,1),(49,35,9,8),
   (32,42,8,1),(33,42,1,6)]  # dalende boog: open bovenrand (32,42) dicht, band 2 px, lijn diagonaal (31,41)-(32,42)-(33,43)
fz=[(x,y) for x in range(28,32) for y in range(16,22)]+[(x,y) for x in range(17,24) for y in range(30,34)]+[(21,15),(22,15),(23,15),(21,16),(22,16),(23,16),(15,22),(16,22),(18,28),(19,28)]+[(x,30) for x in range(25,29)]
log=[]
for nm in ('creme','wit'):
    im=Image.open(os.path.join(R15,f'capykart_{nm}.png')); src=[[im.getpixel((x,y)) for x in range(64)] for y in range(64)]
    g=[r[:] for r in src]
    for x,y,o,n in W: assert src[y][x]==o,(nm,x,y,src[y][x]); g[y][x]=n
    o=Image.new('P',(64,64)); o.putpalette(im.getpalette()); o.putdata([v for r in g for v in r]); o.save(os.path.join(H,f'capykart_{nm}.png'),transparency=0)
    o.convert('RGBA').resize((512,512),Image.NEAREST).save(os.path.join(H,f'capykart_{nm}_8x.png'))
    d=[(x,y) for y in range(64) for x in range(64) if g[y][x]!=src[y][x]]; A={(x,y) for x,y,_,_ in W}
    # open hoepelrand: band-pixel (8/9 hoepel) 4-buur van licht hout 5/6/D
    hz=lambda x,y: (9<=x<=33 and 33<=y<=50) or (48<=x<=51 and 33<=y<=45)
    opn=[(x,y) for y in range(64) for x in range(64) if hz(x,y) and g[y][x]==8 and any(g[y+b][x+a] in (5,6,13) for a,b in ((1,0),(-1,0),(0,1),(0,-1)))]
    log.append(f'{nm}: {len(d)} px anders dan r15, buiten genoemde 0: {all(p in A for p in d)}; gezicht diff {sum(g[y][x]!=src[y][x] for x,y in fz)}; silhouet 0: {all((g[y][x]==0)==(src[y][x]==0) for x,y in d)}; kleuren {len(set(v for r in g for v in r))}; hoepelpixels (8) grenzend aan hout: {opn}')
open(os.path.join(H,'controle.txt'),'w').write('\n'.join(log)+'\n'); print('\n'.join(log))
