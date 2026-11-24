import os,numpy as np; from PIL import Image,ImageDraw
H=os.path.dirname(os.path.abspath(__file__))
def rgba(p):
    im=Image.open(p); a=np.array(im); o=im.convert('RGBA'); o.putalpha(Image.fromarray(((a!=0)*255).astype(np.uint8))); return o
N=rgba(os.path.join(H,'claydol_eind_r2.png')); E=rgba(os.path.join(H,'../claydol_eind.png'))
V=Image.new('RGBA',(1100,1000),(255,255,255,255)); d=ImageDraw.Draw(V)
def put(im,x,y,z,bg=None):
    im=im.resize((im.width*z,im.height*z),Image.NEAREST)
    if bg: V.paste(Image.new('RGBA',im.size,bg),(x,y))
    V.alpha_composite(im,(x,y))
d.text((10,5),'r2 (8x)',fill='black'); put(N,10,20,8); d.text((540,5),'eind (8x)',fill='black'); put(E,540,20,8)
for j,im in enumerate((N,E)):
    d.text((10+j*540,545),'voeten 12x '+('r2' if j==0 else 'eind'),fill='black'); put(im.crop((19,50,46,61)),10+j*540,560,12)
for i,bg in enumerate([(255,255,255,255),(40,40,48,255)]):
    put(N,10+i*80,720,1,bg); put(E,10+i*80,800,1,bg)
d.text((10,705),'1x r2 / eind',fill='black')
put(N,200,720,2,(232,232,232,255)); put(E,340,720,2,(232,232,232,255)); d.text((200,705),'2x r2 | eind',fill='black')
V.crop((0,0,1080,880)).convert('RGB').save(os.path.join(H,'vel.png'))
