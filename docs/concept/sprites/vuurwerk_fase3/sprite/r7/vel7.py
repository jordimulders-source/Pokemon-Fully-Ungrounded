# vel.png r7: (1) kop 8x: r7 geel | r7 goud | r5 115% geel | model (hoge resolutie); (2) hele sprite 8x: r7 geel | r7 goud;
# (3) 1x op wit / creme / donker / groen: r7 geel, r7 goud, r5.
from PIL import Image, ImageDraw
def rgba(f):
    s=Image.open(f); s.save('/tmp/_v7.png',transparency=0); return Image.open('/tmp/_v7.png').convert('RGBA')
def op(im,c): b=Image.new('RGBA',im.size,c); b.alpha_composite(im); return b.convert('RGB')
M=Image.open('../../referenties/model_v14.png').convert('RGB')
fs=['sprite_geel.png','sprite_goud.png','../r5/sprite_115_geel.png']; KW,KH,Z=24,30,8
vel=Image.new('RGB',(max(4*(KW*Z+12),2*532)+20,30+KH*Z+40+512+40+4*70+20),(232,232,232)); d=ImageDraw.Draw(vel)
y=10; d.text((20,y),'1. kop 8x: r7 geel | r7 goud | r5 115% | model',fill=0); y+=16
for i,f in enumerate(fs): vel.paste(op(rgba(f),(255,255,255,255)).crop((0,1,KW,KH+1)).resize((KW*Z,KH*Z),Image.NEAREST),(20+i*(KW*Z+12),y))
vel.paste(M.crop((106+12*3,120+12*2,106+12*23,120+12*27)).resize((KW*Z,KH*Z),Image.LANCZOS),(20+3*(KW*Z+12),y))
y+=KH*Z+24; d.text((20,y),'2. hele sprite 8x: r7 geel | r7 goud',fill=0); y+=16
for i,f in enumerate(fs[:2]): vel.paste(op(rgba(f),(255,255,255,255)).resize((512,512),Image.NEAREST),(20+i*532,y))
y+=512+24; d.text((20,y),'3. 1x op wit / creme / donker / groen: r7 geel, r7 goud, r5',fill=0); y+=16
for r,c in enumerate([(255,255,255,255),(248,240,220,255),(40,40,48,255),(90,140,90,255)]):
    for i,f in enumerate(fs): vel.paste(op(rgba(f),c),(20+i*70,y+r*70))
vel.save('vel.png'); print(vel.size)
