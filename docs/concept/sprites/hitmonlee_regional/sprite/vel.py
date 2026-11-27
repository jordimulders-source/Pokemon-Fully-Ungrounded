# vel.py rN [rN-1]: sprite 8x | vorige 8x | model (zelfde hoogte) + 1x op licht en donker
from PIL import Image; import numpy as np, sys
D='docs/concept/sprites/hitmonlee_regional/sprite/'
def rgba(path):
    im=Image.open(path)
    if im.mode=='P': im=im.convert('RGBA')
    return im.convert('RGBA')
def op(im,bg):
    b=Image.new('RGBA',im.size,bg); b.alpha_composite(im); return b.convert('RGB')
r=sys.argv[1]; cur=rgba(D+f'{r}/sprite.png')
prev=rgba(D+f'{sys.argv[2]}/sprite.png') if len(sys.argv)>2 else None
S=8
mod=Image.open('docs/concept/sprites/hitmonlee_regional/gemini/r2.png').convert('RGB').crop((int(13*10.24),int(13*10.24),int(81*10.24),int(87*10.24)))
mod=mod.resize((int(mod.width*64*S/mod.height),64*S),Image.LANCZOS)
tiles=[op(cur,(255,255,255)).resize((64*S,64*S),Image.NEAREST)]
if prev: tiles.append(op(prev,(255,255,255)).resize((64*S,64*S),Image.NEAREST))
tiles.append(mod)
Wt=sum(t.width for t in tiles)+10*len(tiles)
vel=Image.new('RGB',(Wt,64*S+90),(200,200,200))
x=0
for t in tiles: vel.paste(t,(x,0)); x+=t.width+10
vel.paste(op(cur,(240,240,232)),(10,64*S+13)); vel.paste(op(cur,(40,44,56)),(90,64*S+13))
vel.paste(op(cur,(240,240,232)).resize((128,128)).crop((0,0,128,77)),(170,64*S+13))
vel.save(D+f'{r}/vel.png'); print('ok',vel.size)
