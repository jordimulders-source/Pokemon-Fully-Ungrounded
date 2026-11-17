# vel.png r5: (1) hele sprite 8x: r5 115% | r5 125% (oog geel) | r4 | model; (2) kop 6x: oogvarianten geel/goud/magenta/rood
# voor beide maten + model; (3) 1x op licht/creme/donker/groen: alle 8 varianten, r4, model.
from PIL import Image, ImageDraw
def rgba(f):
    s=Image.open(f); s.save('/tmp/_v5.png',transparency=0); return Image.open('/tmp/_v5.png').convert('RGBA')
def op(im,c): b=Image.new('RGBA',im.size,c); b.alpha_composite(im); return b.convert('RGB')
M=Image.open('../../referenties/model_v14.png').convert('RGB'); MB=M.crop((106,120,874,888)); m64=MB.resize((64,64),Image.BOX).convert('RGBA')
OOG=['geel','goud','magenta','rood']
vel=Image.new('RGB',(4*532+20,30+512+40+2*(32*6+30)+40+4*70+20),(232,232,232)); d=ImageDraw.Draw(vel)
y=10; d.text((20,y),'1. hele sprite 8x: r5 kop 115% | r5 kop 125% (oog geel) | r4 | model',fill=0); y+=16
for i,im in enumerate([rgba('sprite_115_geel.png'),rgba('sprite_125_geel.png'),rgba('../r4/sprite.png')]):
    vel.paste(op(im,(255,255,255,255)).resize((512,512),Image.NEAREST),(20+i*532,y))
vel.paste(MB.resize((512,512),Image.LANCZOS),(20+3*532,y))
y+=512+24; d.text((20,y),'2. kop 6x, oogvarianten: geel | goud | magenta | rood  (boven 115%, onder 125%), model rechts',fill=0); y+=16
for r,maat in enumerate((115,125)):
    for i,o in enumerate(OOG):
        vel.paste(op(rgba('sprite_%d_%s.png'%(maat,o)),(255,255,255,255)).crop((0,0,30,32)).resize((180,192),Image.NEAREST),(20+i*200,y+r*(192+20)))
vel.paste(M.crop((106-24,120-24,106+336,120+360)).resize((300,320),Image.LANCZOS),(20+4*200,y))
y+=2*(192+20)+24; d.text((20,y),'3. 1x op wit / creme / donker / groen: 115 geel goud magenta rood | 125 geel goud magenta rood | r4 | model',fill=0); y+=16
fs=['sprite_115_%s.png'%o for o in OOG]+['sprite_125_%s.png'%o for o in OOG]+['../r4/sprite.png']
for r,c in enumerate([(255,255,255,255),(248,240,220,255),(40,40,48,255),(90,140,90,255)]):
    for i,f in enumerate(fs): vel.paste(op(rgba(f),c),(20+i*70,y+r*70))
    vel.paste(op(m64,c),(20+len(fs)*70,y+r*70))
vel.save('vel.png'); print(vel.size)
