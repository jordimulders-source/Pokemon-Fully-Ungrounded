# render npy-indexkaarten (front-palet) naast elkaar op 8x
import sys,numpy as np; from PIL import Image
pal=Image.open('../../af/shuppetto.png').getpalette()
ims=[]
for f in sys.argv[2:]:
    o=np.load(f); im=Image.fromarray(o.astype('uint8'),'P'); im.putpalette(pal); im=im.convert('RGB')
    ims.append(im.resize((o.shape[1]*8,o.shape[0]*8),Image.NEAREST))
W=sum(i.width+16 for i in ims); H=max(i.height for i in ims)
v=Image.new('RGB',(W,H),(152,208,160)); x=0
for i in ims: v.paste(i,(x,0)); x+=i.width+16
v.save(sys.argv[1])
