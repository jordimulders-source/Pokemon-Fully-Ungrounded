"""Capykart r15 = r14 + keurderreparaties (hoepels dicht omlijnd, cockpitrand, rood blok 1 px naar links).
Elke wissel controleert eerst de verwachte oude index."""
import os
from PIL import Image
H=os.path.dirname(os.path.abspath(__file__)); R14=os.path.join(H,'../r14')
W=[]  # (x,y,oud,nieuw)
for p in [(9,37),(10,36),(11,36),(12,35),(13,35)]: W.append((*p,8,1))
W.append((14,34,4,1))
for x in range(15,19): W.append((x,34,6,1))
for p in [(28,38),(29,39),(30,40),(31,41)]: W.append((*p,5,1))
W.append((33,42,6,1)); W.append((32,41,1,6))
for y in (44,45,46): W.append((30,y,6,1))
W += [(34,38,6,1),(35,38,1,4),(34,40,4,1),(34,41,4,1)]
for y in range(36,45): W.append((49,y,8,1))
log=[]
for nm in ('creme','wit'):
    im=Image.open(os.path.join(R14,f'capykart_{nm}.png')); src=[[im.getpixel((x,y)) for x in range(64)] for y in range(64)]
    g=[r[:] for r in src]
    for x,y,o,n in W:
        assert src[y][x]==o,(nm,x,y,src[y][x],o); g[y][x]=n
    # rood blok rijen 19-24: x46..57 -> x45..56
    for y in range(19,25):
        assert src[y][45]==0 and src[y][57]==1
        for x in range(45,57): g[y][x]=src[y][x+1]
        g[y][57]=0
    for y in (18,25): assert src[y][45]==0; g[y][45]=1
    o=Image.new('P',(64,64)); o.putpalette(im.getpalette()); o.putdata([v for r in g for v in r]); o.save(os.path.join(H,f'capykart_{nm}.png'),transparency=0)
    o.convert('RGBA').resize((512,512),Image.NEAREST).save(os.path.join(H,f'capykart_{nm}_8x.png'))
    allowed={(x,y) for x,y,_,_ in W}|{(x,y) for y in range(19,25) for x in range(45,58)}|{(45,18),(45,25)}
    d=[(x,y) for y in range(64) for x in range(64) if g[y][x]!=src[y][x]]
    fz=[(x,y) for x in range(28,32) for y in range(16,22)]+[(x,y) for x in range(17,24) for y in range(30,34)]+[(21,15),(22,15),(23,15),(21,16),(22,16),(23,16),(15,22),(16,22),(18,28),(19,28)]+[(x,30) for x in range(25,29)]
    sil=sum(1 for x,y in d if (g[y][x]==0)!=(src[y][x]==0))
    log.append(f'{nm}: {len(d)} px anders dan r14, buiten genoemde pixels: {sum(1 for p in d if p not in allowed)}; gezicht diff {sum(g[y][x]!=src[y][x] for x,y in fz)}; silhouet {sil} px (rood blok); kleuren {len(set(v for r in g for v in r))}')
open(os.path.join(H,'controle.txt'),'w').write('\n'.join(log)+'\n'); print('\n'.join(log))
