import sys
from PIL import Image, ImageDraw
P='/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/'
def gen3(n):
    im=Image.open(P+n+'/anim_front.png')
    L=open(P+n+'/normal.pal').read().split('\n')[3:19]
    pal=[int(v) for l in L for v in l.split()]; im.putpalette(pal+[0]*(768-48))
    im=im.crop((0,0,64,64)); im.info['transparency']=0
    return im.convert('RGBA')
def rgba(p):
    return Image.open(p).convert('RGBA')
rn=sys.argv[1]
A=rgba('../rond/rond_A.png'); B=rgba(rn+'.png')
LI,DK=(232,236,232),(40,44,52)
W=1064; v=Image.new('RGB',(W,920),(255,255,255)); d=ImageDraw.Draw(v)
def put(im,x,y,s,bg):
    big=im.resize((64*s,64*s),Image.NEAREST); t=Image.new('RGB',big.size,bg); t.paste(big,(0,0),big); v.paste(t,(x,y))
put(A,0,20,8,LI); put(B,532,20,8,LI)
d.text((4,4),'rond_A 8x',fill=0); d.text((536,4),rn+' 8x',fill=0)
y=560; x=0
items=[('rond_A',A),(rn,B),('castform',gen3('castform')),('swablu',gen3('swablu')),('spheal',gen3('spheal'))]
for name,im in items:
    d.text((x+4,y-14),name,fill=0)
    put(im,x,y,1,LI); put(im,x,y+70,1,DK)
    put(im,x+68,y,2,LI); put(im,x+68,y+130,2,DK)
    x+=210
v.save('vel_'+rn+'.png')
