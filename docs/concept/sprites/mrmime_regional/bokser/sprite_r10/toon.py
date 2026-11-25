# toon.py uit.png a.npy [b.npy ...] : naast elkaar op 10x met raster (+ model op dezelfde schaal achteraan)
import sys,numpy as np; from PIL import Image, ImageDraw
sys.path.insert(0,'../sprite_r6'); from palet import PAL
Z=10; BG=(232,240,232); fs=sys.argv[2:]
ims=[]
for f in fs:
    a=np.load(f); ims.append(Image.fromarray(np.array([BG]+PAL[1:],'uint8')[a]).resize((a.shape[1]*Z,a.shape[0]*Z),Image.NEAREST))
m=Image.open('natief.png').convert('RGB').crop((12,5,72,93)); a0=np.load(fs[0])
ims.append(m.resize((a0.shape[1]*Z,a0.shape[0]*Z),Image.LANCZOS))
W=max(i.size[0] for i in ims); H=max(i.size[1] for i in ims)
o=Image.new('RGB',(len(ims)*(W+10),H),(255,255,255)); d=ImageDraw.Draw(o)
for k,im in enumerate(ims):
    o.paste(im,(k*(W+10),0)); w,h=im.size
    if im.size[0]==a0.shape[1]*Z:
        for x in range(0,w+1,Z): d.line([(k*(W+10)+x,0),(k*(W+10)+x,h)],fill=(255,0,0) if (x//Z)%5==0 else (205,205,240))
        for y in range(0,h+1,Z): d.line([(k*(W+10),y),(k*(W+10)+w,y)],fill=(255,0,0) if (y//Z)%5==0 else (205,205,240))
o.save(sys.argv[1])
