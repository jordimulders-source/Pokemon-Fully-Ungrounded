import numpy as np; from PIL import Image, ImageDraw; import maak_r9 as m9, kijk
from lever_r6 import png, tekst
from lever_r8 import model_crop
R='r9/'
def grid(im,s,x0,y0,x1,y1,dy=0):
    a=im.copy() if im.width>64 else kijk.op_wit(im,s).crop((x0*s,y0*s,x1*s,y1*s))
    d=ImageDraw.Draw(a)
    for i in range(x1-x0+1): d.line([(i*s,0),(i*s,a.height)],fill=(255,0,0) if (x0+i)%5==0 else (170,170,170))
    for j in range(y1-y0+1): d.line([(0,j*s),(a.width,j*s)],fill=(255,0,0) if (y0+dy+j)%5==0 else (170,170,170))
    return a
A=m9.bouw(); log=dict(m9.LOG); im=png(A,R+'zandloper_fase3.png')
r8=Image.open('r8/zandloper_fase3.png')
open(R+'log.txt','w').write('\n'.join('%s %d %s'%(k,len(v),v) for k,v in log.items()))
kaal=m9.schuif(m9.R8); print(len(np.unique(A)),'kleuren; afwijkend van kaal verschoven r8:',int((A!=kaal).sum()),'px')
for k,v in log.items(): print(' ',k,len(v))
# vel
W=3*530; c=Image.new('RGB',(W,20+512+130+20+300+20+300),'white')
mod=Image.open('../gemini/r5.webp').convert('RGB').resize((512,512),Image.LANCZOS)
for i,(x,t) in enumerate([(kijk.op_wit(im,8),'r9'),(kijk.op_wit(r8,8),'r8'),(mod,'model r5')]):
    c.paste(x,(i*530,20)); tekst(c,(i*530+4,4),t)
y=545
for i,(x,t) in enumerate([(im,'r9 1x'),(r8,'r8 1x')]):
    for j,bg in enumerate([(255,255,255),(40,44,52)]):
        b=Image.new('RGBA',(64,64),bg+(255,)); b.alpha_composite(x.convert('RGBA')); c.paste(b.convert('RGB'),(i*170+j*72,y+16))
    tekst(c,(i*170,y),t)
y=680; s=12; bx=(9,22,27,37)
h1=grid(im,s,*bx); h2=grid(r8,s,bx[0],bx[1]-2,bx[2],bx[3]-2,dy=2); h3=model_crop(bx[0],bx[1]-2,bx[2],bx[3]-2,s)
for i,(x,t) in enumerate([(h1,'r9 handen 12x (x9-26, y22-36)'),(h2,'r8 (zelfde lijfplek)'),(h3,'model r5 (zelfde lijfplek)')]):
    c.paste(x,(i*(x.width+20),y+16)); tekst(c,(i*(x.width+20),y),t)
y=y+16+h1.height+20; bt=(22,40,42,62)
t1=grid(im,s,*bt); t2=grid(r8,s,*bt)
for i,(x,t) in enumerate([(t1,'r9 staart 12x (2 rijen weg: r8-rij 51-52)'),(t2,'r8')]):
    c.paste(x,(i*(x.width+20),y+16)); tekst(c,(i*(x.width+20),y),t)
c=c.crop((0,0,W,y+16+t1.height+10)); c.save(R+'vel.png')
# overlay handen: model r5 op 24x met spritelijnen (S0/zwart) als rode rand en het r9-raster
s=24; bx=(9,22,27,37); M=model_crop(bx[0],bx[1]-2,bx[2],bx[3]-2,s).convert('RGB')
S=kijk.op_wit(im,s).crop((bx[0]*s,bx[1]*s,bx[2]*s,bx[3]*s))
ov=Image.blend(M,S,0.45); d=ImageDraw.Draw(ov)
for Y in range(bx[1],bx[3]):
    for X in range(bx[0],bx[2]):
        x0=(X-bx[0])*s; y0=(Y-bx[1])*s
        if A[Y,X] in (1,2): d.rectangle([x0+3,y0+3,x0+s-4,y0+s-4],outline=(255,0,0),width=2)
        if (Y,X) in m9.HAND: d.ellipse([x0+8,y0+8,x0+s-9,y0+s-9],outline=(0,90,255),width=2)
g=grid(ov,s,*bx); g2=grid(M,s,*bx)
o=Image.new('RGB',(g.width*2+20,g.height+20),'white'); o.paste(g,(0,20)); o.paste(g2,(g.width+20,20))
tekst(o,(2,2),'r9 over model r5, 24x: rood = lijnpixel sprite, blauw rondje = pixel aangepast naar het model'); tekst(o,(g.width+22,2),'model r5 (zelfde raster)')
o.save(R+'overlay_handen.png')
