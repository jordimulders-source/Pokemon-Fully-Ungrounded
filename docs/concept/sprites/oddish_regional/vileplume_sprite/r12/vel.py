# r11/vel.py (vanuit vileplume_sprite/): vel.png = r11 8x | r10 8x | model 8x / 12x VL, VR, linkerpoot, gezicht
# (sprite | r10 | model) / 1x; vel_ogen.png = oogopties A/B/C op 1x en 8x, gezicht 12x.
import sys, numpy as np; from PIL import Image, ImageDraw
sys.path.insert(0,'gereedschap'); from gemeen import *
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
def rij(panelen,gap=8):
    W=sum(p.width for p in panelen)+gap*(len(panelen)-1); H=max(p.height for p in panelen)
    r=Image.new('RGB',(W,H),'white'); x=0
    for p in panelen: r.paste(p,(x,0)); x+=p.width+gap
    return r
def kolom(rijen,gap=10):
    W=max(p.width for p in rijen); H=sum(p.height for p in rijen)+gap*(len(rijen)-1)
    r=Image.new('RGB',(W,H),'white'); y=0
    for p in rijen: r.paste(p,(0,y)); y+=p.height+gap
    return r
R11,R10='r12/vileplume_r12.png','r11/vileplume_r11.png'
s11,s10=rgb_from(R11),rgb_from(R10)
boven=rij([kop(s11.resize((512,512),Image.NEAREST),'r12 8x'),kop(s10.resize((512,512),Image.NEAREST),'r11 8x'),kop(model_op_schaal(8),'model 8x')])
z=12; zones=[('T + L (gaatje)',8,0,48,14),('VL',8,10,38,32),('VR',32,8,58,31),('gezicht',16,28,44,38)]
rijen=[]
for n,x0,y0,x1,y1 in zones:
    a=raster(s11.crop((x0,y0,x1,y1)).resize(((x1-x0)*z,(y1-y0)*z),Image.NEAREST),z)
    b=raster(s10.crop((x0,y0,x1,y1)).resize(((x1-x0)*z,(y1-y0)*z),Image.NEAREST),z)
    rijen.append(rij([kop(a,'%s r12 x%d-%d y%d-%d'%(n,x0,x1-1,y0,y1-1)),kop(b,'r11'),kop(model_crop(x0,y0,x1,y1,z),'model')]))
een=rij([kop(s11,'r12'),kop(rgb_from(R11,(40,48,56)),''),kop(s10,'r11'),kop(model_op_schaal(1),'model')])
g=Image.open('../../../../../graphics/pokemon/vileplume/anim_front.png').convert('RGBA').crop((0,0,64,64))
gb=Image.new('RGBA',(64,64),(255,255,255,255)); gb.alpha_composite(Image.open('../../../../../graphics/pokemon/vileplume/anim_front.png').convert('RGBA').crop((0,0,64,64)))
ga=np.asarray(Image.open('../../../../../graphics/pokemon/vileplume/anim_front.png'))[:64]; gp=np.array(Image.open('../../../../../graphics/pokemon/vileplume/anim_front.png').getpalette()[:48]).reshape(-1,3)
gi=np.zeros((64,64,3),'uint8'); gi[:]=255
for k in range(1,16): gi[ga==k]=gp[k]
gi=Image.fromarray(gi)
gz=rij([kop(raster(s11.crop((18,28,36,37)).resize((18*z,9*z),Image.NEAREST),z),'r12 gezicht 12x'),
        kop(raster(gi.crop((19,32,37,41)).resize((18*z,9*z),Image.NEAREST),z),'Vileplume (game) gezicht 12x'),
        kop(s11,'r12 1x'),kop(gi,'Vileplume 1x')])
kolom([boven,rijen[0],rij([rijen[1],rijen[2]],16),rijen[3],gz,een]).save('r12/vel.png')
import sys; sys.exit()
# oogopties
opt=[('A','r11/vileplume_r11_ogenA.png'),('B','r11/vileplume_r11_ogenB.png'),('C','r11/vileplume_r11_ogenC.png')]
r1=rij([kop(rgb_from(p),k) for k,p in opt]+[kop(rgb_from(R10),'r10'),kop(model_op_schaal(1),'model')])
r8=rij([kop(rgb_from(p).resize((512,512),Image.NEAREST).crop((96,192,416,352)),'%s 8x'%k) for k,p in opt])
x0,y0,x1,y1=18,28,36,37
r12=rij([kop(raster(rgb_from(p).crop((x0,y0,x1,y1)).resize(((x1-x0)*z,(y1-y0)*z),Image.NEAREST),z),'%s gezicht 12x'%k) for k,p in opt]
        +[kop(raster(s10.crop((x0,y0,x1,y1)).resize(((x1-x0)*z,(y1-y0)*z),Image.NEAREST),z),'r10'),kop(model_crop(x0,y0,x1,y1,z),'model')])
kolom([r1,r8,r12]).save('r11/vel_ogen.png')
print('ok')
