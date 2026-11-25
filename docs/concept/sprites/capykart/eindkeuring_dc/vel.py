# vel.png: vorige (eindkeuring_r17) | nieuw | model zelfde schaal | Dundragoon | Skinguin (8x); blokken en kop 12x; 1x licht/donker. Draaien vanuit capykart/.
from PIL import Image, ImageDraw
S=62/73; Z=8; D='eindkeuring_dc/'
def rgba(p):
    im=Image.open(p)
    if im.mode=='P': im.save('/tmp/_ekdc.png',transparency=0); im=Image.open('/tmp/_ekdc.png')
    return im.convert('RGBA')
def op(im,bg,z):
    c=Image.new('RGBA',im.size,bg+(255,)); c.alpha_composite(im); return c.resize((im.width*z,im.height*z),Image.NEAREST)
vor=rgba('eindkeuring_r17/capykart.png'); nw=rgba(D+'capykart.png')
nat=Image.open('sprite/r17/natief.png').convert('RGBA'); n=round(99*S*Z)
m=Image.new('RGBA',(64*Z,64*Z),(255,255,255,255)); m.paste(nat.resize((n,n),Image.NEAREST),(round((1-12*S)*Z),round((2-11*S)*Z)))
mm={k:rgba(f'../{k}/af/{k}.png') for k in ['dundragoon','skinguin','viscacha','awki']}
panelen=[op(vor,(255,255,255),Z),op(nw,(255,255,255),Z),m,op(mm['dundragoon'],(255,255,255),Z),op(mm['skinguin'],(255,255,255),Z)]
tit=['vorige (eindkeuring_r17)','nieuw (eindkeuring_dc)','model_r5 zelfde schaal','Dundragoon (maatstaf)','Skinguin (maatstaf)']
G=12; W=5*512+6*G
# 12x uitsneden: kop (x13-44,y9-40) en toren (x41-59,y1-35), vorige | nieuw | model
def uit(im,box,z): return im.crop(box).resize(((box[2]-box[0])*z,(box[3]-box[1])*z),Image.NEAREST)
mod64=m.resize((64,64),Image.BOX)
kop=(13,9,44,40); tor=(41,1,59,35); z=12
rij2=[]
for box in (kop,tor):
    for im in (op(vor,(255,255,255),1),op(nw,(255,255,255),1),mod64): rij2.append(uit(im,box,z))
H2=max(r.height for r in rij2)
Hh=20+512+G+20+H2+G+20+2*(128+G)+G
vel=Image.new('RGB',(W,Hh),(235,235,235)); d=ImageDraw.Draw(vel)
for i,(p,t) in enumerate(zip(panelen,tit)):
    x=G+i*(512+G); d.text((x,4),t,fill=(0,0,0)); vel.paste(p.convert('RGB'),(x,20))
y=20+512+G; d.text((G,y),'12x: kop vorige | nieuw | model    toren vorige | nieuw | model',fill=(0,0,0)); y+=20; x=G
for r in rij2: vel.paste(r.convert('RGB'),(x,y)); x+=r.width+G
y+=H2+G; d.text((G,y),'1x (2x getoond) op licht en donker: vorige | nieuw | dundragoon | skinguin | zapacha | princadee',fill=(0,0,0)); y+=20
reeks=[vor,nw]+list(mm.values())
for bg in [(248,248,240),(40,44,52)]:
    x=G
    for im in reeks: vel.paste(op(im,bg,2).convert('RGB'),(x,y)); x+=128+G
    y+=128+G
vel.save(D+'vel.png'); print('ok',vel.size)
