# vel.png r8: (1) kop 8x: probeersels a-e | r5 115% | model; (2) 1x hele sprite op wit / creme / donker / groen (a-e, r5);
# (3) 2x hele sprite a-e; (4) vlamtong: r7 | r8 | model op 16x.
from PIL import Image, ImageDraw
def rgba(f):
    s=Image.open(f); s.save('/tmp/_v8.png',transparency=0); return Image.open('/tmp/_v8.png').convert('RGBA')
def op(im,c): b=Image.new('RGBA',im.size,c); b.alpha_composite(im); return b.convert('RGB')
M=Image.open('../../referenties/model_v14.png').convert('RGB')
K='abcde'; fs=['sprite_%s.png'%k for k in K]+['../r5/sprite_115_geel.png']; KW,KH,Z=24,30,8
W=7*(KW*Z+12)+20; vel=Image.new('RGB',(W,30+KH*Z+40+4*70+40+140+40+8*16+20),(232,232,232)); d=ImageDraw.Draw(vel)
y=10; d.text((20,y),'1. kop 8x: a | b | c | d | e | r5 115% | model',fill=0); y+=16
for i,f in enumerate(fs): vel.paste(op(rgba(f),(255,255,255,255)).crop((0,1,KW,KH+1)).resize((KW*Z,KH*Z),Image.NEAREST),(20+i*(KW*Z+12),y)); d.text((24+i*(KW*Z+12),y+2),(K+' ')[i] if i<5 else 'r5',fill=(0,0,255))
vel.paste(M.crop((106+12*3,120+12*2,106+12*23,120+12*27)).resize((KW*Z,KH*Z),Image.LANCZOS),(20+6*(KW*Z+12),y))
y+=KH*Z+24; d.text((20,y),'2. 1x op wit / creme / donker / groen: a b c d e r5',fill=0); y+=16
for r,c in enumerate([(255,255,255,255),(248,240,220,255),(40,40,48,255),(90,140,90,255)]):
    for i,f in enumerate(fs): vel.paste(op(rgba(f),c),(20+i*70,y+r*70))
y+=4*70+24; d.text((20,y),'3. 2x: a b c d e r5',fill=0); y+=16
for i,f in enumerate(fs): vel.paste(op(rgba(f),(255,255,255,255)).resize((128,128),Image.NEAREST),(20+i*140,y))
y+=140+24; d.text((20,y),'4. vlamtong 16x: r7 | r8 | model (r4-raster x11-19, y1-8; de kop is in r8 115% groter)',fill=0); y+=16
for i,f in enumerate(['../r7/sprite_geel.png','sprite_a.png']): vel.paste(op(rgba(f),(255,255,255,255)).crop((11,0,20,8)).resize((9*16,8*16),Image.NEAREST),(20+i*170,y))
import sys; sys.path.insert(0,'../r5')
vel.paste(Image.open('/tmp/_vlam_model.png') if False else M.crop((106+12*11,120+12*1,106+12*19,120+12*8)).resize((8*16,7*16),Image.LANCZOS),(20+2*170,y))
vel.save('vel.png'); print(vel.size)
