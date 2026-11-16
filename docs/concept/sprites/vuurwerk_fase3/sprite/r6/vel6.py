# vel.png r6: (1) kop 8x: geel+glans | geel | goud+glans | goud | r5 | model (hoge resolutie) | bronoog Seviper (Gen 3) 8x;
# (2) hele sprite 8x (geel+glans) | model; (3) 1x op wit/creme/donker/groen: 4 varianten + r5.
from PIL import Image, ImageDraw
def rgba(f):
    s=Image.open(f); s.save('/tmp/_v6.png',transparency=0); return Image.open('/tmp/_v6.png').convert('RGBA')
def op(im,c): b=Image.new('RGBA',im.size,c); b.alpha_composite(im); return b.convert('RGB')
M=Image.open('../../referenties/model_v14.png').convert('RGB')
V=['geel_glans','geel','goud_glans','goud']; KW,KH=24,30; Z=8
vel=Image.new('RGB',(6*(KW*Z+12)+14*13+40,30+KH*Z+40+512+40+4*70+20),(232,232,232)); d=ImageDraw.Draw(vel)
y=10; d.text((20,y),'1. kop 8x: geel+glans | geel | goud+glans | goud | r5 | model | bronoog Seviper Gen 3 (x16-22, y16-20, 8x)',fill=0); y+=16
fs=['sprite_%s.png'%v for v in V]+['../r5/sprite_115_geel.png']
for i,f in enumerate(fs): vel.paste(op(rgba(f),(255,255,255,255)).crop((0,1,KW,KH+1)).resize((KW*Z,KH*Z),Image.NEAREST),(20+i*(KW*Z+12),y))
vel.paste(M.crop((106+12*3,120+12*2,106+12*23,120+12*27)).resize((KW*Z,KH*Z),Image.LANCZOS),(20+5*(KW*Z+12),y))   # model: kop (r4-raster x3-23, y2-27)
sv=rgba('../../../../../../graphics/pokemon/seviper/anim_front_gba.png').crop((12,12,26,24))
Q=13; vel.paste(op(sv,(255,255,255,255)).resize((14*Q,12*Q),Image.NEAREST),(20+6*(KW*Z+12),y)); dd=ImageDraw.Draw(vel)
dd.rectangle([20+6*(KW*Z+12)+4*Q,y+4*Q,20+6*(KW*Z+12)+11*Q,y+9*Q],outline=(0,120,255))
y+=KH*Z+24; d.text((20,y),'2. hele sprite 8x (geel + glans) | model',fill=0); y+=16
vel.paste(op(rgba('sprite_geel_glans.png'),(255,255,255,255)).resize((512,512),Image.NEAREST),(20,y))
vel.paste(M.crop((106,120,874,888)).resize((512,512),Image.LANCZOS),(552,y))
y+=512+24; d.text((20,y),'3. 1x op wit / creme / donker / groen: geel+glans, geel, goud+glans, goud, r5',fill=0); y+=16
for r,c in enumerate([(255,255,255,255),(248,240,220,255),(40,40,48,255),(90,140,90,255)]):
    for i,f in enumerate(fs): vel.paste(op(rgba(f),c),(20+i*70,y+r*70))
vel.save('vel.png'); print(vel.size)
