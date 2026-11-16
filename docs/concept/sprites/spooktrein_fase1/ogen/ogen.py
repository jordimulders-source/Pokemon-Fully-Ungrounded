# Oogvarianten voor de schoorsteenopening (Claude, 16 nov). Basis: ../sprite_r6/sprite.png
from PIL import Image, ImageDraw
import numpy as np
base=np.array(Image.open('../sprite_r6/sprite.png').convert('RGBA'))
C=(0x1e,0x17,0x0e,255); D=(0xd8,0xc8,0xb0,255); W=(0xf0,0xe8,0xd8,255); G=(0x7b,0x79,0x75,255)
inner={21:range(22,26),22:range(20,27),23:range(19,27),24:range(19,26),25:range(18,25),26:range(18,24),27:range(19,22),28:range(20,21)}
def leeg():
    a=base.copy()
    for y,xs in inner.items():
        for x in xs: a[y,x]=C
    return a
V={
 'A_kraal_1x2':  [((20,24),D),((20,25),D),((24,22),D),((24,23),D)],
 'B_blok_2x2':   [((20,24),D),((21,24),D),((20,25),D),((21,25),D),((23,22),D),((24,22),D),((23,23),D),((24,23),D)],
 'C_stip':       [((20,24),D),((24,22),D)],
 'D_ovaal_glans':[((20,24),W),((20,25),D),((21,25),D),((24,22),W),((24,23),D),((25,23),D)],
}
out=[]
for n,px in V.items():
    a=leeg()
    for (x,y),c in px: a[y,x]=c
    Image.fromarray(a).save(f'{n}.png'); out.append((n,a))
S=8; pad=10; cw=64*S
vel=Image.new('RGB',(len(out)*(cw+pad)+pad, 64*S+150),(235,235,235)); d=ImageDraw.Draw(vel)
for i,(n,a) in enumerate(out):
    im=Image.fromarray(a); x0=pad+i*(cw+pad)
    bg=Image.new('RGBA',(64,64),'white'); bg.alpha_composite(im)
    vel.paste(bg.resize((cw,cw),Image.NEAREST),(x0,20)); d.text((x0,5),n,fill=(0,0,0))
    vel.paste(bg,(x0,64*S+30)); vel.paste(bg.resize((128,128),Image.NEAREST),(x0+80,64*S+30))
    dk=Image.new('RGBA',(64,64),(40,44,64,255)); dk.alpha_composite(im); vel.paste(dk,(x0+220,64*S+30))
vel.save('varianten.png')
