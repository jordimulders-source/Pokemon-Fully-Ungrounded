"""Raster van front+rug-paren op 2x. python3 front_rug_vel.py uit.png [--set gba|new] soort ..."""
import os,sys,numpy as np
from PIL import Image,ImageDraw
a=sys.argv[2:]; st='gba'
if '--set' in a: i=a.index('--set'); st=a[i+1]; a=a[:i]+a[i+2:]
sfx='_gba' if st=='gba' else ''
def pal(p):
    L=open(p).read().split('\n'); return [tuple(int(v) for v in L[3+k].split()[:3]) for k in range(int(L[2]))]
def rgb(p,P):
    ix=np.array(Image.open(p))[:64]; o=np.full((64,64,3),235,np.uint8)
    for k in range(1,16): o[ix==k]=P[k]
    return Image.fromarray(o)
C=6; Z=2; cell=(64*Z*2+12,64*Z+16); rows=(len(a)+C-1)//C
img=Image.new('RGB',(C*cell[0],rows*cell[1]),'white'); d=ImageDraw.Draw(img)
for n,sp in enumerate(a):
    D='graphics/pokemon/'+sp
    f=D+'/anim_front%s.png'%sfx
    if not os.path.exists(f): f=D+'/front%s.png'%sfx
    P=pal(D+'/normal%s.pal'%sfx)
    x,y=(n%C)*cell[0],(n//C)*cell[1]
    img.paste(rgb(f,P).resize((128,128),Image.NEAREST),(x,y+14)); img.paste(rgb(D+'/back%s.png'%sfx,P).resize((128,128),Image.NEAREST),(x+132,y+14))
    d.text((x+2,y+1),sp,fill=0)
img.save(sys.argv[1])
