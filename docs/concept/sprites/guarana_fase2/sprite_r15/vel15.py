# voor_jordi_r15_8x.png (fase 1 | r15 | r14, 8x, wit) en afstand.png (fase 1 | r15 | r14 op 1x en 2x)
from PIL import Image
def w(f):
    a=Image.open(f); a.info['transparency']=0; a=a.convert('RGBA'); B=Image.new('RGBA',a.size,(255,255,255,255)); B.alpha_composite(a); return B.convert('RGB')
F=[w('../guarana/af/guarana.png'),w('sprite_r15/guarana2_r15.png'),w('sprite_r14/guarana2_r14.png')]
T=Image.new('RGB',(3*512+32,512),'white')
for i,im in enumerate(F): T.paste(im.resize((512,512),0),(i*528,0))
T.save('sprite_r15/voor_jordi_r15_8x.png')
T=Image.new('RGB',(3*72+3*136+8,136),'white'); x=4
for s in (1,2):
    for im in F: T.paste(im.resize((64*s,64*s),0),(x,4)); x+=64*s+8
T.save('sprite_r15/afstand.png')
