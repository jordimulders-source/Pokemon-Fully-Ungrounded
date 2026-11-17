# Meet: afwijking per zone t.o.v. de kale reductie (dichtstbijzijnde paletkleur per geschrapt-modelpixel),
# losse pixels (geen 4-buur met dezelfde index), lijnpixels (#) zonder lijnbuur, kleurtelling.
import sys; from PIL import Image; import numpy as np
D='docs/concept/sprites/mate_fase2/sprite/'; R=sys.argv[1] if len(sys.argv)>1 else 'r1'
im=Image.open(D+R+'/mate2.png'); s=np.asarray(im).astype(int); pal=np.array(im.getpalette()[:48]).reshape(16,3)
g=np.asarray(Image.open(D+'r1/geschrapt.png').convert('RGB')).astype(int); H,W,_=g.shape; oy=64-H-1; ox=(64-W)//2
sp=s[oy:oy+H,ox:ox+W]; used=sorted(set(s.flatten()))
kaal=np.abs(g[:,:,None,:]-pal[None,None,1:len(used)]).sum(3).argmin(2)+1
kaal[sp==0]=0
zones={'gezicht ventje':(33,5,48,15),'ventje rest':(28,0,52,28),'ogen kano':(0,22,16,38),'verre bombilla':(19,1,34,21),'nabije bombilla':(36,17,60,44),'bladhoop+rand':(5,17,30,29),'romp':(0,26,62,44),'water/achter':(48,12,62,26)}
print('kleuren incl. transparant:',len(used))
for n,(x0,y0,x1,y1) in zones.items():
    z=(sp[y0:y1,x0:x1]!=kaal[y0:y1,x0:x1])&(sp[y0:y1,x0:x1]>0); print('%-16s afwijkend van kale reductie: %d / %d'%(n,z.sum(),((sp[y0:y1,x0:x1]>0)).sum()))
los=[];zw=[]
for y in range(64):
    for x in range(64):
        i=s[y,x]
        if i==0: continue
        nb=[s[y+dy,x+dx] for dy,dx in((1,0),(-1,0),(0,1),(0,-1)) if 0<=y+dy<64 and 0<=x+dx<64]
        if i not in nb and i!=1: los.append((x,y,i))
print('losse pixels (x,y,idx):',len(los),los)
print('rand: kolom 0/63 of rij 0/63 gebruikt:',s[:,0].any(),s[:,63].any(),s[0].any(),s[63].any())
