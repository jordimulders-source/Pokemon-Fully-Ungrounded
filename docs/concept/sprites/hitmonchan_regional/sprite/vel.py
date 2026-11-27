# vel.py rN [rM]: sprite 8x | vorige 8x | model (zelfde hoogte, natief raster) + 1x en 2x op licht en donker
from PIL import Image; import numpy as np, sys
D='docs/concept/sprites/hitmonchan_regional/sprite/'
def rgba(path):
    im=Image.open(path); im=im.convert('RGBA'); return im
def op(im,bg):
    b=Image.new('RGBA',im.size,bg); b.alpha_composite(im); return b.convert('RGB')
r=sys.argv[1]; cur=rgba(D+f'{r}/sprite.png')
prev=rgba(D+f'{sys.argv[2]}/sprite.png') if len(sys.argv)>2 else None
S=8
mod=Image.open(D+'natief.png').convert('RGB')
mod=mod.resize((int(mod.width*64*S/mod.height),64*S),Image.NEAREST)
tiles=[op(cur,(255,255,255)).resize((64*S,64*S),Image.NEAREST)]
if prev: tiles.append(op(prev,(255,255,255)).resize((64*S,64*S),Image.NEAREST))
tiles.append(mod)
Wt=sum(t.width for t in tiles)+10*len(tiles)
vel=Image.new('RGB',(Wt,64*S+150),(200,200,200))
x=0
for t in tiles: vel.paste(t,(x,0)); x+=t.width+10
y=64*S+10
vel.paste(op(cur,(240,240,232)),(10,y)); vel.paste(op(cur,(40,44,56)),(84,y))
vel.paste(op(cur,(240,240,232)).resize((128,128),Image.NEAREST),(170,y)); vel.paste(op(cur,(40,44,56)).resize((128,128),Image.NEAREST),(310,y))
vel.save(D+f'{r}/vel.png'); print('ok',vel.size)
