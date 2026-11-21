# r20 = r19 p2 zonder het rood gestipte pixel van Jordi (krabbel_jordi_r19.png geregistreerd: schaal 14.94,
# oorsprong (4,17), fout 0.15 -> stipje op spritepixel (28,44): omlijning van de middenpoot die tegen de
# knieband van de nabije voorpoot plakt). Wordt transparant, zodat de twee poten los van elkaar staan.
import sys; sys.path.insert(0,'sprite_r14')
from lib import *
im=Image.open('sprite_r19/vlieg_r19_p2.png'); b=im.load()
b[28,44]=0
im.save('sprite_r20/vlieg_r20.png',transparency=0)
onbg(im).resize((512,512),Image.NEAREST).save('sprite_r20/vlieg_r20_8x.png')
v=Image.open('sprite_r19/vlieg_r19_p2.png'); bx=(18,38,36,50)
t=[zoom(v,bx,12,False),zoom(im,bx,12,False)]
c=Image.new('RGB',(t[0].width*2+10,t[0].height+18),'white')
for i,m in enumerate(t): c.paste(m,(i*(m.width+10),18))
d=ImageDraw.Draw(c); d.text((4,3),'voor (r19 p2), 12x',fill=(0,0,0)); d.text((t[0].width+14,3),'na (r20)',fill=(0,0,0))
c.save('sprite_r20/voor_na_12x.png')
a=v.load(); print('diff',[(x,y) for x in range(64) for y in range(64) if a[x,y]!=b[x,y]])
