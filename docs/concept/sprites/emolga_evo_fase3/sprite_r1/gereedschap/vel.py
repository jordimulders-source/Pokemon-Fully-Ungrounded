# vel.py -> ../vel.png: A0 | A | A_geel | model (zelfde schaal, scherp) | model verkleind (16x16-blokgemiddelde), alles 8x;
# daaronder 1x op licht en donker (en 2x op licht).
import sys; sys.path.insert(0,'/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/emolga_evo_fase3/sprite_r1/gereedschap')
from fv import *; import palet
from PIL import ImageDraw
X0,X1=12,52                              # uitsnede in spritekolommen (figuur x19-44)
def sp(n): return np.asarray(Image.open(D+'sprite_r1/%s.png'%n)).astype(int)
def acht(im): return im.crop((X0,0,X1,64)).resize(((X1-X0)*8,512),Image.NEAREST)
mb=modelblokken().mean(2).astype('uint8'); mverk=Image.fromarray(mb)                       # 64x64 blokgemiddelde
m=Image.open(D+'model/model.png').convert('RGB')
mscherp=m.transform(((X1-X0)*8,512),Image.EXTENT,(X0*16+16,0,X1*16+16,1024),Image.BICUBIC,fillcolor=(255,255,255))
kol=[('A0 (trouw model)',acht(palet.rgb(sp('A0'),(255,255,255)))),('A (C vizier + A kap)',acht(palet.rgb(sp('A'),(255,255,255)))),
     ('A_geel (A + geel vlekje)',acht(palet.rgb(sp('A_geel'),(255,255,255)))),('model, zelfde schaal',mscherp),('model verkleind 64 px',acht(mverk))]
W=(X1-X0)*8; v=Image.new('RGB',(len(kol)*(W+10)+10,512+40+150),'white'); d=ImageDraw.Draw(v)
for i,(t,im) in enumerate(kol): v.paste(im,(10+i*(W+10),24)); d.text((10+i*(W+10),6),t,fill=(0,0,0))
y0=512+40
for i,(n,bron) in enumerate([('A0',None),('A',None),('A_geel',None),('verkleind',mverk)]):
    x=10+i*(W+10)
    for j,bg in enumerate([(232,232,216),(40,48,56)]):
        if bron is None: im=palet.rgb(sp(n),bg)
        else:
            a=np.asarray(bron).copy(); a[(modelblokken().min(-1)>=245).mean(-1)>=0.5]=bg; im=Image.fromarray(a)
        v.paste(im,(x+j*70,y0))
    im2=palet.rgb(sp(n),(232,232,216)) if bron is None else Image.fromarray(np.asarray(bron))
    v.paste(im2.resize((128,128),Image.NEAREST),(x+140,y0)) if W>=268 else None
d.text((10,y0-14),'1x op licht en donker, 2x op licht',fill=(0,0,0))
v.save(D+'sprite_r1/vel.png'); print(v.size)
