# Model op spriteschaal (box-filter), uitgelijnd op de onderlaag (fase 18,0; plek 1,2).
from PIL import Image; import numpy as np
cx=np.load('natief_cx.npy'); cy=np.load('natief_cy.npy')
x0=cx[0]-2.56+5.12*(18-3*1); y0=cy[0]-2.56+5.12*(0-3*2)
im=Image.open('../referenties/gemini_gekozen_r7.png').convert('RGB')
big=Image.new('RGB',(2000,2000),(255,255,255)); big.paste(im,(500,500))
s=15.36; box=(500+x0,500+y0,500+x0+64*s,500+y0+64*s)
r=big.resize((64,64),Image.BOX,box=box); r.save('model64.png')
r.resize((512,512),Image.NEAREST).save('model64_8x.png')
big.crop(tuple(int(round(v)) for v in box)).resize((768,768),Image.LANCZOS).save('model_12x.png')
print(x0,y0)
