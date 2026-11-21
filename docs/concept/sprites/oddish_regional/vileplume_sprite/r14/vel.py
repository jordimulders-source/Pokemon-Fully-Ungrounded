# r13/vel.py (vanuit vileplume_sprite/): r13 | r12 | model 8x / poten dik|dun 8x en 1x / 12x gat en lijnen (r13 | r12 | model)
import sys, numpy as np; from PIL import Image, ImageDraw
sys.path.insert(0,'gereedschap'); from gemeen import *
sys.path.insert(0,'r11'); 
def rgb_from(path,bg=(255,255,255)):
    im=Image.open(path); o=np.asarray(im); pal=np.array(im.getpalette()[:48]).reshape(-1,3)
    img=np.zeros((64,64,3),'uint8'); img[:]=bg
    for k in range(1,16): img[o==k]=pal[k]
    return Image.fromarray(img)
def raster(a,z):
    d=ImageDraw.Draw(a)
    for x in range(0,a.width+1,z): d.line([(x,0),(x,a.height)],fill=(225,225,225))
    for y in range(0,a.height+1,z): d.line([(0,y),(a.width,y)],fill=(225,225,225))
    return a
def kop(img,t):
    r=Image.new('RGB',(img.width,img.height+14),'white'); r.paste(img,(0,14)); ImageDraw.Draw(r).text((2,1),t,fill=(0,0,0)); return r
def rij(p,g=8):
    r=Image.new('RGB',(sum(i.width for i in p)+g*(len(p)-1),max(i.height for i in p)),'white'); x=0
    for i in p: r.paste(i,(x,0)); x+=i.width+g
    return r
def kolom(p,g=10):
    r=Image.new('RGB',(max(i.width for i in p),sum(i.height for i in p)+g*(len(p)-1)),'white'); y=0
    for i in p: r.paste(i,(0,y)); y+=i.height+g
    return r
A,B='r14/vileplume_r14.png','r13/vileplume_r13.png'
a,b=rgb_from(A),rgb_from(B)
boven=rij([kop(a.resize((512,512),Image.NEAREST),'r14 8x'),kop(b.resize((512,512),Image.NEAREST),'r13 8x'),kop(model_op_schaal(8),'model 8x')])
z=12; rijen=[]
for n,x0,y0,x1,y1 in [('naad VL|VR',28,16,44,31),('poten',18,40,44,64)]:
    rijen.append(rij([kop(raster(s_.crop((x0,y0,x1,y1)).resize(((x1-x0)*z,(y1-y0)*z),Image.NEAREST),z),t) for s_,t in ((a,'r14 '+n),(b,'r13'))]+[kop(model_crop(x0,y0,x1,y1,z),'model')]))
een=rij([kop(a,'r14 1x'),kop(rgb_from(A,(40,48,56)),''),kop(b,'r13 1x'),kop(model_op_schaal(1),'model')])
kolom([boven,rijen[0],rijen[1],een]).save('r14/vel.png'); print('ok')
