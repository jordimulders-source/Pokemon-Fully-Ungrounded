# vel: r4 | r3 | model (zelfde schrap-schaal) op 8x; poten 12x: r4 | model; 1x licht/donker; verschilkaart
import numpy as np; from PIL import Image, ImageDraw
from reduce_pal import PAL
P=np.array([(255,255,255)]+PAL[1:])
def sp(f,r0,r1,Z): a=P[np.loadtxt(f,dtype=int)[16:62,6:56][r0:r1]].astype('uint8'); return Image.fromarray(a).resize((50*Z,(r1-r0)*Z),Image.NEAREST)
M=Image.open('model_zelfde_schaal.png').convert('RGB')
def mo(r0,r1,Z): return M.crop((0,r0,50,r1)).resize((50*Z,(r1-r0)*Z),Image.NEAREST)
rij=[([sp('vlieg_r4.txt',0,46,8),sp('vlieg_r3.txt',0,46,8),mo(0,46,8)],['r4','r3','model (zelfde schaal)']),
     ([sp('vlieg_r4.txt',21,46,12),mo(21,46,12)],['r4 poten 12x','model'])]
w=max(sum(p.width+20 for p in r) for r,_ in rij); h=sum(r[0].height+24 for r,_ in rij)+420
v=Image.new('RGB',(w,h),'white'); d=ImageDraw.Draw(v); y=0
for r,t in rij:
    x=0
    for p,tt in zip(r,t): v.paste(p,(x,y+16)); d.text((x+2,y+2),tt,fill=(255,0,0)); x+=p.width+20
    y+=r[0].height+24
im=Image.open('vlieg_r4.png'); im.save('/tmp/_v4.png',transparency=0); s=Image.open('/tmp/_v4.png').convert('RGBA')
for k,bg in enumerate([(248,248,248),(40,40,48)]):
    t=Image.new('RGBA',(64,64),bg+(255,)); t.alpha_composite(s)
    v.paste(t.convert('RGB'),(k*80,y+10)); v.paste(t.resize((128,128),Image.NEAREST).convert('RGB'),(180+k*150,y+10))
vd=Image.open('verschil.png'); v.paste(vd,(500,y+16))
d.text((500,y+2),'rood = reparatie t.o.v. kale reductie (potengebied), blauw = extra verre poten, groen = gewijzigd buiten potengebied (moet leeg)',fill=(255,0,0))
v.save('vel.png'); print(v.size)
