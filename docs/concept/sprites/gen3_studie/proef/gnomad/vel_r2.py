from PIL import Image
import os
D = os.path.dirname(os.path.abspath(__file__)); G = os.path.join(D,'../../../../../../graphics/pokemon')
imgs = [Image.open(os.path.join(D,p)).convert('RGBA') for p in ('../../../gnomad/af/gnomad.png','na.png','na_r2.png')]
for s in ('makuhita','jigglypuff'):
    imgs.append(Image.open(os.path.join(G,s,'anim_front_gba.png')).convert('RGBA').crop((0,0,64,64)))
S=6; W=len(imgs)*64*S+(len(imgs)+1)*8
vel = Image.new('RGBA',(W,64*S+16+64+8),(255,255,255,255))
for i,im in enumerate(imgs):
    x = 8+i*(64*S+8)
    vel.alpha_composite(im.resize((64*S,64*S),0),(x,8)); vel.alpha_composite(im,(x,64*S+16))
vel.convert('RGB').save(os.path.join(D,'voor_na_r2.png'))
