# Keurder r3: close-up lijf (x0-40,y20-64) sprite en model op 12x naast elkaar
from PIL import Image
spr=Image.open('../r3.png').convert('RGBA'); b=Image.new('RGBA',spr.size,(255,255,255,255)); b.alpha_composite(spr); spr=b.convert('RGB')
mod=Image.open('model3x_r2.png').convert('RGB')
box=(0,18,44,64); s=12
a=spr.crop(box); m=mod.crop(box)
W=Image.new('RGB',(a.width*s*2+20,a.height*s),(255,255,255))
W.paste(m.resize((a.width*s,a.height*s),0),(0,0)); W.paste(a.resize((a.width*s,a.height*s),0),(a.width*s+20,0))
W.save('kop_r3_12x.png')
