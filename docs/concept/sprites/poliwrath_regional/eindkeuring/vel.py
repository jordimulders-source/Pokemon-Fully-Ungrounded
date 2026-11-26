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
ek=rgba('poliwrath_regional_ek.png'); r2=rgba('../sprite_r2/poliwrath_regional_r2_E2M1.png')
# model: gespiegeld + geschrapt op spritemaat (../sprite_r1/geschrapt.npz, op x+1, y+2), elke cel = echte modelcel
z=np.load('../sprite_r1/geschrapt.npz'); g=np.zeros((64,64,4),'uint8'); g[2:62,1:63,:3]=z['N']; g[2:62,1:63,3]=np.where(z['air'],0,255)
mod=Image.fromarray(g)
W=Image.new('RGB',(3*528+16,660),'white'); D=ImageDraw.Draw(W)
for i,(im,n) in enumerate(((ek,'eindkeuring (ek)'),(r2,'r2_E2M1 (invoer)'),(mod,'model (Gemini v2, gespiegeld, geschrapt op spritemaat)'))):
    x=16+i*528; D.text((x,4),n,fill='black'); q=im.resize((512,512),Image.NEAREST); W.paste(q,(x,18),q)
y=540; D.text((16,y),'1x licht / donker: ek, r2_E2M1',fill='black')
for j,bg in enumerate(((255,255,255),(24,24,32))):
    W.paste(Image.new('RGB',(150,72),bg),(16+j*160,y+14))
    for k,im in enumerate((ek,r2)): W.paste(im,(16+j*160+4+k*70,y+18),im)
refs=[(ek,'ek'),(rgba(R+'docs/concept/sprites/poliwhirl_regional/af/poliwhirl_regional.png'),'Poliwhirl reg.'),
 (rgba(R+'graphics/pokemon/poliwrath/anim_front_gba.png',True),'Poliwrath gba'),
 (rgba(R+'docs/concept/sprites/dundragoon/af/dundragoon.png'),'Dundragoon'),(rgba(R+'docs/concept/sprites/awki/af/awki.png'),'Princadee'),
 (rgba(R+'docs/concept/sprites/viscacha/af/viscacha.png'),'Zapacha'),(rgba(R+'docs/concept/sprites/skinguin/af/skinguin.png'),'Skinguin')]
y=660
W2=Image.new('RGB',(max(W.width,16+7*260),y+290),'white'); W2.paste(W,(0,0)); D=ImageDraw.Draw(W2)
for k,(im,n) in enumerate(refs):
    q=im.resize((256,256),Image.NEAREST); W2.paste(q,(16+k*260,y+20),q); D.text((16+k*260,y+4),n+' (4x)',fill='black')
W2.save('vel.png'); print(W2.size)
