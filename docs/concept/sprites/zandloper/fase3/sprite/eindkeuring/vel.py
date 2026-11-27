import numpy as np; from PIL import Image, ImageDraw
R='/home/user/Pokemon-Fully-Ungrounded/'; Z=R+'docs/concept/sprites/'
def rgba(p,pal=None):
    im=Image.open(p)
    if pal:
        L=open(pal).read().split()[3:]; im.putpalette([int(v) for v in L][:48]+[0]*720)
    a=np.array(im.crop((0,0,64,64))); pl=np.array(im.getpalette()[:48]+[0]*720).reshape(-1,3)[:256]
    o=np.zeros((64,64,4),np.uint8); o[...,:3]=pl[a]; o[...,3]=np.where(a==0,0,255); return Image.fromarray(o,'RGBA')
def op(im,s,bg=(255,255,255)):
    b=Image.new('RGBA',im.size,bg+(255,)); b.alpha_composite(im); return b.convert('RGB').resize((im.width*s,im.height*s),Image.NEAREST)
voor=rgba('../r11/biceps.png'); na=rgba('zandloper_fase3.png')
m=Image.open(Z+'zandloper/fase3/gemini/r5.webp').convert('RGB').crop((150,30,930,1010)).resize((408,512),Image.LANCZOS)
rij1=[('voor (r11 biceps)',op(voor,8)),('na (eindkeuring)',op(na,8)),('model r5',m)]
rij2=[('skinguin',op(rgba(Z+'skinguin/af/skinguin.png'),8)),('dundragoon',op(rgba(Z+'dundragoon/af/dundragoon.png'),8)),
      ('machamp gba',op(rgba(R+'graphics/pokemon/machamp/anim_front_gba.png',R+'graphics/pokemon/machamp/normal_gba.pal'),8))]
W=3*530; H=2*560+120; c=Image.new('RGB',(W,H),'white'); d=ImageDraw.Draw(c)
for r,rij in enumerate([rij1,rij2]):
    for i,(t,im) in enumerate(rij):
        c.paste(im,(i*530,r*560+20)); d.text((i*530,r*560+4),t,fill='black')
y=2*560+10; x=0
for t,im in [('voor',voor),('na',na)]:
    for bg in [(255,255,255),(40,44,52)]:
        c.paste(op(im,1,bg),(x,y+14)); x+=74
    d.text((x-148,y),t,fill='black')
c.save('vel.png'); op(na,8).save('zandloper_fase3_8x.png')
