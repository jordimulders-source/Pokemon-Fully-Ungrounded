# r29 = r28A + 1 px: (32,43) terug naar zwart (zonegrens x=33 knipte de wagenplaatlijn; 1 px idx15 vóór een zwarte lijn).
from PIL import Image; import numpy as np
im=Image.open('sprite_r28/sprite_A.png'); a=np.array(im); a[43,32]=1
o=Image.fromarray(a,'P'); o.putpalette(im.getpalette()); o.save('sprite_r29/sprite.png',transparency=0)
def w(f):
    s=Image.open(f).convert('RGBA'); bg=Image.new('RGBA',(64,64),(255,255,255,255)); bg.alpha_composite(s); return bg.convert('RGB')
w('sprite_r29/sprite.png').resize((512,512),Image.NEAREST).save('sprite_r29/sprite_8x.png')
ims=[w(f) for f in ('sprite_r27/sprite.png','sprite_r28/sprite_A.png','sprite_r29/sprite.png')]
v=Image.new('RGB',(3*532,512+150),(235,235,235))
for i,m in enumerate(ims):
    v.paste(m.resize((512,512),Image.NEAREST),(i*532,0)); v.paste(m.resize((128,128),Image.NEAREST),(i*532,520)); v.paste(m,(i*532+140,520))
v.save('sprite_r28/vel_r27_r28A_r29.png')
