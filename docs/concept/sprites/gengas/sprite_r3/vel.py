# vel.py ronde 3: wervel 12x (r3 | r2 | model) + sprite 8x (alleen weergave)
from PIL import Image, ImageDraw
def wit(p):
    i=Image.open(p).convert('RGBA'); b=Image.new('RGBA',i.size,(255,255,255,255)); b.alpha_composite(i); return b
r3,r2,k=wit('gengas_r3.png'),wit('../sprite_r2/gengas_r2.png'),wit('../model/kleurgids_64.png')
box=(33,29,51,43); S=12; w,h=(box[2]-box[0])*S,(box[3]-box[1])*S
V=Image.new('RGBA',(3*w+40,h+560),(235,235,235,255)); d=ImageDraw.Draw(V)
for i,(im,t) in enumerate([(r3,'r3'),(r2,'r2'),(k,'model')]):
    V.paste(im.crop(box).resize((w,h),Image.NEAREST),(10+i*(w+10),22)); d.text((10+i*(w+10),6),'wervel 12x: '+t,fill=(0,0,0))
d.text((10,h+30),'r3 8x',fill=(0,0,0)); V.paste(r3.resize((512,512),Image.NEAREST),(10,h+44))
V.save('vel.png'); print(V.size)
