from PIL import Image, ImageDraw
import sys
G='/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/'
def load(png,pal):
    im=Image.open(G+png); L=[l.split() for l in open(G+pal).read().split('\n')[3:] if l.strip()]
    im.putpalette([int(v) for t in L for v in t[:3]]); rgb=im.convert('RGB')
    out=Image.new('RGB',(64,64),(232,232,232))
    for y in range(64):
        for x in range(64):
            if im.getpixel((x,y))!=0: out.putpixel((x,y),rgb.getpixel((x,y)))
    return out
L=[('braviary','braviary/anim_front.png','braviary/normal.pal',(0,36,16,52)),('hisui-braviary','braviary/hisui/front.png','braviary/hisui/normal.pal',(0,36,16,52)),
('staraptor','staraptor/anim_front.png','staraptor/normal.pal',(10,18,26,34)),('pidgeot gba','pidgeot/anim_front_gba.png','pidgeot/normal_gba.pal',(4,22,20,38)),
('skarmory gba','skarmory/anim_front_gba.png','skarmory/normal_gba.pal',(10,0,26,16)),('corviknight','corviknight/anim_front.png','corviknight/normal.pal',(8,2,24,18)),
('mandibuzz','mandibuzz/anim_front.png','mandibuzz/normal.pal',(40,8,56,24)),('fearow gba','fearow/anim_front_gba.png','fearow/normal_gba.pal',(46,40,62,56))]
Z=int(sys.argv[2]) if len(sys.argv)>2 else 12
V=Image.new('RGB',(len(L)*(16*Z+10),16*Z+20),(255,255,255)); d=ImageDraw.Draw(V)
for i,(n,p,q,b) in enumerate(L):
    V.paste(load(p,q).crop(b).resize((16*Z,16*Z),Image.NEAREST),(i*(16*Z+10),18)); d.text((i*(16*Z+10),3),n+' (12x)',fill=(0,0,0))
V.save(sys.argv[1])
