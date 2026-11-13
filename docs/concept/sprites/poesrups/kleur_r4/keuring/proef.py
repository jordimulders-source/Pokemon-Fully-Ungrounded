# Proef van de voorgestelde reparaties (alleen tint); schrijft NIET naar de sprite, alleen een vergelijkingsvel
from PIL import Image
S='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/poesrups/kleur_r4/poesrups.png'
A=10
R1=[((41,45),A,7),((42,45),A,7),((42,46),A,7),((43,46),A,7),((42,47),A,7),((42,48),A,7)]
R2=[((x,57),6,5) for x in (24,25,26,28,29,30,31,32,35,36)]+[((x,58),6,5) for x in (32,33,36,37)]
def variant(reps):
    im=Image.open(S).copy(); px=im.load()
    for (x,y),a,b in reps:
        assert px[x,y]==a,((x,y),px[x,y],a)
        px[x,y]=b
    return im
vs=[('r4',[]),('R1',R1),('R2',R2),('R1+R2',R1+R2)]
bgs=[(248,248,248),(40,40,48),(120,168,96)]
def rgba(im):
    o=im.convert('RGBA'); p=im.load(); q=o.load()
    for y in range(64):
        for x in range(64):
            if p[x,y]==0: q[x,y]=(0,0,0,0)
    return o.crop((0,24,64,64))
W=Image.new('RGB',(len(vs)*(64*4+64+8),len(bgs)*160),(128,128,128))
for i,(n,r) in enumerate(vs):
    s=rgba(variant(r))
    for j,bg in enumerate(bgs):
        t=Image.new('RGBA',(64*4+64,160),bg+(255,))
        b=s.resize((256,160),Image.NEAREST); t.paste(b,(0,0),b); t.paste(s,(256,60),s)
        W.paste(t.convert('RGB'),(i*(64*5+8),j*160))
W.save('proef_reparaties.png')
