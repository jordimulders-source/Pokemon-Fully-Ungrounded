# voor_jordi_r10_8x.png = r10a | r9a | fase 1 op 8x, wit; afstand.png via afstand.py
from PIL import Image
def p8(f):
    a=Image.open(f); a.info['transparency']=0; a=a.convert('RGBA'); B=Image.new('RGBA',a.size,(255,255,255,255)); B.alpha_composite(a)
    return B.convert('RGB').resize((512,512),0)
T=Image.new('RGB',(1568,512),'white')
for i,f in enumerate(('sprite_r10/guarana2_r10a.png','sprite_r9/guarana2_r9a.png','../guarana/af/guarana.png')): T.paste(p8(f),(i*528,0))
T.save('sprite_r10/voor_jordi_r10_8x.png')
