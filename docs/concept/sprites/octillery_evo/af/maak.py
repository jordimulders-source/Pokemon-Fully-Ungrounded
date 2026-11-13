# Krassault definitief (Jordi, 13 nov): kleurronde 4, kleur B, pupil linkeroog 2 px. Draaien vanuit deze map.
from PIL import Image
im=Image.open('../sprite3/kleur/r4_B_pupil2.png'); im.save('krassault.png',transparency=0)
rgb=Image.new('RGBA',(64,64),(255,255,255,255)); rgb.alpha_composite(im.convert('RGBA')); rgb.resize((512,512),Image.NEAREST).convert('RGB').save('krassault_8x.png')
print(im.size,im.mode,len(set(im.getdata()))-1,'kleuren')
