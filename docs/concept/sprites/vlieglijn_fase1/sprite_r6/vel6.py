# vel: A1 | A2 | r9 (natief, zelfde schaal) | r5 B op 8x; poten 12x (A1, A2, r9 1024px-uitsnede); 1x licht/donker
import numpy as np; from PIL import Image, ImageDraw
PAL=[(255,255,255)]+[tuple(map(int,l.split())) for l in open('normal.pal').read().split('\n')[4:19]]
P=np.array(PAL)
def sp(t,y0,y1,x0,x1,Z): a=P[np.loadtxt(t,dtype=int)[y0:y1,x0:x1]].astype('uint8'); return Image.fromarray(a).resize(((x1-x0)*Z,(y1-y0)*Z),Image.NEAREST)
r9=Image.open('../gemini/r9.png').convert('RGB')
def g(y0,y1,x0,x1,Z): return r9.crop((x0*16,y0*16,x1*16,y1*16)).resize(((x1-x0)*Z,(y1-y0)*Z),Image.LANCZOS)
R1=[sp('vlieg_r6_A1.txt',14,63,4,58,8),sp('vlieg_r6_A2.txt',14,63,4,58,8),g(14,63,4,58,8),sp('../sprite_r5/vlieg_r5_B.txt',14,63,4,58,8)]
T1=['A1 (+4,-4)','A2 (+5,-4)','Gemini r9 (zelfde schaal)','r5 B']
R2=[sp('vlieg_r6_A1.txt',38,62,6,54,12),sp('vlieg_r6_A2.txt',38,62,6,54,12),g(38,62,6,54,12)]; T2=['A1 poten 12x','A2 poten 12x','r9 poten 12x']
w=max(sum(p.width+16 for p in R1),R2[0].width*2+32); h=R1[0].height+20+2*(R2[0].height+20)+110
v=Image.new('RGB',(w,h),'white'); d=ImageDraw.Draw(v); x=0
for p,t in zip(R1,T1): v.paste(p,(x,14)); d.text((x+2,0),t,fill=(255,0,0)); x+=p.width+16
y=R1[0].height+20
for i,(p,t) in enumerate(zip(R2,T2)):
    xx=(i%2)*(p.width+16); yy=y+(i//2)*(p.height+20); v.paste(p,(xx,yy+14)); d.text((xx+2,yy),t,fill=(255,0,0))
y0=y+2*(R2[0].height+20)
for k,n in enumerate(('A1','A2')):
    im=Image.open(f'vlieg_r6_{n}.png').convert('RGBA')   # P met transparency-index -> alfa klopt
    for j,bg in enumerate([(248,248,248),(40,40,48)]):
        t=Image.new('RGBA',(64,64),bg+(255,)); t.alpha_composite(im); xx=R2[0].width+32+k*170+j*80
        v.paste(t.convert('RGB'),(xx,y0-R2[0].height+40)); d.text((xx,y0-R2[0].height+26),n,fill=(255,0,0))
v.save('vel.png'); print(v.size)
