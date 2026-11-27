"""Vellen eindkeuring. Draaien vanuit guarana_fase2/: python3 eindkeuring/vel_ek.py"""
from PIL import Image, ImageDraw
def rgba(p):
    im=Image.open(p); im.save('/dev/null','PNG') if False else None
    return im.convert('RGBA')
def op(bg,im,z):
    c=Image.new('RGBA',im.size,bg); c.alpha_composite(im); return c.resize((im.width*z,im.height*z),Image.NEAREST)
S=[('fase 1','../guarana/af/guarana.png'),('EK','eindkeuring/guarana2_ek.png'),('r16','sprite_r16/guarana2_r16.png')]
ims=[(n,rgba(p)) for n,p in S]
z=8; pad=16
v=Image.new('RGB',(len(ims)*(64*z+pad)+pad,64*z+40),'white'); d=ImageDraw.Draw(v)
for i,(n,im) in enumerate(ims):
    x=pad+i*(64*z+pad); v.paste(op((255,255,255,255),im,z),(x,32)); d.text((x,10),n,fill='black')
v.save('eindkeuring/voor_jordi_ek_8x.png')
# afstand: 1x en 2x op wit en donker
a=Image.new('RGB',(2*(64+128)+60,2*128+30),'white'); d=ImageDraw.Draw(a)
for r,bg in enumerate([(255,255,255,255),(40,44,52,255)]):
    for c,(n,im) in enumerate(ims[:2]):
        x=10+c*(64+128+20); y=10+r*138
        a.paste(op(bg,im,1),(x,y)); a.paste(op(bg,im,2),(x+64+6,y))
a.save('eindkeuring/afstand.png')
