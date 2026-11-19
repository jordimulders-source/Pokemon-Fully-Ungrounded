# vel: model | r7 | r6 op 8x; daaronder 1x en 2x op licht en donker naast Gen 3 (mareep, flaaffy, ponyta, girafarig, stantler)
from PIL import Image, ImageDraw
R='../../../../../../../'
def rgba(p):
    im=Image.open(p); 
    if im.size[1]==128: im=im.crop((0,0,64,64))
    import numpy as np
    m=np.array(im); out=np.array(im.convert('RGBA')); out[m==0,3]=0
    return Image.fromarray(out,'RGBA')
r7=rgba('lama.png'); r6=rgba('../r6/lama.png')
model=Image.open('../../gemini/poten/model_v3.png').convert('RGBA').resize((512,512),Image.LANCZOS)
gen3=[rgba(R+'graphics/pokemon/%s/anim_front.png'%n) for n in ('mareep','flaaffy','ponyta','girafarig','stantler')]
W=3*512+4*16; V=Image.new('RGBA',(W,512+32+2*(128+16)+16),(255,255,255,255)); d=ImageDraw.Draw(V)
for i,(im,t) in enumerate([(model,'model'),(r7,'r7'),(r6,'r6')]):
    x=16+i*(512+16); bg=Image.new('RGBA',(512,512),(255,255,255,255))
    bg.alpha_composite(im if im.size==(512,512) else im.resize((512,512),Image.NEAREST)); V.paste(bg,(x,24)); d.text((x,6),t,fill=(0,0,0))
y=24+512+16
for bgc in [(248,248,240,255),(40,40,48,255)]:
    strip=Image.new('RGBA',(W,128+16),bgc); x=8
    for im in [r7]+gen3:
        strip.alpha_composite(im,(x,40)); x+=72
    x+=16
    for im in [r7]+gen3:
        strip.alpha_composite(im.resize((128,128),Image.NEAREST),(x,8)); x+=136
    V.paste(strip,(0,y)); y+=128+16
V.convert('RGB').save('vel.png'); print(V.size)
