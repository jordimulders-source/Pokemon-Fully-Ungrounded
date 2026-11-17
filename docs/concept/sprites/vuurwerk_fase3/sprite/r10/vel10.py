# vel.png r10: hele sprite 8x (r10 B | r10 rond | r9 a | model-64); kop 8x (r10 B | r10 rond | r9 a | model hoog);
# 1x op wit / creme / donker / groen: r10 B, r10 rond, r9 a.
import numpy as np, json; from PIL import Image, ImageDraw
PAL=json.load(open('../r9/palet.json'))
def rgba(f):
    s=np.asarray(Image.open(f)).astype(int); c=np.zeros((64,64,4),np.uint8); c[...,:3]=np.array(PAL,np.uint8)[s]; c[...,3]=(s>0)*255
    return Image.fromarray(c,'RGBA')
def op(im,c): b=Image.new('RGBA',im.size,c); b.alpha_composite(im); return b.convert('RGB')
M=Image.open('../../referenties/model_v14.png').convert('RGB'); m64=Image.open('../keuring_r9/model64.png').convert('RGB')
fs=['sprite_B.png','sprite_rond.png','../r9/sprite_a.png']; KW,KH,Z=28,36,8
vel=Image.new('RGB',(4*532+20,30+512+40+KH*Z+40+4*70+20),(232,232,232)); d=ImageDraw.Draw(vel)
y=10; d.text((20,y),'hele sprite 8x: r10 B | r10 rond | r9 a | model-64',fill=0); y+=16
for i,f in enumerate(fs): vel.paste(op(rgba(f),(255,255,255,255)).resize((512,512),Image.NEAREST),(20+i*532,y))
vel.paste(m64.resize((512,512),Image.NEAREST),(20+3*532,y))
y+=512+24; d.text((20,y),'kop 8x: r10 B | r10 rond | r9 a | model hoog',fill=0); y+=16
for i,f in enumerate(fs): vel.paste(op(rgba(f),(255,255,255,255)).crop((0,0,KW,KH)).resize((KW*Z,KH*Z),Image.NEAREST),(20+i*(KW*Z+12),y))
vel.paste(M.crop((106+12*0,120+12*0,106+12*25,120+12*32)).resize((KW*Z,KH*Z),Image.LANCZOS),(20+3*(KW*Z+12),y))
y+=KH*Z+24; d.text((20,y),'1x op wit / creme / donker / groen: r10 B, r10 rond, r9 a',fill=0); y+=16
for r,c in enumerate([(255,255,255,255),(248,240,220,255),(40,40,48,255),(90,140,90,255)]):
    for i,f in enumerate(fs): vel.paste(op(rgba(f),c),(20+i*70,y+r*70))
vel.save('vel.png'); print(vel.size)
