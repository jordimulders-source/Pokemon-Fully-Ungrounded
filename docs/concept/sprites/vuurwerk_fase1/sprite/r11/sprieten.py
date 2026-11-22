# r11 = r10 B (zonder krullen) + alleen de sprieten uit Gemini r11 (r11/gemini_sprieten.png, 16 px per spritepixel).
# Gemini-pixels: celmidden, dichtstbijzijnde kleur uit het r10-palet; alleen overgenomen in twee zones (sprietje boven, kieuwen rechts).
from PIL import Image
import numpy as np
B=Image.open('../r10/sprite_zonder.png'); pal=np.array(B.getpalette()[:48]).reshape(16,3); b=np.array(B)
g=np.array(Image.open('../../r11/gemini_sprieten.png').convert('RGB')).astype(int)
c=g[8::16,8::16]; white=c.min(axis=2)>225
d=((c[:,:,None,:]-pal[None,None,:,:])**2).sum(-1); d[:,:,0]=10**9
idx=d.argmin(-1); idx[white]=0
out=b.copy(); zone=np.zeros_like(b,bool)
zone[2:9,30:36]=True      # sprietje boven
zone[12:23,42:51]=True    # kieuwen rechts
out[zone]=idx[zone]
print('gewijzigd',(out!=b).sum())
im=Image.fromarray(out.astype(np.uint8),'P'); im.putpalette(B.getpalette()); im.save('sprite.png',transparency=0)
a=Image.open('sprite.png').convert('RGBA'); bg=Image.new('RGBA',(64,64),(255,255,255,255)); bg.alpha_composite(a)
bg.resize((512,512),Image.NEAREST).convert('RGB').save('r11_8x.png')
