# vel: A | B | C | model (zelfde schaal) op 8x; achterste poten 12x per variant + model; 1x licht/donker
import numpy as np; from PIL import Image, ImageDraw
from reduce_pal import PAL
P=np.array([(255,255,255)]+PAL[1:])
def sp(n,y0,y1,x0,x1,Z): a=P[np.loadtxt(f'vlieg_r5_{n}.txt',dtype=int)[y0:y1,x0:x1]].astype('uint8'); return Image.fromarray(a).resize(((x1-x0)*Z,(y1-y0)*Z),Image.NEAREST)
M=Image.new('RGB',(64,64),'white'); M.paste(Image.open('model_zelfde_schaal.png').convert('RGB'),(6,16))
def mo(y0,y1,x0,x1,Z): return M.crop((x0,y0,x1,y1)).resize(((x1-x0)*Z,(y1-y0)*Z),Image.NEAREST)
R1=[sp(n,14,63,4,58,8) for n in 'ABC']+[mo(14,63,4,58,8)]; T1=['A (+3,-2)','B (-2,-2)','C (+4,-3)','model']
R2=[sp(n,38,63,24,56,12) for n in 'ABC']+[mo(38,63,24,56,12)]; T2=['A achterpoten 12x','B','C','model']
w=max(sum(p.width+16 for p in R) for R in (R1,)) ; w=max(w,2*(R2[0].width+16))
v=Image.new('RGB',(w,R1[0].height+2*(R2[0].height+20)+200),'white'); d=ImageDraw.Draw(v); y=0; x=0
for p,t in zip(R1,T1): v.paste(p,(x,y+14)); d.text((x+2,y),t,fill=(255,0,0)); x+=p.width+16
y+=R1[0].height+20
for i,(p,t) in enumerate(zip(R2,T2)):
    xx=(i%2)*(p.width+16); yy=y+(i//2)*(p.height+20); v.paste(p,(xx,yy+14)); d.text((xx+2,yy),t,fill=(255,0,0))
y+=2*(R2[0].height+20)
for k,n in enumerate('ABC'):
    im=Image.open(f'vlieg_r5_{n}.png').convert('RGBA')
    for j,bg in enumerate([(248,248,248),(40,40,48)]):
        t=Image.new('RGBA',(64,64),bg+(255,)); t.alpha_composite(im); xx=k*300+j*140
        v.paste(t.convert('RGB'),(xx,y+20)); v.paste(t.resize((128,128),Image.NEAREST).convert('RGB'),(xx,y+90)) if False else None
        d.text((xx,y+4),n,fill=(255,0,0))
v.save('vel.png'); print(v.size)
