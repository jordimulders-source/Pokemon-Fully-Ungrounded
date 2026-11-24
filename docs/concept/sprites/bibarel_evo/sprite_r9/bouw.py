# bouw.py ronde 9 (vanaf r8): alleen tinten herverdelen binnen het crème van rij 45-53 (keuring r8: banding onderbuik).
# Draaien vanuit docs/concept/sprites/bibarel_evo:  python3 sprite_r9/bouw.py
# 1) grens licht/midden bolle curve (kern op r46-47 tot x31, dan snel terug); 2) middentint stopt op r50;
# 3) tan onderin als sikkel die breder wordt; 4) donkerste crème alleen in de onderste rechterhoek (r50-53).
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage
im8=Image.open('sprite_r8/sprite.png'); PAL=np.array(im8.getpalette()[:48]).reshape(16,3).astype('uint8')
r8=np.asarray(im8).astype(int); o=r8.copy()
C,M,S,D=7,10,6,15; CR=(C,M,S,D)
#        rij: (laatste licht, laatste midden, eerste donker)  -> licht t/m a, midden t/m b, tan tot c, donker vanaf c
PLAN={45:(30,36,99),46:(31,35,99),47:(31,35,99),48:(30,34,99),49:(27,32,99),50:(24,28,35),51:(23,0,34),52:(0,0,33),53:(0,0,33)}
for y,(a,b,c) in PLAN.items():
    for x in range(64):
        if r8[y,x] not in CR: continue
        o[y,x]=C if x<=a else (M if x<=b else (D if x>=c else S))
# geen vlakjes < 3 px in het crème
R=np.zeros((64,64),bool); R[45:55,19:46]=True   # onderbuik
for k in CR:
    lab,n=ndimage.label((o==k)&R)
    for i in range(1,n+1):
        assert (lab==i).sum()>=3,('vlakje',k,np.argwhere(lab==i)[0][::-1])
def save(idx,pad,z=None):
    im=Image.new('P',(64,64)); im.putpalette(PAL.ravel().tolist()+[0]*3*240)
    im.putdata(idx.astype('uint8').ravel().tolist()); im.save(pad,transparency=0)
    if z: Image.fromarray(PAL[idx]).resize((64*z,64*z),Image.NEAREST).save(pad.replace('.png',f'_{z}x.png'))
save(o,'sprite_r9/sprite.png',8)
dd=np.argwhere(o!=r8)
print('gewijzigd:',len(dd),'| buiten r45-53:',[(int(x),int(y)) for y,x in dd if not 45<=y<=53],
      '| niet-crème geraakt:',int(sum(r8[y,x] not in CR for y,x in dd)),'| silhouet gelijk:',((o>0)==(r8>0)).all())
for y in range(45,54):
    row={k:[x for x in range(64) if o[y,x]==k] for k in CR}
    print(y,' '.join(f"{n}:{min(v)}-{max(v)}" for n,v in zip('kmhd',row.values()) if v))
# vel: r9 | r8 (8x), buik 12x, 1x licht/donker
V=Image.new('RGB',(1060,1000),'white'); d=ImageDraw.Draw(V)
big=lambda idx,z,box=None:(lambda im:im.resize((im.width*z,im.height*z),Image.NEAREST))(Image.fromarray(PAL[idx]).crop(box) if box else Image.fromarray(PAL[idx]))
for i,(idx,t) in enumerate([(o,'r9'),(r8,'r8')]):
    V.paste(big(idx,8),(10+i*522,30)); d.text((10+i*522,10),t+' 8x',fill='black')
bb=(16,42,46,57)
for i,(idx,t) in enumerate([(o,'buik r9 12x'),(r8,'buik r8 12x')]):
    V.paste(big(idx,12,bb),(10+i*375,580)); d.text((10+i*375,562),t,fill='black')
for j,bg in enumerate([(248,248,248),(40,40,48)]):
    for i,idx in enumerate((o,r8)):
        t=Image.new('RGB',(64,64),bg); t.paste(Image.fromarray(PAL[idx]),(0,0),Image.fromarray(((idx>0)*255).astype('uint8'))); V.paste(t,(800+i*80,580+j*80))
d.text((800,562),'1x: r9, r8',fill='black')
V.crop((0,0,1060,780)).save('sprite_r9/vel.png')
