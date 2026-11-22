import sys, numpy as np
from PIL import Image
R='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/viscacha/icoon/onderdelen/'
b=np.array(Image.open(R+'icon_a2_af.png')); n=np.array(Image.open(sys.argv[1]))
Z={'oren':(6,15,7,14),'oog':(8,11,15,17),'snorharen':(0,6,18,24),'wangzak links':(3,7,14,18),'nekpluk':(11,17,14,19),'voorpoten':(6,15,20,26)}
for f in (0,1):
    d=np.argwhere(b[f*32:f*32+32]!=n[f*32:f*32+32]); cnt={k:0 for k in Z}; out=[]
    for y,x in d:
        yy=y-(1 if f==1 and y<=23 else 0)  # frame 2: body 1 px lower
        for k,(x0,x1,y0,y1) in Z.items():
            if x0<=x<=x1 and y0<=yy<=y1: cnt[k]+=1; break
        else: out.append((int(x),int(y)))
    print('frame',f+1,'totaal',len(d),cnt,'BUITEN ZONES:',len(out),out)
# singletons (no 4-neighbour same colour), excluding outline greys
for f in (0,1):
    a=n[f*32:f*32+32]; s=[]
    for y in range(1,31):
        for x in range(1,31):
            v=a[y,x]
            if v in (0,14,15): continue
            if not any(a[y+dy,x+dx]==v for dy,dx in ((0,1),(1,0),(0,-1),(-1,0))): s.append((x,y,'%X'%v))
    print('frame',f+1,'enkele pixels (geen buur v. zelfde kleur):',s)
