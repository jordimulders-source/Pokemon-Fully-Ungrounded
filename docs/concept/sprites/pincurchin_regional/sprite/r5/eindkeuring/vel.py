# Eindkeuring-vel: sprite 8x naast model en Gen 3-referenties (alleen lezen)
from PIL import Image
import sys
R='/home/user/Pokemon-Fully-Ungrounded/'
def f1(p):
    im=Image.open(R+p).convert('RGBA'); 
    if im.size[1]>64: im=im.crop((0,0,64,64))
    px=im.load(); 
    # transparant = eerste paletkleur
    src=Image.open(R+p)
    if src.mode=='P':
        q=src.crop((0,0,64,64)).load()
        for y in range(64):
            for x in range(64):
                if q[x,y]==0: px[x,y]=(255,255,255,255)
    return im
items=['docs/concept/sprites/pincurchin_regional/sprite/r5/V1_oog4x5_mond+1+2.png']+sys.argv[2:]
S=int(sys.argv[1])
W=Image.new('RGB',(64*S*len(items),64*S),'white')
for i,p in enumerate(items):
    W.paste(f1(p).resize((64*S,64*S),Image.NEAREST),(64*S*i,0))
W.save(R+'docs/concept/sprites/pincurchin_regional/sprite/r5/eindkeuring/vel_%d.png'%len(items))
