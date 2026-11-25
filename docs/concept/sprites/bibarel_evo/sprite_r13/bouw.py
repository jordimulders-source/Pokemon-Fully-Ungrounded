# bouw.py ronde 13 (vanaf sprite_r12). Jordi 24 nov: "de bollen links opnieuw getekend ipv gewoon bollen zoals in het model,
# de klep van de helm mag net iets breder" + "het is niet erg als die klep een klein beetje overlapt".
# Draaien vanuit docs/concept/sprites/bibarel_evo:  python3 sprite_r13/bouw.py
import numpy as np, sys
from PIL import Image, ImageDraw
sys.path.insert(0,'sprite_r13'); from reductie import red, MK   # oppervlaktegewogen reductie van model/r10_k8.png, lijnweging: donkerste wint bij >=25% lijn
im12=Image.open('sprite_r12/sprite.png'); PAL=np.array(im12.getpalette()[:48]).reshape(16,3).astype('uint8')
r12=np.asarray(im12).astype(int); r11=np.asarray(Image.open('sprite_r11/sprite.png')).astype(int)
o=r12.copy(); herkomst={}
# 1. linker kraagbollen = reductie van het model (x16-20, r16-23; x21 = oogring/snuit, blijft)
AL=[1,2,3,4,5,8,9]                      # K b c d f e L
DONKER={1,8,9}
for y in range(16,24):
    for x in range(16,21):
        v,_=red(x,y,AL)
        if v in DONKER and x<=17:        # model: hand/stam (donker) -> hand van r11 terug (mijn getekende r12-randpixels weg)
            o[y,x]=r11[y,x]; herkomst[(x,y)]='hand r11'
        elif v in (8,9):                 # e/L binnen de kraag = lijn -> lijn in eigen donkere tint (b)
            o[y,x]=2; herkomst[(x,y)]='reductie %s -> b (reparatie)'%('e' if v==8 else 'L')
        else:
            o[y,x]=v; herkomst[(x,y)]='reductie'
# 2. klep iets breder, zelfde boog (uiteinden stijgen), steekt links 1 px over de rand
KLEP={(19,12):2,(20,12):3,(19,13):3,(35,12):2}
for p,v in KLEP.items(): o[p[1],p[0]]=v
def save(idx,pad,z=None):
    im=Image.new('P',(64,64)); im.putpalette(PAL.ravel().tolist()+[0]*3*240)
    im.putdata(idx.astype('uint8').ravel().tolist()); im.save(pad,transparency=0)
    if z: Image.fromarray(PAL[idx]).resize((64*z,64*z),Image.NEAREST).save(pad.replace('.png',f'_{z}x.png'))
save(o,'sprite_r13/sprite.png',8)
ch='.KbcdfSCeLMogWwD'
dd=[(int(x),int(y)) for y,x in np.argwhere(o!=r12)]
inz=lambda x,y:(16<=x<=20 and 16<=y<=23) or (x,y) in KLEP
print('gewijzigd:',len(dd),'| buiten zones:',[p for p in dd if not inz(*p)],'| silhouet extra:',[(int(x),int(y)) for y,x in np.argwhere((o>0)&~(r12>0))])
for y in range(16,24): print(y,''.join(ch[o[y,x]] for x in range(16,21)),'  ',' | '.join(f'{x}:{herkomst[(x,y)]}' for x in range(16,21)))
for y in (12,13,14,15):
    run=mx=0
    for x in range(17,40): run=run+1 if o[y,x]==2 else 0; mx=max(mx,run)
    print('klep rij',y,'langste lijnrun',mx)
# vel: r13 | r12 (8x); links: model-uitsnede | r12 | r13 (12x); klep 12x
fig=np.load('sprite_r1/masker.npy'); yy,xx=np.where(fig); MKi=MK.astype('uint8'); mx0,my0=xx.min(),yy.min(); s_=64/(xx.max()-mx0+1); oy=64-round((yy.max()-my0+1)*s_)
def modelvak(x0,y0,x1,y1,Z):
    W,H=(x1-x0)*Z,(y1-y0)*Z; out=np.full((H,W,3),255,'uint8')
    py,px=np.mgrid[0:H,0:W]; X=(mx0+(x0+px/Z)/s_).astype(int); Y=(my0+(y0+py/Z-oy)/s_).astype(int)
    ok=(X>=0)&(X<99)&(Y>=0)&(Y<99); out[ok]=MKi[Y[ok],X[ok]]; return Image.fromarray(out)
big=lambda idx,z,box=(0,0,64,64):Image.fromarray(PAL[idx]).crop(box).resize(((box[2]-box[0])*z,(box[3]-box[1])*z),Image.NEAREST)
V=Image.new('RGB',(1300,1400),'white'); d=ImageDraw.Draw(V)
for i,(idx,t) in enumerate([(o,'r13'),(r12,'r12')]):
    V.paste(big(idx,8),(10+i*522,30)); d.text((10+i*522,10),t+' 8x',fill='black')
y0=580; lb=(12,13,26,27)
for i,(img,t) in enumerate([(modelvak(*lb,12),'model (r10_k8) 12x'),(big(r12,12,lb),'r12 12x'),(big(o,12,lb),'r13 12x')]):
    X0=10+i*190; V.paste(img,(X0,y0+20)); d.text((X0,y0),t,fill='black')
    dr=ImageDraw.Draw(V); dr.rectangle([X0+(16-lb[0])*12,y0+20+(16-lb[1])*12,X0+(21-lb[0])*12-1,y0+20+(24-lb[1])*12-1],outline=(0,90,255))
y0+=200; kb=(15,5,43,18)
for i,(img,t) in enumerate([(modelvak(*kb,12),'model klep 12x'),(big(r12,12,kb),'klep r12 12x'),(big(o,12,kb),'klep r13 12x')]):
    X0=10+i*350; V.paste(img,(X0,y0+20)); d.text((X0,y0),t,fill='black')
y0+=190
for j,bg in enumerate([(248,248,248),(40,40,48)]):
    for i,idx in enumerate((o,r12)):
        t=Image.new('RGB',(64,64),bg); t.paste(Image.fromarray(PAL[idx]),(0,0),Image.fromarray(((idx>0)*255).astype('uint8'))); V.paste(t,(10+i*80,y0+20+j*80))
d.text((10,y0),'1x: r13, r12',fill='black')
V.crop((0,0,1300,y0+190)).save('sprite_r13/vel.png')
