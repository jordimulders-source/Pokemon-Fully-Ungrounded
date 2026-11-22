import sys; sys.path.insert(0,'gereedschap'); from r4lib import rgba
from PIL import Image, ImageDraw
def op(c,bg,zz):
    b=Image.new('RGBA',c.size,bg+(255,)); b.alpha_composite(c); return b.convert('RGB').resize((c.width*zz,c.height*zz),Image.NEAREST)
half=(20,40,49,64); full=(15,26,50,64); z=10
L={'A':'A  model: breed, korte kegel','B':'B  zuivere spits (2:1)','C':'C  kleine ruit'}
W=(half[2]-half[0])*z; H=(half[3]-half[1])*z; fw,fh=full[2]-full[0],full[3]-full[1]
vel=Image.new('RGB',(3*(W+30)+20,H+60+2*fh+30),(255,255,255)); d=ImageDraw.Draw(vel)
for i,k in enumerate('ABC'):
    im=rgba(Image.open(f'sprite_r14/baltoy_r14{k}.png')); x=20+i*(W+30); d.text((x,10),L[k],fill=(0,0,0))
    vel.paste(op(im.crop(half),(255,255,255),z),(x,30)); f=im.crop(full); y=H+45
    vel.paste(op(f,(255,255,255),1),(x,y)); vel.paste(op(f,(255,255,255),2),(x+fw+6,y)); vel.paste(op(f,(48,48,56),1),(x+3*fw+16,y)); vel.paste(op(f,(48,48,56),2),(x+4*fw+22,y))
vel.save('sprite_r14/keuze.png')
