# r25 = r24 + pixelreparaties eindkeuring r24 (assert op oude index)
from PIL import Image; import numpy as np
im=Image.open('../r24/hoatzin.png'); a=np.array(im)
fix=[((38,59),1,0),((52,60),2,1),((52,61),2,1),((51,60),1,2),((51,61),1,2),((52,22),3,1),
     ((19,9),3,1),((16,8),3,2),((10,11),3,2)]
for (x,y),old,new in fix:
    assert a[y,x]==old,(x,y,a[y,x]); a[y,x]=new
out=Image.fromarray(a.astype(np.uint8),'P'); out.putpalette(im.getpalette()); out.save('hoatzin.png',transparency=0)
s=Image.open('hoatzin.png').convert('RGBA').resize((512,512),Image.NEAREST); bg=Image.new('RGBA',(512,512),(255,255,255,255)); bg.alpha_composite(s); bg.convert('RGB').save('hoatzin_8x.png')
print('ok',len(fix))
