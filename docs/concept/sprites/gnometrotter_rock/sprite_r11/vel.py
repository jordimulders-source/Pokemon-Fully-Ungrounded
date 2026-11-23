# vel.py: r11 | r10 | model op 8x; daaronder 1x en 2x naast Gnomad
from PIL import Image, ImageDraw
D='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/'
r11=Image.open('gnometrotter_rock.png').convert('RGBA'); r10=Image.open('../sprite_r10/gnometrotter_rock.png').convert('RGBA'); gd=Image.open(D+'gnomad/af/gnomad.png').convert('RGBA')
m=Image.open('../r8/gemini_r8.png').convert('RGB'); x0=512+(0-32)*8.1; y0=523-60*8.1
m=m.crop((int(x0),int(y0),int(x0+64*8.1),int(y0+64*8.1))).resize((512,512),Image.LANCZOS)
r11.resize((512,512),0).save('gnometrotter_rock_8x.png')
W=Image.new('RGB',(3*522,512+200),(152,208,160)); d=ImageDraw.Draw(W)
for i,(im,t) in enumerate([(r11.resize((512,512),0),'r11'),(r10.resize((512,512),0),'r10'),(m,'model r8')]):
    W.paste(im,(i*522,0)); d.text((i*522+4,4),t,fill=(0,0,0))
x=10
for im in (r11,gd): W.paste(im,(x,540)); x+=74
for im in (r11,gd): W.paste(im.resize((128,128),0),(x,540)); x+=138
d.text((10,520),'1x: r11, Gnomad    2x: r11, Gnomad',fill=(0,0,0))
W.save('vel.png')
