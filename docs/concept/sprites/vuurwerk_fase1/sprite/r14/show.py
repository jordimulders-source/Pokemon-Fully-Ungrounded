# 8x-uitsnede naast elkaar: python3 show.py out.png r0 r1 c0 c1 bestand...(png of npy)
import sys,numpy as np; from PIL import Image
pal=Image.open('../r11/sprite.png').getpalette()
out=sys.argv[1]; r0,r1,c0,c1=map(int,sys.argv[2:6]); fs=sys.argv[6:]; Z=24
W=Image.new('RGB',(len(fs)*((c1-c0)*Z+10),(r1-r0)*Z),'white')
for k,f in enumerate(fs):
    a=np.load(f) if f.endswith('.npy') else np.array(Image.open(f))
    im=Image.fromarray(a.astype("uint8"),"P"); im.putpalette(Image.open(f).getpalette() if f.endswith(".png") else pal); rgb=np.array(im.convert('RGB')); rgb[a==0]=255
    W.paste(Image.fromarray(rgb).crop((c0,r0,c1,r1)).resize(((c1-c0)*Z,(r1-r0)*Z),Image.NEAREST),(k*((c1-c0)*Z+10),0))
W.save(out)
