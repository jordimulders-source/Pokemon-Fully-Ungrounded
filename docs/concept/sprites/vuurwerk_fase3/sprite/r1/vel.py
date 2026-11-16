# vel.png: model verkleind (BOX, 64) op 8x | sprite op 8x | 1x op licht en donker | close-ups 8x kop+spikkels en pijl (model | sprite)
import sys; from PIL import Image, ImageDraw
SP=sys.argv[1] if len(sys.argv)>1 else 'sprite.png'; OUT=sys.argv[2] if len(sys.argv)>2 else 'vel.png'
s=Image.open(SP); s.save('/tmp/_v.png',transparency=0); s=Image.open('/tmp/_v.png').convert('RGBA')
M=Image.open('../../referenties/model_v14.png').convert('RGB').crop((106,120,106+768,120+768))
m64=M.resize((64,64),Image.BOX).convert('RGBA')
def op(im,c):
    b=Image.new('RGBA',im.size,c); b.alpha_composite(im); return b.convert('RGB')
Z=8; W=64*Z
vel=Image.new('RGB',(W*2+60,W+40+ 300+ 30),(235,235,235)); d=ImageDraw.Draw(vel)
vel.paste(op(m64,(255,255,255)).resize((W,W),Image.NEAREST),(20,30)); d.text((20,12),'model (BOX naar 64) 8x',fill=0)
vel.paste(op(s,(255,255,255)).resize((W,W),Image.NEAREST),(W+40,30)); d.text((W+40,12),SP+' 8x',fill=0)
y=W+50
for i,c in enumerate([(255,255,255,255),(248,248,232,255),(40,40,48,255),(90,140,90,255)]):
    vel.paste(op(s,c),(20+i*80,y+10))
    vel.paste(op(m64,c),(20+i*80,y+90))
d.text((20,y-4),'1x: sprite (boven) / model (onder) op licht en donker',fill=0)
# close-ups: kop (0..30,0..30) en pijl (22..50,40..64), model-uitsnede uit het origineel
def cu(x0,y0,x1,y1,px,py,Zc=6):
    mc=M.crop((x0*12,y0*12,x1*12,y1*12)).resize(((x1-x0)*Zc,(y1-y0)*Zc),Image.LANCZOS)
    sc=op(s.crop((x0,y0,x1,y1)),(255,255,255)).resize(((x1-x0)*Zc,(y1-y0)*Zc),Image.NEAREST)
    vel.paste(mc,(px,py)); vel.paste(sc,(px+mc.size[0]+6,py)); return mc.size[0]*2+6
w=cu(0,0,30,30,360,y+10,6)
cu(22,40,50,64,360+w+20,y+10,6)
d.text((360,y-4),'close-ups (model | sprite): kop + spikkels, pijl',fill=0)
vel.save(OUT); print(vel.size)
