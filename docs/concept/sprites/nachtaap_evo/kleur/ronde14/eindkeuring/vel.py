# Vergelijkingsvel eindkeuring ronde 14: 1x en 3x, licht en donker, naast echte sprites.
import sys
from PIL import Image, ImageDraw
G='/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/'
R='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/nachtaap_evo/'
def pal(p):
    L=open(p).read().split('\n')[3:19]; return [tuple(map(int,l.split())) for l in L]
def load(path,palp=None):
    im=Image.open(path)
    if palp and im.mode=='P':
        p=pal(palp); flat=[c for t in p for c in t]; im.putpalette(flat+[0]*(768-len(flat)))
    if im.mode=='P':
        t=im.info.get('transparency',0)
        im=im.crop((0,0,64,64)) if im.size[1]>64 else im
        rgba=im.convert('RGBA'); px=rgba.load(); src=im.load()
        for y in range(im.size[1]):
            for x in range(im.size[0]):
                if src[x,y]==0: px[x,y]=(0,0,0,0)
        return rgba
    im=im.convert('RGBA'); return im.crop((0,0,64,64))
names=['growlithe','slakoth','vigoroth','lairon','sableye','misdreavus','espurr','aipom','grumpig','natu','abra','monferno']
sprites=[('NACHTAAP r14',load(R+'kleur/ronde14/nachtaap.png')),('fase1',load(R+'referenties/fase1_goedgekeurd.png'))]
sprites+= [(n,load(G+n+'/anim_front.png',G+n+'/normal.pal')) for n in names]
S=3; cw=64*S+8
W=cw*7+8; H=(64*S+20)*4+ (64+16)*2+20
vel=Image.new('RGBA',(W,H),(255,255,255,255)); d=ImageDraw.Draw(vel)
y=0
for bg in [(248,248,248),(36,36,44)]:
    for row in range(2):
        for i,(n,im) in enumerate(sprites[row*7:(row+1)*7]):
            x=8+i*cw; d.rectangle([x,y,x+64*S,y+64*S+18],fill=bg+(255,))
            b=im.resize((64*S,64*S),Image.NEAREST); vel.alpha_composite(b,(x,y+16))
            d.text((x+2,y+2),n,fill=(200,0,0) if bg[0]<100 else (0,0,0))
        y+=64*S+20
for bg in [(248,248,248),(36,36,44)]:
    d.rectangle([0,y,W,y+80],fill=bg+(255,))
    for i,(n,im) in enumerate(sprites):
        vel.alpha_composite(im,(8+i*70,y+8))
    y+=80
vel.save(sys.argv[1])
