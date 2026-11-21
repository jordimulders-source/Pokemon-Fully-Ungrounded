# vel: r9 | r8 op 8x; poten 12x r9 | r8; 1x licht/donker
import numpy as np; from PIL import Image, ImageDraw
PAL=[(255,255,255)]+[tuple(map(int,l.split())) for l in open('normal.pal').read().split('\n')[4:19]]; P=np.array(PAL)
def sp(t,y0,y1,x0,x1,Z): a=P[np.loadtxt(t,dtype=int)[y0:y1,x0:x1]].astype('uint8'); return Image.fromarray(a).resize(((x1-x0)*Z,(y1-y0)*Z),Image.NEAREST)
R1=[sp('vlieg_r9.txt',14,63,4,58,8),sp('../sprite_r8/vlieg_r8.txt',14,63,4,58,8)]
R2=[sp('vlieg_r9.txt',38,62,24,52,12),sp('../sprite_r8/vlieg_r8.txt',38,62,24,52,12)]
w=2*(R1[0].width+16); h=R1[0].height+R2[0].height+170
v=Image.new('RGB',(w,h),'white'); d=ImageDraw.Draw(v)
for i,(p,t) in enumerate(zip(R1,['r9','r8'])): v.paste(p,(i*(p.width+16),14)); d.text((i*(p.width+16)+2,0),t,fill=(255,0,0))
y=R1[0].height+30
for i,(p,t) in enumerate(zip(R2,['r9 poten 12x','r8 poten 12x'])): v.paste(p,(i*(R1[0].width+16),y+14)); d.text((i*(R1[0].width+16)+2,y),t,fill=(255,0,0))
y+=R2[0].height+50; im=Image.open('vlieg_r9.png').convert('RGBA')
for j,bg in enumerate([(248,248,248),(40,40,48)]):
    t=Image.new('RGBA',(64,64),bg+(255,)); t.alpha_composite(im); v.paste(t.convert('RGB'),(j*80,y)); d.text((j*80,y-12),'r9 1x',fill=(255,0,0))
v.save('vel.png'); print(v.size)
