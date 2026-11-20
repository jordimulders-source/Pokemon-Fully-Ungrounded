# r24 = r23 + pixelreparaties keurder r23 (per pixel, assert op oude index)
from PIL import Image; import numpy as np
im=Image.open('../r23/hoatzin.png'); a=np.array(im)
fix=[((29,50),11,1),((31,50),11,1),((15,31),1,2),((16,32),1,2),((17,36),1,2),((18,38),1,11),((21,48),12,11),((27,18),1,6),((28,18),1,6)]
for (x,y),old,new in fix:
    assert a[y,x]==old,(x,y,a[y,x]); a[y,x]=new
out=Image.fromarray(a.astype(np.uint8),'P'); out.putpalette(im.getpalette()); out.save('hoatzin.png',transparency=0)
s=Image.open('hoatzin.png').convert('RGBA').resize((512,512),Image.NEAREST); bg=Image.new('RGBA',(512,512),(255,255,255,255)); bg.alpha_composite(s); bg.convert('RGB').save('hoatzin_8x.png')
print('ok',len(fix))
