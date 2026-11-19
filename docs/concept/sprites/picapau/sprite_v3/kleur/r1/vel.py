from PIL import Image, ImageDraw
R='/home/user/Pokemon-Fully-Ungrounded/'
def ld(f,crop=True):
    p=Image.open(f); p.info['transparency']=0; im=p.convert('RGBA')
    return im.crop((0,0,64,64)) if crop else im
def op(im,bg,s):
    b=Image.new('RGBA',im.size,bg+(255,)); b.alpha_composite(im); return b.convert('RGB').resize((im.width*s,im.height*s),0)
r1=ld('picapau.png'); r17=ld('../../r17/picapau.png'); orig=ld('../../../af/picapau.png')
op(r1,(255,255,255),8).save('picapau_8x.png')
pk=ld(R+'graphics/pokemon/pikachu/anim_front_gba.png'); tl=ld(R+'graphics/pokemon/taillow/anim_front_gba.png')
W=3*512+40; H=512+30+150+150
V=Image.new('RGB',(W,H),(200,200,200)); d=ImageDraw.Draw(V)
for i,(n,im) in enumerate([('kleur r1',r1),('r17 (vorm bevroren)',r17),('origineel af/picapau.png',orig)]):
    V.paste(op(im,(255,255,255),8),(i*532,24)); d.text((i*532+4,6),n,fill=(0,0,0))
y=24+512+10
LIGHT=(255,255,255); DARK=(40,40,48)
x=0
for bg in (LIGHT,DARK):
    for im in (r1,r17):
        V.paste(op(im,bg,1),(x,y)); x+=70
    for im in (r1,r17):
        V.paste(op(im,bg,2),(x,y)); x+=134
    x+=20
d.text((4,y+132),'1x en 2x op licht en donker (telkens r1 | r17)',fill=(0,0,0))
y+=150
x=0
for bg in (LIGHT,(152,208,160)):
    for im in (pk,r1,tl):
        V.paste(op(im,bg,1),(x,y)); x+=68
    x+=20
    for im in (pk,r1,tl):
        V.paste(op(im,bg,2),(x,y)); x+=132
    x+=20
d.text((4,y+132),'naast Pikachu en Taillow (1x en 2x)',fill=(0,0,0))
V.save('vel.png')
