# Rij: potoo (eind_r3) tussen echte Gen 3-frontsprites, op 1x en 3x, licht en battle-achtig groen.
from PIL import Image
P='/home/user/Pokemon-Fully-Ungrounded/'
namen=['noctowl','xatu','potoo','swellow','drifloon','dusclops']
def laad(n):
    if n=='potoo': im=Image.open(P+'docs/concept/sprites/potoo/eind_r3/potoo.png')
    else:
        im=Image.open(P+f'graphics/pokemon/{n}/anim_front.png') if __import__('os').path.exists(P+f'graphics/pokemon/{n}/anim_front.png') else Image.open(P+f'graphics/pokemon/{n}/front.png')
        im=im.crop((0,0,64,64))
    return im.convert('RGBA') if im.mode!='P' else im.convert('RGBA') if 'transparency' in im.info else im.convert('RGBA')
def zonder_bg(im,n):
    im=im.copy(); px=im.load(); bg=px[0,0] if n!='potoo' else None
    if bg:
        for y in range(64):
            for x in range(64):
                if px[x,y][:3]==bg[:3]: px[x,y]=(0,0,0,0)
    return im
ims=[zonder_bg(laad(n),n) for n in namen]
for z,naam in ((1,'rij_1x.png'),(3,'rij_3x.png')):
    s=Image.new('RGBA',(len(ims)*64*z,2*64*z),(255,255,255,255))
    for i,im in enumerate(ims):
        big=im.resize((64*z,64*z),Image.NEAREST)
        s.alpha_composite(big,(i*64*z,0))
        g=Image.new('RGBA',(64*z,64*z),(160,200,152,255)); g.alpha_composite(big); s.paste(g,(i*64*z,64*z))
    s.convert('RGB').save(P+'docs/concept/sprites/potoo/eindkeuring3/'+naam)
