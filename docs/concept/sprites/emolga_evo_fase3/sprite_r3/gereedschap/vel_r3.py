# vel_r3.py: vel.png = r3 | r2 | model verkleind (8x, x16-48) + 1x licht/donker en 2x; voor A0 en A.
import sys; sys.path.insert(0,'/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/emolga_evo_fase3/sprite_r3/gereedschap')
from fv import *; import palet
from PIL import ImageDraw
LICHT,DONKER=(232,232,216),(40,48,56)
def lees(p): return np.asarray(Image.open(p)).astype(int)
m=Image.open(D+'model/model.png').convert('RGB'); c=Image.new('RGB',(1024,1024),'white'); c.paste(m.crop((16,0,1024,1024)),(0,0)); m64=c.resize((64,64),Image.BOX)
kol=[('r3 A0','sprite_r3/A0'),('r2 A0','sprite_r2/A0'),('r3 A','sprite_r3/A'),('r2 A','sprite_r2/A'),('r3 A_geel','sprite_r3/A_geel'),('model verkleind',None)]
x0,x1,z=16,48,8; W=(x1-x0)*z+12
v=Image.new('RGB',(W*len(kol),64*z+20+140),'white'); d=ImageDraw.Draw(v)
for i,(nm,p) in enumerate(kol):
    im=palet.rgb(lees(D+p+'.png'),LICHT) if p else m64
    v.paste(im.crop((x0,0,x1,64)).resize(((x1-x0)*z,64*z),Image.NEAREST),(i*W,18)); d.text((i*W,3),nm,fill=(0,0,0))
    if p:
        o=lees(D+p+'.png')
        for j,bg in enumerate((LICHT,DONKER)): v.paste(palet.rgb(o,bg),(i*W+j*68,64*z+24))
        v.paste(palet.rgb(o,LICHT).resize((128,128),Image.NEAREST),(i*W+136,64*z+24))
v.save(D+'sprite_r3/vel.png'); print('ok')
