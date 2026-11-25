# vel.png: r17b | eind | model op dezelfde schaal | Dundragoon (8x); daaronder 1x op licht en donker (+ maatstaf). Draaien vanuit capykart/.
from PIL import Image, ImageDraw
S=62/73; Z=8; D='eindkeuring_r17/'
def rgba(p):
    im=Image.open(p)
    if im.mode=='P': im.save('/tmp/_ek.png',transparency=0); im=Image.open('/tmp/_ek.png')
    return im.convert('RGBA')
def op(im,bg,z):
    c=Image.new('RGBA',im.size,bg+(255,)); c.alpha_composite(im); return c.resize((im.width*z,im.height*z),Image.NEAREST)
r17b=rgba('sprite/r17b/capykart.png'); eind=rgba(D+'capykart.png')
op(eind,(255,255,255),8).convert('RGB').save(D+'capykart_8x.png')
nat=Image.open('sprite/r17/natief.png').convert('RGBA'); n=round(99*S*Z)
m=Image.new('RGBA',(64*Z,64*Z),(255,255,255,255)); m.paste(nat.resize((n,n),Image.NEAREST),(round((1-12*S)*Z),round((2-11*S)*Z)))
mt=['sprite/r17b','eind (DC)','model_r5 zelfde schaal','Dundragoon (maatstaf)']
maat={'dundragoon':'../dundragoon/af/dundragoon.png','skinguin':'../skinguin/af/skinguin.png','viscacha':'../viscacha/af/viscacha.png','awki':'../awki/af/awki.png'}
mm={k:rgba(v) for k,v in maat.items()}
dun=mm['dundragoon']
panelen=[op(r17b,(255,255,255),Z),op(eind,(255,255,255),Z),m.convert('RGBA'),op(dun.resize((64,64)) if dun.size!=(64,64) else dun,(255,255,255),Z)]
G=12; W=4*512+5*G; Hh=20+512+G+20+2*(64*2+G)+G
vel=Image.new('RGB',(W,Hh),(235,235,235)); d=ImageDraw.Draw(vel)
for i,(p,t) in enumerate(zip(panelen,mt)):
    x=G+i*(512+G); d.text((x,4),t,fill=(0,0,0)); vel.paste(p.convert('RGB'),(x,20))
y=20+512+G; d.text((G,y),'1x (2x getoond) op licht en donker: r17b | eind | dundragoon | skinguin | zapacha | princadee',fill=(0,0,0)); y+=20
reeks=[r17b,eind]+list(mm.values())
for bg in [(248,248,240),(40,44,52)]:
    x=G
    for im in reeks:
        vel.paste(op(im,bg,2).convert('RGB'),(x,y)); x+=im.width*2+G
    y+=64*2+G
vel.save(D+'vel.png'); print('ok',vel.size)
