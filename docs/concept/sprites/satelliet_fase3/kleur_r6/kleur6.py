# Kleurronde r6 ruimtestation: alleen indexwissels per pixel op eindkeuring_r5/sprite.png.
# Silhouet exact gelijk (alpha-diff 0). Minder tinten per onderdeel, harder contrast.
# Draaien: python3 kleur6.py (vanuit elke map). Schrijft sprite.png, sprite_8x.png, vel.png.
import os, numpy as np
from PIL import Image, ImageDraw
H=os.path.dirname(os.path.abspath(__file__)); R=os.path.normpath(os.path.join(H,'..'))
G=os.path.normpath(os.path.join(R,'..','..','..','..'))
src=Image.open(os.path.join(R,'eindkeuring_r5','sprite.png'))
A=np.array(src); PAL0=src.getpalette()[:48]

# nieuw palet (index: rgb, rol)
PAL={0:(0,0,0),
 1:(24,19,36),     # zwart: outline shadow (ongewijzigd)
 2:(41,38,69),     # navy: outline base (ongewijzigd)
 3:(60,48,96),     # binnenlijn / donkerste eigen tint (iets paarser dan r5)
 4:(150,138,186),  # wit schaduw (r5: C, B en lichte 4)
 5:(206,198,228),  # wit midden (r5: E en D)
 6:(80,44,104),    # paars donker (ring schaduw)
 7:(116,70,142),   # paars midden
 8:(156,100,182),  # paars licht
 9:(38,104,110),   # iris donker
 10:(86,182,174),  # iris licht
 11:(58,52,104),   # paneel vak (r5: navy 2 binnen het paneel)
 12:(120,106,172), # paneel rasterlijn (r5: lila 5)
 13:(0,0,0),       # vrij
 14:(0,0,0),       # vrij
 15:(248,248,252)} # wit licht (ongewijzigd)

# r5-pixels met index 4 waar het verkleinde model L<100 heeft (gemeten met de kaal.py-reductie, top=13)
DONKER4={(29,43),(18,42),(41,34),(21,44),(46,26),(20,43),(45,25),(19,42),(37,39),(34,37),(27,38),(23,32),(41,35),(35,28),(49,36)}
S=os.path.join(os.path.dirname(R),'satelliet_fase3')
B=np.zeros_like(A)
h,w=A.shape
PANEL={1,2,5}
def nb(y,x):
    return [A[y+dy,x+dx] if 0<=y+dy<h and 0<=x+dx<w else 0 for dy,dx in ((-1,0),(1,0),(0,-1),(0,1))]
for y in range(h):
    for x in range(w):
        v=A[y,x]; n=nb(y,x)
        if v==0: continue
        inpanel = all(q in PANEL for q in n)          # alle 4 buren paneelkleur, geen transparant
        if v==15: B[y,x]=15
        elif v in (14,13): B[y,x]=5
        elif v in (12,11): B[y,x]=4
        elif v==4: B[y,x]=3 if (x,y) in DONKER4 else 4   # model donker (L<100) = naad/binnenlijn, anders witschaduw
        elif v==8: B[y,x]=8
        elif v==7: B[y,x]=7
        elif v==6: B[y,x]=6
        elif v in (9,10): B[y,x]=v
        elif v==5: B[y,x]=12 if sum(q in PANEL for q in n)>=3 else 3
        elif v==2: B[y,x]=11 if inpanel else 2
        else: B[y,x]=v
assert ((A>0)!=(B>0)).sum()==0
flat=[c for i in range(16) for c in PAL[i]]
out=Image.fromarray(B.astype(np.uint8),'P'); out.putpalette(flat)
out.save(os.path.join(H,'sprite.png'),transparency=0)
P0=np.array(PAL0).reshape(16,3); P1=np.array(flat).reshape(16,3)
chg=int((P0[A]!=P1[B]).any(2).sum())
print('pixels met andere kleur',chg,'alpha-diff',int(((A>0)!=(B>0)).sum()),'kleuren',len(np.unique(B)))
from collections import Counter
print('wissels',sorted(Counter((int(a),int(b)) for a,b in zip(A.ravel(),B.ravel()) if a).items()))

def rgb(arr,pal,bg):
    o=np.zeros(arr.shape+(3,),np.uint8)+np.array(bg,np.uint8)
    for i in range(1,16): o[arr==i]=pal[i]
    return Image.fromarray(o)
def rgba(img):
    return img.convert('RGBA')
rgb(B,P1,(235,240,235)).resize((512,512),Image.NEAREST).save(os.path.join(H,'sprite_8x.png'))

# vel
m=Image.open(os.path.join(R,'model','model_gekozen.png')).convert('RGB')
f2=Image.open(os.path.join(R,'..','satelliet_fase2','af','satelliet.png')).convert('RGBA')
refs=[f2]+[Image.open(os.path.join(G,'graphics','pokemon',n,'anim_front_gba.png')).convert('RGBA').crop((0,0,64,64)) for n in ('magneton','metagross')]
vel=Image.new('RGB',(3*532+20,512+40+2*(64*3+20)),(255,255,255)); d=ImageDraw.Draw(vel)
mm=m.crop((3,3,228,3+int(round(42*3.515625)))).resize((512,int(42*3.515625*512/225)),Image.LANCZOS)
mfull=Image.new('RGB',(512,512),(235,240,235)); mfull.paste(mm,(0,13*8))
for i,(im,t) in enumerate(((rgb(A,P0,(235,240,235)).resize((512,512),Image.NEAREST),'r5 8x'),
                            (rgb(B,P1,(235,240,235)).resize((512,512),Image.NEAREST),'r6 8x'),
                            (mfull,'model (verkleind)'))):
    vel.paste(im,(10+i*532,30)); d.text((10+i*532+4,10),t,fill=(0,0,0))
y0=560
r5=Image.fromarray(np.dstack([P0[A],(A>0)*255]).astype(np.uint8),'RGBA')
r6=Image.fromarray(np.dstack([P1[B],(B>0)*255]).astype(np.uint8),'RGBA')
for row,bg in enumerate(((235,240,235),(40,44,60))):
    yy=y0+row*(64*3+20); vel.paste(Image.new('RGB',(3*532,64*3+10),bg),(10,yy))
    x=20
    for im in [r5,r6]+refs:
        vel.paste(im,(x,yy+5),im); x+=72
    x+=20
    for im in [r5,r6]+refs:
        b=im.resize((128,128),Image.NEAREST); vel.paste(b,(x,yy+5),b); x+=136
d.text((20,y0-14),'1x en 2x: r5, r6, fase 2, Magneton, Metagross (licht en donker)',fill=(0,0,0))
vel.save(os.path.join(H,'vel.png'))
