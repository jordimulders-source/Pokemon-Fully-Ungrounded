# vel_r2.py: vel.png (r2 A0 | r2 A | r1 A0 | model verkleind, 8x; daaronder 1x licht/donker) en kop_probeersels.png (P1-P3 op 8x + 1x).
import sys; sys.path.insert(0,'/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/emolga_evo_fase3/sprite_r2/gereedschap')
from fv import *; import palet, kijk, bouw_r2 as b
from PIL import ImageDraw
LICHT,DONKER=(232,232,216),(40,48,56)
def lees(p): return np.asarray(Image.open(p)).astype(int)
def model64():
    m=Image.open(D+'model/model.png').convert('RGB'); c=Image.new('RGB',(1024,1024),'white'); c.paste(m.crop((16,0,1024,1024)),(0,0))
    return c.resize((64,64),Image.BOX)
x0,x1=16,48; z=8
kol=[('r2 A0',palet.rgb(lees(D+'sprite_r2/A0.png'),LICHT)),('r2 A (gekozen kap P1)',palet.rgb(lees(D+'sprite_r2/A.png'),LICHT)),
     ('r2 A_geel',palet.rgb(lees(D+'sprite_r2/A_geel.png'),LICHT)),('r1 A0',palet.rgb(lees(D+'sprite_r1/A0.png'),LICHT)),('model verkleind',model64())]
W=(x1-x0)*z+16; v=Image.new('RGB',(W*len(kol),64*z+20+150),'white'); d=ImageDraw.Draw(v)
for i,(nm,im) in enumerate(kol):
    v.paste(im.crop((x0,0,x1,64)).resize(((x1-x0)*z,64*z),Image.NEAREST),(i*W,18)); d.text((i*W,3),nm,fill=(0,0,0))
    if i<4:
        o=lees(D+'sprite_%s/%s.png'%(('r2','A0'),('r2','A'),('r2','A_geel'),('r1','A0'))[i])
        for j,bg in enumerate((LICHT,DONKER)): v.paste(palet.rgb(o,bg),(i*W+j*70,64*z+26))
        v.paste(palet.rgb(o,LICHT).resize((128,128),Image.NEAREST),(i*W+140,64*z+26))
v.save(D+'sprite_r2/vel.png')
# kop-probeersels
basis=b.zet(b.zet(b.A1,b.VLEUGEL),b.wang('W3'))
kx0,ky0,kx1,ky1=18,40,40,56
items=[('r1 A',b.A1),('P1 (gekozen)',b.kap(basis,'P1',False)),('P2',b.kap(basis,'P2',False)),('P3',b.kap(basis,'P3',False))]
W=(kx1-kx0)*z+16; v=Image.new('RGB',(W*5,(ky1-ky0)*z+20+150),'white'); d=ImageDraw.Draw(v)
for i,(nm,o) in enumerate(items):
    v.paste(palet.rgb(o[ky0:ky1,kx0:kx1],LICHT).resize(((kx1-kx0)*z,(ky1-ky0)*z),Image.NEAREST),(i*W,18)); d.text((i*W,3),nm,fill=(0,0,0))
    for j,bg in enumerate((LICHT,DONKER)): v.paste(palet.rgb(o,bg),(i*W+j*70,(ky1-ky0)*z+26))
v.paste(kijk.modelblok(16,kx0,ky0,kx1,ky1,z),(4*W,18)); d.text((4*W,3),'model',fill=(0,0,0))
v.save(D+'sprite_r2/kop_probeersels.png')
print('ok')
