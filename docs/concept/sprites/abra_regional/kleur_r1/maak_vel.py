# vel.png: sprite 8x | model op dezelfde schaal (8x) | sprite 1x op licht en donker (ook 2x)
from PIL import Image, ImageDraw; import numpy as np
im=Image.open('abra_r1.png').convert('RGBA')   # opgeslagen met transparency=0, dus alfa klopt
def op(img,kl):
    b=Image.new('RGBA',img.size,kl); b.alpha_composite(img); return b.convert('RGB')
s8=op(im,(255,255,255,255)).resize((512,512),Image.NEAREST); s8.save('abra_r1_8x.png') if False else None
im.resize((512,512),Image.NEAREST).save('abra_r1_8x.png')
m=Image.open('../referenties/gemini_gekozen.png').convert('RGB')
g=np.asarray(m).min(2); ys,xs=np.where(g<215)
mb=(xs.min(),ys.min(),xs.max()+1,ys.max()+1)
sb=im.getbbox()   # sprite bbox in 1x
sc=512/64*(sb[2]-sb[0])/((mb[2]-mb[0]))  # model px -> vel px
mm=m.crop(mb).resize((round((mb[2]-mb[0])*sc),round((mb[3]-mb[1])*sc)),Image.LANCZOS)
mv=Image.new('RGB',(512,512),'white'); mv.paste(mm,(sb[0]*8,sb[3]*8-mm.height))
klein=Image.new('RGB',(512,512),(200,200,200))
for k,(kl) in enumerate([(248,248,248,255),(40,40,48,255),(144,200,144,255)]):
    klein.paste(op(im,kl),(16+k*80,16)); klein.paste(op(im,kl).resize((128,128),Image.NEAREST),(16+k*164,120))
v=Image.new('RGB',(512*3+40,560),'white'); d=ImageDraw.Draw(v)
for k,(x,t) in enumerate(((s8,'abra_r1 8x'),(mv,'model, zelfde schaal'),(klein,'1x en 2x op licht/donker'))):
    v.paste(x,(k*532,40)); d.text((k*532+8,12),t,fill=(0,0,0))
v.save('vel.png')
