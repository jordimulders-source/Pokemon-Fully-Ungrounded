"""Vel: front 4x | icoon f1 (en f2) 8x | 1x tussen echte knaagdier-iconen op groen. python3 vel.py icon.png uit.png"""
import sys,numpy as np
from PIL import Image,ImageDraw
def pal(p):
    L=open(p).read().split('\n'); return [tuple(int(v) for v in L[3+k].split()[:3]) for k in range(16)]
def rgba(a,P):
    o=np.zeros(a.shape+(4,),np.uint8)
    for k in range(1,16): o[a==k]=P[k]+(255,)
    return Image.fromarray(o)
ic=Image.open(sys.argv[1]); ia=np.array(ic); IP=[tuple(ic.getpalette()[3*k:3*k+3]) for k in range(16)]
fr=Image.open('docs/concept/sprites/cuyby/ronde4/anim_front.png'); FP=[tuple(fr.getpalette()[3*k:3*k+3]) for k in range(16)]
f=rgba(np.array(fr)[:64],FP).resize((256,256),Image.NEAREST)
W=Image.new('RGB',(256+20+256*2+20+300,300),(115,197,164))
W.paste(f,(0,20),f)
for j in range(2):
    i=rgba(ia[32*j:32*j+32],IP).resize((256,256),Image.NEAREST); W.paste(i,(276+266*j,20),i)
bur=[('pikachu',2),('dedenne',0),('pachirisu',0),('rattata',2)]
x=820
for n,(sp,p) in enumerate(bur+[('X',0)]):
    if sp=='X': a=ia[:32]; P=IP
    else: a=np.array(Image.open(f'graphics/pokemon/{sp}/icon.png'))[:32]; P=pal(f'graphics/pokemon/icon_palettes/pal{p}.pal')
    im=rgba(a,P); W.paste(im,(x+(n%3)*34,40+(n//3)*34),im)
    im2=im.resize((64,64),Image.NEAREST); W.paste(im2,(x+(n%3)*70,120+(n//3)*70),im2)
W.save(sys.argv[2])
