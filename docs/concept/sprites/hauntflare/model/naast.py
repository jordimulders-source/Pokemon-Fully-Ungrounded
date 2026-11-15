# Zet de modellen naast elkaar (6x, met naam)
from PIL import Image, ImageDraw, ImageFont
f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',26)
L=[('model_claude_natief.png','Claude'),('model_jordi_natief.png','Jordi')]
S=6; w=99*S; v=Image.new('RGB',(2*w+60,w+60),'white'); d=ImageDraw.Draw(v)
for i,(n,t) in enumerate(L):
    im=Image.open('model/'+n).resize((w,w),Image.NEAREST); x=20+i*(w+20)
    v.paste(im,(x,50)); d.text((x+w//2,25),t,fill='black',font=f,anchor='mm')
v.save('model/naast_elkaar.png')
