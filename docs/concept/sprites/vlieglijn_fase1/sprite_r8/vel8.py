# vel: krabbel-overlay op r9 (8x) | r8 | r7_B (8x); poten 12x r8 naast r9; 1x licht/donker
import numpy as np; from PIL import Image, ImageDraw
PAL=[(255,255,255)]+[tuple(map(int,l.split())) for l in open('normal.pal').read().split('\n')[4:19]]; P=np.array(PAL)
k=np.asarray(Image.open('../sprite_r7/krabbel_jordi.png').convert('RGB')).astype(int)
R,G,B=k[...,0],k[...,1],k[...,2]; geel=(R>180)&(G>160)&(B<90); rood=(R>170)&(G<80)&(B<80); s,ox,oy=5.02,2.9,14.9
def sp(t,y0,y1,x0,x1,Z): a=P[np.loadtxt(t,dtype=int)[y0:y1,x0:x1]].astype('uint8'); return Image.fromarray(a).resize(((x1-x0)*Z,(y1-y0)*Z),Image.NEAREST)
def overlay(im,x0,y0,Z):
    d=ImageDraw.Draw(im)
    for mk,col in ((rood,(255,0,0)),(geel,(240,210,0))):
        ys,xs=np.where(mk)
        for y,x in zip(ys,xs): X,Y=(x/s+ox-x0)*Z,(y/s+oy-y0)*Z; d.rectangle((X-1,Y-1,X+1,Y+1),fill=col)
    return im
r9=Image.open('../gemini/r9.png').convert('RGB')
R1=[overlay(sp('../sprite_r6/r9_nat_idx.txt',14,63,4,58,8),4,14,8),sp('vlieg_r8.txt',14,63,4,58,8),sp('../sprite_r7/vlieg_r7_B.txt',14,63,4,58,8)]
T1=['krabbel (geel/rood) op r9 natief','r8','r7_B']
R2=[overlay(sp('vlieg_r8.txt',38,62,20,54,12),20,38,12),sp('vlieg_r8.txt',38,62,20,54,12),r9.crop((20*16,38*16,54*16,62*16)).resize((34*12,24*12),Image.LANCZOS)]
T2=['r8 poten 12x + rood/geel','r8 poten 12x','r9 poten 12x']
w=sum(p.width+16 for p in R1); h=R1[0].height+R2[0].height+60+110
v=Image.new('RGB',(w,h),'white'); d=ImageDraw.Draw(v); x=0
for p,t in zip(R1,T1): v.paste(p,(x,14)); d.text((x+2,0),t,fill=(255,0,0)); x+=p.width+16
y=R1[0].height+30; x=0
for p,t in zip(R2,T2): v.paste(p,(x,y+14)); d.text((x+2,y),t,fill=(255,0,0)); x+=p.width+16
y+=R2[0].height+40
im=Image.open('vlieg_r8.png').convert('RGBA')
for j,bg in enumerate([(248,248,248),(40,40,48)]):
    t=Image.new('RGBA',(64,64),bg+(255,)); t.alpha_composite(im); v.paste(t.convert('RGB'),(j*80,y)); d.text((j*80,y-12),'r8 1x',fill=(255,0,0))
v.save('vel.png'); print(v.size)
