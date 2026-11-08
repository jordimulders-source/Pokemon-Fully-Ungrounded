# vel4.py: r4 | r3 | Gemini (8x); klauwen r4|r3 (12x); poten r4|Gemini (12x); 1x
from PIL import Image, ImageDraw
G='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/olinguito_v2/gemini_samen/'
def on(p,col=(255,255,255)):
    im=Image.open(p).convert('RGBA'); b=Image.new('RGBA',im.size,col); b.alpha_composite(im); return b.convert('RGB')
r4,r3=G+'olinguito_r4.png',G+'olinguito_r3.png'; model=Image.open(G+'stappen/model_512.png').convert('RGB')
o=Image.new('RGB',(3*512+40,512+20+300+20+80),(235,235,235)); d=ImageDraw.Draw(o)
for i,(im,t) in enumerate([(on(r4),'r4'),(on(r3),'r3'),(model,'Gemini v4')]):
    o.paste(im.resize((512,512),0) if im.size!=(512,512) else im,(i*532,0)); d.text((10+i*532,5),t,fill=(200,0,0))
y=532; z=12; cb=(18,48,32,62); W=(cb[2]-cb[0])*z; H=(cb[3]-cb[1])*z
o.paste(on(r4).crop(cb).resize((W,H),0),(0,y)); o.paste(on(r3).crop(cb).resize((W,H),0),(W+8,y))
d.text((5,y+2),'klauwen r4',fill=(200,0,0)); d.text((W+13,y+2),'klauwen r3',fill=(200,0,0))
pb=(24,36,50,52); W2=(pb[2]-pb[0])*z; H2=(pb[3]-pb[1])*z; x0=2*W+30
o.paste(on(r4).crop(pb).resize((W2,H2),0),(x0,y)); o.paste(model.crop(tuple(v*8 for v in pb)).resize((W2,H2),Image.LANCZOS),(x0+W2+8,y))
d.text((x0+5,y+2),'poten r4',fill=(200,0,0)); d.text((x0+W2+13,y+2),'poten Gemini',fill=(200,0,0))
y2=y+max(H,H2)+20
for i,c in enumerate([(255,255,255),(152,208,160),(40,40,48),(90,90,90)]): o.paste(on(r4,c),(10+80*i,y2))
o.crop((0,0,o.width,y2+70)).save(G+'vel_r4.png')
