# vel r17b | r17 op 8x, daaronder 1x op wit, crème, donker, plus kop-close-up 16x van beide
import numpy as np; from PIL import Image
def rgb(path,bg):
    im=Image.open(path); o=np.asarray(im); pal=np.array(im.getpalette()[:48]).reshape(-1,3)
    img=np.zeros((64,64,3),'uint8'); img[:]=bg
    for k in range(1,16): img[o==k]=pal[k]
    return Image.fromarray(img)
S=['sprite/r17b/capykart.png','sprite/r17/capykart.png']
v=Image.new('RGB',(1040+2*528,760),'white')
for i,p in enumerate(S):
    v.paste(rgb(p,(255,255,255)).resize((512,512),Image.NEAREST),(i*520,0))
    v.paste(rgb(p,(255,255,255)).crop((8,8,41,41)).resize((528,528),Image.NEAREST),(1040+i*528,0))
    for j,bg in enumerate([(255,255,255),(248,248,232),(40,48,56)]): v.paste(rgb(p,bg),(i*240+j*72+8,540))
v.save('sprite/r17b/vel.png'); print(v.size)
