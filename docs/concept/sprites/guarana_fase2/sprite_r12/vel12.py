# voor_jordi_r12_8x.png = fase 1 | r12 | r11 (8x, wit); afstand.png = fase 1 | r12 | r11 op 1x, daarna op 2x
from PIL import Image
def w(f):
    a=Image.open(f); a.info['transparency']=0; a=a.convert('RGBA'); B=Image.new('RGBA',a.size,(255,255,255,255)); B.alpha_composite(a); return B.convert('RGB')
F=[w('../guarana/af/guarana.png'),w('sprite_r12/guarana2_r12.png'),w('sprite_r11/guarana2_r11.png')]
T=Image.new('RGB',(3*512+32,512),'white')
for i,im in enumerate(F): T.paste(im.resize((512,512),0),(i*528,0))
T.save('sprite_r12/voor_jordi_r12_8x.png')
T=Image.new('RGB',(3*72+3*136+8,136),'white'); x=4
for s in (1,2):
    for im in F: T.paste(im.resize((64*s,64*s),0),(x,4)); x+=64*s+8
T.save('sprite_r12/afstand.png')
