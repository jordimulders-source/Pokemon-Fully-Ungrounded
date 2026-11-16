# Ogen: varianten met andere bemonsteringsfase; oogpixel = zwart als >=30% oogzwart (lum<90), anders vulkleur (incl. grijze oogkas uit het model)
import itertools; import numpy as np; from PIL import Image, ImageDraw
from zone import *
DK=AL&(LUM<90)
def oog(i,j,phx,phy):
    tw=0; dk=0; c=np.zeros(3); cw=0
    for y,x,w in cellen(i,j,phx,phy):
        tw+=w
        if not AL[y,x]: continue
        if DK[y,x]: dk+=w; continue
        c+=w*RGB[y,x]; cw+=w
    if dk/tw>=0.3: return 1
    return dichtst(c/cw,GRP)
VENSTERS=[(13,18,29,33),(28,33,29,33)]
r1=np.load('r1_bevroren.npy'); res=[]
op=r1>0; p=np.pad(op,1); RAND=op&~(p[:-2,1:-1]&p[2:,1:-1]&p[1:-1,:-2]&p[1:-1,2:])
for phx,phy in itertools.product([0,1/3,1/2,2/3],repeat=2):
    o=r1.copy()
    for i0,i1,j0,j1 in VENSTERS:
        for j in range(j0,j1):
            for i in range(i0,i1):
                if not RAND[j,i]: o[j,i]=oog(i,j,phx,phy)
    res.append((phx,phy,o))
np.save('ogen_varianten.npy',np.array([r[2] for r in res])); 
S=14; tegels=[]
m=Image.open('model_natief.png'); w=Image.new('RGBA',m.size,'white'); w.alpha_composite(m); W=w.convert('RGB')
def paar(o):
    ims=[Image.fromarray(rgb(o)[j0:j1,i0:i1]).resize(((i1-i0)*S,(j1-j0)*S),Image.NEAREST) for i0,i1,j0,j1 in VENSTERS]
    v=Image.new('RGB',(ims[0].width*2+6,ims[0].height),'white'); v.paste(ims[0],(0,0)); v.paste(ims[1],(ims[0].width+6,0)); return v
nat=[]
for i0,i1,j0,j1 in VENSTERS:
    nx0,ny0=X0+(i0-1)*F,Y0+(j0-17)*F; nat.append(W.crop((int(nx0),int(ny0),int(nx0+(i1-i0)*F),int(ny0+(j1-j0)*F))).resize(((i1-i0)*S,(j1-j0)*S),Image.NEAREST))
nv=Image.new('RGB',(nat[0].width*2+6,nat[0].height),'white'); nv.paste(nat[0],(0,0)); nv.paste(nat[1],(nat[0].width+6,0))
tegels=[('model natief',nv),('r1',paar(r1))]+[('o%d %.2f/%.2f'%(k,r[0],r[1]),paar(r[2])) for k,r in enumerate(res)]
tw,th=tegels[0][1].size; n=6; v=Image.new('RGB',(n*(tw+10),3*(th+20)),'white'); dr=ImageDraw.Draw(v)
for k,(t,im) in enumerate(tegels):
    X,Y=(k%n)*(tw+10),(k//n)*(th+20); v.paste(im,(X,Y+16)); dr.text((X+2,Y+2),t,fill=(0,0,0))
v.save('ogenvel_r2.png')
