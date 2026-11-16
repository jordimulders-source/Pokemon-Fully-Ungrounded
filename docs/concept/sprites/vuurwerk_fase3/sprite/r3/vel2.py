# vel.png r2: r2 | r1 | model (BOX) op 8x; 1x op licht/donker (r2, r1, model); close-ups kop en pijl (model | r2 | r1) op 6x;
# spikkelvarianten A/B/C op 1x en 4x.
from PIL import Image, ImageDraw
def rgba(f):
    s=Image.open(f)
    if s.mode=='P': s.save('/tmp/_v2.png',transparency=0); s=Image.open('/tmp/_v2.png')
    return s.convert('RGBA')
def op(im,c): b=Image.new('RGBA',im.size,c); b.alpha_composite(im); return b.convert('RGB')
r2=rgba('sprite.png'); r1=rgba('../r1/sprite.png')
M=Image.open('../../referenties/model_v14.png').convert('RGB').crop((106,120,106+768,120+768)); m64=M.resize((64,64),Image.BOX).convert('RGBA')
Z=8; W=512
vel=Image.new('RGB',(3*W+80,W+40+190+250+300),(232,232,232)); d=ImageDraw.Draw(vel)
for i,(im,t) in enumerate([(r2,'r2 (variant A)'),(r1,'r1'),(m64,'model BOX->64')]):
    vel.paste(op(im,(255,255,255)).resize((W,W),Image.NEAREST),(20+i*(W+20),30)); d.text((20+i*(W+20),12),t+' 8x',fill=0)
y=W+50; d.text((20,y),'1x: r2 / r1 / model op wit, creme, donker, groen',fill=0)
for i,c in enumerate([(255,255,255,255),(248,248,232,255),(40,40,48,255),(90,140,90,255)]):
    for j,im in enumerate((r2,r1,m64)): vel.paste(op(im,c),(20+i*76,y+16+j*56))
# close-ups
def cu(x0,y0,x1,y1,px,py,Zc=6):
    w=(x1-x0)*Zc; h=(y1-y0)*Zc
    vel.paste(M.crop((x0*12,y0*12,x1*12,y1*12)).resize((w,h),Image.LANCZOS),(px,py))
    vel.paste(op(r2.crop((x0,y0,x1,y1)),(255,255,255)).resize((w,h),Image.NEAREST),(px+w+6,py))
    vel.paste(op(r1.crop((x0,y0,x1,y1)),(255,255,255)).resize((w,h),Image.NEAREST),(px+2*w+12,py))
    return 3*w+12
d.text((340,y),'close-ups 6x: model | r2 | r1  (kop, pijl)',fill=0)
w=cu(0,0,30,32,340,y+16); cu(22,42,50,64,340+w+20,y+16)
y2=y+16+32*6+20
d.text((20,y2),'vuurwerkspikkels om de kop: A (b2 op de kop) | B (b3 + b2 naast de kop) | C (b1 op de kop, straal 13)  -- 1x en 4x',fill=0)
for i,k in enumerate('ABC'):
    s=rgba('sprite_%s.png'%k)
    vel.paste(op(s,(255,255,255)),(20+i*(256+60),y2+16)); vel.paste(op(s,(40,40,48,255)),(20+i*(256+60),y2+86))
    vel.paste(op(s.crop((0,0,40,48)),(255,255,255)).resize((160,192),Image.NEAREST),(100+i*(256+60),y2+16))
    d.text((20+i*(256+60),y2+160),k,fill=0)
vel.save('vel.png'); print(vel.size)
