# Stap 5: na het samenvoegen staan roest- en staalstukken soms zonder scheiding tegen elkaar. Waar het model daar
# een lijn heeft (>=1 donkere modelpixel in het 2x2-blok), krijgt de roestkant de donkerste roesttint (#433425, model).
import numpy as np; from PIL import Image
o=np.load('post.npy'); WZ,SZ,RZ,MZ=np.load('z64.npy')
X,Y,ww,hh=map(int,open('plaats.txt').read().split()); y0,y1,x0,x1=map(int,open('half_crop.txt').read().split())
a=np.asarray(Image.open('natief_geschrapt.png').convert('RGB')).astype(int); drk=(a@[0.299,0.587,0.114])<40
OY,OX=1,0; ch=[]
B=lambda v:3<=v<=6; S=lambda v:8<=v<=10
for y,x in zip(*np.where(MZ)):
    v=o[y,x]
    if not B(v): continue
    if not any(S(o[y+dy,x+dx]) for dy,dx in ((1,0),(-1,0),(0,1),(0,-1))): continue
    hy,hx=y-Y+y0,x-X+x0; blk=drk[OY+2*hy:OY+2*hy+2,OX+2*hx:OX+2*hx+2]
    if blk.sum()>=1: ch.append((x,y))
for x,y in ch: o[y,x]=2
print('grenspixels naar #433425',len(ch))
np.save('grens.npy',o)
