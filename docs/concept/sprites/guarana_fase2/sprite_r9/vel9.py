# voor_jordi_r8_8x.png = r9a | r9b | r8a op 8x, wit
from PIL import Image
def p8(f):
    a=Image.open(f); a.info['transparency']=0; a=a.convert('RGBA'); B=Image.new('RGBA',a.size,(255,255,255,255)); B.alpha_composite(a)
    return B.convert('RGB').resize((512,512),0)
T=Image.new('RGB',(1568,512),'white')
for i,f in enumerate(('sprite_r9/guarana2_r9a.png','sprite_r9/guarana2_r9b.png','sprite_r8/guarana2_r8a.png')): T.paste(p8(f),(i*528,0))
T.save('sprite_r9/voor_jordi_r9_8x.png')
