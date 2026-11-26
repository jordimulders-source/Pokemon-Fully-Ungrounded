import numpy as np
from PIL import Image, ImageDraw
R='/home/user/Pokemon-Fully-Ungrounded/'
def rgba(f,gba=False):
    im=Image.open(f)
    if gba:
        L=open(f.replace('anim_front_gba.png','normal_gba.pal')).read().split()[3:]
        im.putpalette([int(x) for x in L[:48]]+[0]*720)
    im=im.crop((0,0,64,64)); im.info['transparency']=0
    return im.convert('RGBA')
ek=rgba('poliwhirl_regional_ek.png'); r6=rgba('../sprite_r6/poliwhirl_regional_r6_B.png')
d=np.load('../sprite_r4/reductie.npz'); xs,ys=d['xs'],d['ys']; P=15.36
m0=Image.open('../referenties/gemini_gekozen_v1.png').convert('RGBA'); m=Image.new('RGBA',(1400,1400),'white'); m.paste(m0,(200,200))
l=xs[0]-7*P+200; t=ys[0]-12*P+200; mod=m.crop((int(l),int(t),int(l+64*P),int(t+64*P))).resize((512,512),Image.LANCZOS)
W=Image.new('RGB',(3*528+16,1000),'white'); D=ImageDraw.Draw(W)
for i,(im,n) in enumerate(((ek,'eindkeuring (ek)'),(r6,'r6_B (invoer)'),(None,'model (Gemini v1)'))):
    x=16+i*528; D.text((x,4),n,fill='black')
    if im is None: W.paste(mod,(x,18))
    else: q=im.resize((512,512),Image.NEAREST); W.paste(q,(x,18),q)
# 1x licht / donker
y=540; D.text((16,y),'1x licht / donker: ek, r6_B',fill='black')
for j,bg in enumerate(((255,255,255),(24,24,32))):
    W.paste(Image.new('RGB',(150,72),bg),(16+j*160,y+14))
    for k,im in enumerate((ek,r6)): W.paste(im,(16+j*160+4+k*70,y+18),im)
# 4x rij
refs=[(ek,'ek'),(rgba(R+'docs/concept/sprites/poliwag_regional/af/poliwag_regional.png'),'Poliwag reg.'),
 (rgba(R+'graphics/pokemon/poliwhirl/anim_front_gba.png',True),'Poliwhirl gba'),(rgba(R+'graphics/pokemon/poliwrath/anim_front_gba.png',True),'Poliwrath gba'),
 (rgba(R+'docs/concept/sprites/dundragoon/af/dundragoon.png'),'Dundragoon'),(rgba(R+'docs/concept/sprites/awki/af/awki.png'),'Princadee'),
 (rgba(R+'docs/concept/sprites/viscacha/af/viscacha.png'),'Zapacha'),(rgba(R+'docs/concept/sprites/skinguin/af/skinguin.png'),'Skinguin')]
y=650
W2=Image.new('RGB',(16+8*260,y+290),'white'); W2.paste(W.crop((0,0,W.width,y)),(0,0)); D=ImageDraw.Draw(W2)
for k,(im,n) in enumerate(refs):
    q=im.resize((256,256),Image.NEAREST); W2.paste(q,(16+k*260,y+20),q); D.text((16+k*260,y+4),n+' (4x)',fill='black')
W2.save('vel.png'); print(W2.size)
