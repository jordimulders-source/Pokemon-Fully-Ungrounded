# vel.png r3: r3 (V, spikkels B) | r2 | model op 8x; 1x licht/donker; close-up kop 8x (model hoge resolutie | r3 V | r3 W | r2);
# spikkelvarianten A/B/C (gezicht V) op 1x en 4x.
from PIL import Image, ImageDraw
def rgba(f):
    s=Image.open(f); s.save('/tmp/_v3.png',transparency=0) if s.mode=='P' else None
    return (Image.open('/tmp/_v3.png') if s.mode=='P' else s).convert('RGBA')
def op(im,c): b=Image.new('RGBA',im.size,c); b.alpha_composite(im); return b.convert('RGB')
r3=rgba('sprite.png'); r2=rgba('../r2/sprite_B.png'); M=Image.open('../../referenties/model_v14.png').convert('RGB').crop((106,120,874,888))
m64=M.resize((64,64),Image.BOX).convert('RGBA')
W=512; vel=Image.new('RGB',(3*W+80,W+50+190+300+230),(232,232,232)); d=ImageDraw.Draw(vel)
for i,(im,t) in enumerate([(r3,'r3 (gezicht V, spikkels B)'),(r2,'r2 (spikkels B)'),(m64,'model BOX->64')]):
    vel.paste(op(im,(255,255,255)).resize((W,W),Image.NEAREST),(20+i*(W+20),30)); d.text((20+i*(W+20),12),t+' 8x',fill=0)
y=W+50; d.text((20,y),'1x: r3 / r2 / model op wit, creme, donker, groen',fill=0)
for i,c in enumerate([(255,255,255,255),(248,248,232,255),(40,40,48,255),(90,140,90,255)]):
    for j,im in enumerate((r3,r2,m64)): vel.paste(op(im,c),(20+i*76,y+16+j*56))
x0,y0,x1,y1=0,0,30,32; Z=8; w=(x1-x0)*Z; h=(y1-y0)*Z
d.text((340,y),'close-up kop 8x: model (hoge resolutie) | r3 gezicht V | r3 gezicht W | r2',fill=0)
vel.paste(M.crop((x0*12,y0*12,x1*12,y1*12)).resize((w,h),Image.LANCZOS),(340,y+16))
for i,f in enumerate(['sprite_V_B.png','sprite_W_B.png','../r2/sprite_B.png']):
    vel.paste(op(rgba(f).crop((x0,y0,x1,y1)),(255,255,255)).resize((w,h),Image.NEAREST),(340+(i+1)*(w+8),y+16))
y2=y+16+h+20; d.text((20,y2),'vuurwerkspikkels (gezicht V): A b2 op de kop | B b3 + b2 naast de kop (= r2) | C b1 op de kop, straal 16  -- 1x licht/donker en 4x',fill=0)
for i,k in enumerate('ABC'):
    s=rgba('sprite_V_%s.png'%k); bx=20+i*(330)
    vel.paste(op(s,(255,255,255)),(bx,y2+16)); vel.paste(op(s,(40,40,48,255)),(bx,y2+86)); d.text((bx,y2+156),k,fill=0)
    vel.paste(op(s.crop((0,0,44,50)),(255,255,255)).resize((176,200),Image.NEAREST),(bx+80,y2+16))
vel.save('vel.png'); print(vel.size)
