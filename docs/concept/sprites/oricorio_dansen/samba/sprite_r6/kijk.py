# kijk.py npy|png box z out : naast elkaar r4 | huidig | model (zelfde uitsnede)
import sys, numpy as np; from PIL import Image, ImageDraw
from palet import PAL
def img(a):
    im=Image.fromarray(a.astype(np.uint8),'P'); im.putpalette(list(sum(PAL,()))+[0]*(768-48)); return im.convert('RGB')
def kijk(a,box,z,out):
    x0,y0,x1,y1=box; w,h=(x1-x0)*z,(y1-y0)*z
    r4=Image.open('r5_ref.png').convert('RGB')
    m=Image.open('../model/gemini_r10.png').convert('RGB'); k=950.272/64
    mc=m.crop((int(19.3344+x0*k),int(29.216+y0*k),int(19.3344+x1*k),int(29.216+y1*k))).resize((w,h),Image.LANCZOS)
    W=Image.new('RGB',(3*w+40,h+16),(255,255,255)); d=ImageDraw.Draw(W)
    for i,im in enumerate([r4,img(a)]):
        c=im.crop(box).resize((w,h),Image.NEAREST); W.paste(c,(i*(w+20),16))
        for x in range(x0,x1+1,5): d.line([(i*(w+20)+(x-x0)*z,16),(i*(w+20)+(x-x0)*z,h+16)],fill=(120,120,120))
        for y in range(y0 - y0%5 +5,y1,5): d.line([(i*(w+20),16+(y-y0)*z),(i*(w+20)+w,16+(y-y0)*z)],fill=(120,120,120))
    W.paste(mc,(2*(w+20),16)); d.text((2,2),'r5 | r6 | model  box=%s (lijnen per 5)'%(box,),fill='black')
    W.save(out)
if __name__=='__main__':
    src=sys.argv[1]; a=np.load(src) if src.endswith('.npy') else np.array(Image.open(src))
    kijk(a,tuple(map(int,sys.argv[2].split(','))),int(sys.argv[3]),sys.argv[4])
