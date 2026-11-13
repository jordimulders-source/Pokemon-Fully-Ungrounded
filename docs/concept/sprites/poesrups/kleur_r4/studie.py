"""studie.py: palet + luma + pixelaantallen van de bestudeerde Gen 3-sprites; studievel op 6x."""
import os
from PIL import Image
G='/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/'
S='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/'
H=os.path.dirname(os.path.abspath(__file__))
L=[('swablu',G+'swablu/anim_front_gba.png'),('altaria',G+'altaria/anim_front_gba.png'),('mareep',G+'mareep/anim_front_gba.png'),
   ('seel',G+'seel/anim_front_gba.png'),('dewgong',G+'dewgong/anim_front_gba.png'),('silcoon',G+'silcoon/anim_front_gba.png'),
   ('cascoon',G+'cascoon/anim_front_gba.png'),('wurmple',G+'wurmple/anim_front_gba.png'),('swinub',G+'swinub/anim_front_gba.png'),
   ('castform',G+'castform/front_gba.png'),('poedellarve',S+'poedellarve/af/poedellarve.png'),('poedelmot',S+'poedelmot/af/poedelmot.png')]
def fr(p):
    im=Image.open(p); return im.crop((0,0,64,64))
if __name__=='__main__':
    V=Image.new('RGB',(6*64*4,6*64*3),(232,232,224))
    for i,(n,p) in enumerate(L):
        im=fr(p); pal=im.getpalette(); cnt=im.getcolors()
        print(n, im.mode, Image.open(p).size)
        for c,ix in sorted(cnt,key=lambda t:t[1]):
            r,g,b=pal[ix*3:ix*3+3]; print(f'   {ix:2d} ({r:3d},{g:3d},{b:3d}) luma {0.3*r+0.59*g+0.11*b:5.0f}  {c:4d}px')
        rg=im.convert('RGBA'); px=rg.load(); bg=pal[0:3]
        for y in range(64):
            for x in range(64):
                if im.getpixel((x,y))==0: px[x,y]=(232,232,224,255)
        V.paste(rg.convert('RGB').resize((384,384),Image.NEAREST),((i%4)*384,(i//4)*384))
    V.save(os.path.join(H,'studie_vel.png'))
