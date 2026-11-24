# vel.png: sprite | samengesteld model geschrapt op 1x | beide op 8x | gezicht 12x (sprite, model) | 1x op licht en donker
import sys, numpy as np; from PIL import Image, ImageDraw
sys.path.insert(0,'claydol_sprite_r1'); from klassen import klasse
from bouw import RIJEN,KOLOMMEN
k,a=klasse()
am=np.delete(np.delete(a,RIJEN,0),KOLOMMEN,1); km=np.delete(np.delete(k,RIJEN,0),KOLOMMEN,1)
ys,xs=np.where(km>0); am=am[ys.min():ys.max()+1,xs.min():xs.max()+1]; km=km[ys.min():ys.max()+1,xs.min():xs.max()+1]
h,w=km.shape; M=np.zeros((64,64,4),'uint8'); M[64-h:,(64-w)//2:(64-w)//2+w,:3]=am; M[64-h:,(64-w)//2:(64-w)//2+w,3]=np.where(km>0,255,0)
model=Image.fromarray(M,'RGBA')
sp=Image.open('claydol_sprite_r1/claydol_r1.png').convert('RGBA')
def op(im,bg,s=1):
    c=Image.new('RGBA',im.size,bg); c.alpha_composite(im); c=c.convert('RGB'); return c.resize((im.width*s,im.height*s),Image.NEAREST)
V=Image.new('RGB',(64*8*2+60,20+64*8+20+30*12+20+80),(236,236,236)); d=ImageDraw.Draw(V)
d.text((10,4),'claydol_r1 (sprite)   |   samengesteld model, geschrapt, 1x   |   8x',fill='black')
V.paste(op(sp,(255,255,255)),(10,20)); V.paste(op(model,(255,255,255)),(84,20))
y8=96; V.paste(op(sp,(255,255,255),8),(10,y8)); V.paste(op(model,(255,255,255),8),(10+512+40,y8))
yg=y8+512+20; box=(10,18,50,42)
V.paste(op(sp.crop(box),(255,255,255),12),(10,yg)); V.paste(op(model.crop(box),(255,255,255),12),(10+480+40,yg))
d.text((10,yg-14),'gezicht 12x: sprite | model',fill='black')
yl=yg+24*12+20
for i,bg in enumerate([(248,248,240),(200,224,248),(40,40,48),(24,64,40)]):
    V.paste(op(sp,bg),(10+i*74,yl))
V=V.crop((0,0,V.width,yl+72)); V.save('claydol_sprite_r1/vel.png')
op(sp,(255,255,255),8).save('claydol_sprite_r1/claydol_r1_8x.png')
# bovenaan: het samengestelde model zelf (natief, 5x) naast r5 / r3 / r6 als bron
from PIL import ImageDraw as _D
bronnen=[('samengesteld model','claydol_model/model_natief_samengesteld.png'),('r5 (basis)','claydol_model/natief_r5.png'),('r3 (oogafwerking)','claydol_model/natief_r3.png'),('r6 (stipjes)','claydol_model/natief_r6.png')]
tops=[Image.open(p).convert('RGB').crop((10,9,89,86)).resize((79*5 if i==0 else 79*3,77*5 if i==0 else 77*3),Image.NEAREST) for i,(n,p) in enumerate(bronnen)]
Wt=max(V.width,sum(t.width for t in tops)+50); top=Image.new('RGB',(Wt,77*5+30),(236,236,236)); dd=_D.Draw(top); x=10
for (n,_),t in zip(bronnen,tops): top.paste(t,(x,22)); dd.text((x,6),n,fill='black'); x+=t.width+10
U=Image.new('RGB',(Wt,top.height+V.height),(236,236,236)); U.paste(top,(0,0)); U.paste(V,(0,top.height)); U.save('claydol_sprite_r1/vel.png')
