# Bouwt de eindbestanden: steen (hoofdversie) + staal, en vel.png
import numpy as np; from PIL import Image, ImageDraw
import lib, modelover
S=np.load('r1.npy')
STEEN=list(lib.PAL); STEEN[3:6]=[(76,70,64),(104,97,89),(176,168,154)]   # stenen vuistbijl: warm grijsbruin, helderheid = model (67/93/165)
STAAL=list(lib.PAL)
lib.opslaan(S,'terreurvogel_bijl_r1.png',STEEN)
lib.opslaan(S,'terreurvogel_bijl_r1_staal.png',STAAL)
lib.opslaan(np.load('kaal.npy'),'kaal.png',STAAL)
def rgba(p):
    im=Image.open(p); return im.convert('RGBA')
def groot(p,s=8,bg=(255,255,255,255)):
    a=rgba(p).resize((64*s,64*s),Image.NEAREST); b=Image.new('RGBA',a.size,bg); b.alpha_composite(a); return b
# rode modelomtrek op 8x
m=np.asarray(Image.open('../gemini/r1_eenvoud.png').convert('RGB')).astype(int).min(2)<225
mi=Image.fromarray((m*255).astype('uint8'))
f=lib.S/10.24*8; ox=(lib.OX+((0-9.25)/10.24-lib.X0)*lib.S)*8; oy=(lib.OY+((0-9.25)/10.24-lib.Y0)*lib.S)*8
z=mi.resize((round(1024*f),round(1024*f)),Image.BILINEAR); can=Image.new('L',(512,512),0); can.paste(z,(round(ox),round(oy)))
M=np.asarray(can)>127; P=np.pad(M,1); rand=M&~(P[:-2,1:-1]&P[2:,1:-1]&P[1:-1,:-2]&P[1:-1,2:])
def omtrek(img):
    a=np.array(img); a[rand]=(230,0,0,255); return Image.fromarray(a)
W=512; vel=Image.new('RGBA',(W*4+50,W+250),(236,236,236,255)); d=ImageDraw.Draw(vel)
panelen=[('sprite r1 (steen) 8x',groot('terreurvogel_bijl_r1.png')),
         ('staal (modelkleuren) 8x',groot('terreurvogel_bijl_r1_staal.png')),
         ('kale reductie 8x',groot('kaal.png')),
         ('model op spriteschaal',modelover.model_op(8).convert('RGBA'))]
for i,(t,p) in enumerate(panelen):
    x=10+i*(W+10); vel.alpha_composite(p.crop((0,0,W,W)),(x,30)); d.text((x,10),t,fill=(0,0,0))
# omtrek over sprite (onder)
y2=W+40
d.text((10,y2),'rode modelomtrek over de sprite (8x, uitsnede)',fill=(0,0,0))
o=omtrek(groot('terreurvogel_bijl_r1.png')).crop((0,160,W,W)); vel.alpha_composite(o.resize((o.width*1,o.height*1)),(10,y2+15))
# 1x en 2x op licht en donker
x=W+30
for j,(bg,nm) in enumerate([((248,248,240,255),'licht'),((40,44,52,255),'donker')]):
    for k,p in enumerate(['terreurvogel_bijl_r1.png','terreurvogel_bijl_r1_staal.png']):
        for s in (1,2):
            b=Image.new('RGBA',(64*s,64*s),bg); b.alpha_composite(rgba(p).resize((64*s,64*s),Image.NEAREST))
            xx=x+j*420+k*200+(0 if s==1 else 70); vel.alpha_composite(b,(xx,y2+20))
    d.text((x+j*420,y2+5),nm+': steen 1x 2x | staal 1x 2x',fill=(0,0,0))
vel.save('vel.png'); print(vel.size)
