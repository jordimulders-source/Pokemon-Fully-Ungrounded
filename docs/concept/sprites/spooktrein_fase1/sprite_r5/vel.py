# vel r5: r5 8x | r4 8x | model op dezelfde maat 8x; daaronder r5 en r4 1x/2x op licht en donker, model 1x/2x
import numpy as np; from PIL import Image, ImageDraw
from toon import rgba
o=np.load('raw.npy'); np.save('sprite.npy',o)
sp=rgba(o); r4=rgba(np.load('../sprite_r4/sprite.npy'))
sp.save('sprite.png'); w=Image.new('RGB',(64,64),'white'); w.paste(sp,(0,0),sp); w.resize((512,512),Image.NEAREST).save('sprite_8x.png')
m=Image.open('../model/model.png').convert('RGB'); a=np.asarray(m); fg=a.min(2)<225; ys,xs=np.where(fg)
ref=Image.new('RGB',(64,64),'white'); ref.paste(m.crop((xs.min(),ys.min(),xs.max()+1,ys.max()+1)).resize((51,44),Image.LANCZOS),(6,19))
def on(s,bg): return Image.alpha_composite(Image.new('RGBA',(64,64),bg),s).convert('RGB')
C=(0,120,512,512)
V=Image.new('RGB',(3*512+4*16,392+16+40+150),(236,236,236)); d=ImageDraw.Draw(V)
for i,(im,t) in enumerate(((on(sp,(255,255,255,255)),'r5'),(on(r4,(255,255,255,255)),'r4'),(ref,'model op dezelfde maat'))):
    V.paste(im.resize((512,512),Image.NEAREST).crop(C),(16+i*528,24)); d.text((16+i*528,8),t+' 8x',fill=(0,0,0))
y=24+392+30; x=16
for s,t in ((sp,'r5'),(r4,'r4')):
    d.text((x,y-16),t+' 1x/2x licht, donker',fill=(0,0,0))
    for bg in ((255,255,255),(40,44,60)):
        V.paste(on(s,bg+(255,)),(x,y)); V.paste(on(s,bg+(255,)).resize((128,128),Image.NEAREST),(x+72,y)); x+=216
V.paste(ref,(x,y)); V.paste(ref.resize((128,128),Image.NEAREST),(x+72,y)); d.text((x,y-16),'model 1x/2x',fill=(0,0,0))
V.save('vel.png')
