# vel_c.png: kop 16x: r15b | r17b | b | c | model; daaronder 8x: b | c | model | Dundragoon | Skinguin; 1x licht/donker. Draaien vanuit capykart/.
from PIL import Image, ImageDraw
S=62/73; D='eindkeuring_dc/'
def rgba(p):
    im=Image.open(p)
    if im.mode=='P': im.save('/tmp/_ekc.png',transparency=0); im=Image.open('/tmp/_ekc.png')
    return im.convert('RGBA')
def op(im,bg,z):
    c=Image.new('RGBA',im.size,bg+(255,)); c.alpha_composite(im); return c.resize((im.width*z,im.height*z),Image.NEAREST)
r15=rgba('sprite/r15b/capykart_creme.png'); r17=rgba('sprite/r17b/capykart.png'); b=rgba(D+'capykart_b.png'); c=rgba(D+'capykart_c.png')
nat=Image.open('sprite/r17/natief.png').convert('RGBA')
def model(z):
    n=round(99*S*z); m=Image.new('RGBA',(64*z,64*z),(255,255,255,255)); m.paste(nat.resize((n,n),Image.NEAREST),(round((1-12*S)*z),round((2-11*S)*z))); return m
mm={k:rgba(f'../{k}/af/{k}.png') for k in ['dundragoon','skinguin','viscacha','awki']}
G=12; box=(12,8,44,36); z=16
def uit(im,zz=z): return im.crop((box[0]*zz,box[1]*zz,box[2]*zz,box[3]*zz))
kop=[uit(op(r15,(255,255,255),z)),uit(op(r17,(255,255,255),z)),uit(op(b,(255,255,255),z)),uit(op(c,(255,255,255),z)),uit(model(z))]
kt=['r15b (oog/wenkbrauw-bron)','r17b (snuit/oren-bron)','b','c','model_r5']
W8=[op(b,(255,255,255),8),op(c,(255,255,255),8),model(8),op(mm['dundragoon'],(255,255,255),8),op(mm['skinguin'],(255,255,255),8)]
t8=['b','c','model_r5','Dundragoon','Skinguin']
kw=kop[0].width; kh=kop[0].height
W=max(5*kw+6*G,5*512+6*G); H=20+kh+G+20+512+G+20+2*(128+G)+G
vel=Image.new('RGB',(W,H),(235,235,235)); d=ImageDraw.Draw(vel)
for i,(p,t) in enumerate(zip(kop,kt)):
    x=G+i*(kw+G); d.text((x,4),'16x kop: '+t,fill=(0,0,0)); vel.paste(p.convert('RGB'),(x,20))
y=20+kh+G
for i,(p,t) in enumerate(zip(W8,t8)):
    x=G+i*(512+G); d.text((x,y),'8x: '+t,fill=(0,0,0)); vel.paste(p.convert('RGB'),(x,y+20))
y+=20+512+G; d.text((G,y),'1x (2x getoond): b | c | dundragoon | skinguin | zapacha | princadee',fill=(0,0,0)); y+=20
for bg in [(248,248,240),(40,44,52)]:
    x=G
    for im in [b,c]+list(mm.values()): vel.paste(op(im,bg,2).convert('RGB'),(x,y)); x+=128+G
    y+=128+G
vel.save(D+'vel_c.png'); print('ok',vel.size)
