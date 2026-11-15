# Model-mockups Gengas: lijf bevroren uit Gemini r5 (natief raster), ledematen als losse onderdelen verschoven.
from PIL import Image, ImageDraw; import numpy as np, sys, json
S=sys.argv[1]; sys.path.insert(0,S); from seg import label
a=np.asarray(Image.open(S+'/n10.png').convert('RGB')).astype(int)
cls=np.load(S+'/cls.npy'); lab=np.load(S+'/lab.npy'); H,W=cls.shape
limbs={}
names={1:'A',8:'B',7:'C',11:'D'}
for k,nm in names.items():
    m=lab==k; ys,xs=np.where(m)
    limbs[nm]=(a[ys.min():ys.max()+1,xs.min():xs.max()+1].copy(), m[ys.min():ys.max()+1,xs.min():xs.max()+1].copy(), (xs.min(),ys.min()))
# lijf = alles wat geen grote ledemaatcomponent is (tanden horen bij het lijf), gaten gevuld
bg=a.min(axis=2)>=232
limbmask=np.isin(lab,list(names.keys()))
body=~limbmask
out_lab,n=label(~body| False)  # placeholder
# buitenkant = achtergrond verbonden met de rand
outside=np.zeros_like(bg); 
reach=bg|limbmask
l2,n2=label(reach)
edge=set(l2[0,:])|set(l2[-1,:])|set(l2[:,0])|set(l2[:,-1]); edge.discard(0)
outside=np.isin(l2,list(edge))
body=~outside
OUT=(28,12,20)
ba=a.copy()
# lijfrand herstellen waar een ledemaat ertegenaan lag
for y,x in zip(*np.where(body)):
    nb=[(y+1,x),(y-1,x),(y,x+1),(y,x-1)]
    if any(0<=yy<H and 0<=xx<W and outside[yy,xx] for yy,xx in nb) and (0.299*a[y,x,0]+0.587*a[y,x,1]+0.114*a[y,x,2])>60:
        if limbmask[max(0,y-2):y+3,max(0,x-2):x+3].any(): ba[y,x]=OUT
body=np.load(S+'/body2.npy'); ba=np.load(S+'/ba2.npy')
def render(spec,C=140):
    cv=np.full((C,C,3),255,int); ox,oy=spec.get('body',(15,10))
    def put(nm,x,y,dark):
        img,m,_=limbs[nm]; h,w=m.shape
        if spec.get('flip_'+nm): img=img[:,::-1]; m=m[:,::-1]
        sub=img.copy()
        if dark: sub=(sub*0.72).astype(int)
        reg=cv[y:y+h,x:x+w]; reg[m]=sub[m]
    for nm,(x,y,lay) in spec['limbs'].items():
        if lay=='achter': put(nm,x,y,True)
    reg=cv[oy:oy+H,ox:ox+W]; reg[body]=ba[body]
    for nm,(x,y,lay) in spec['limbs'].items():
        if lay!='achter': put(nm,x,y,False)
    fg=cv.min(axis=2)<232; ys,xs=np.where(fg)
    x0,x1,y0,y1=xs.min(),xs.max(),ys.min(),ys.max(); side=max(x1-x0+1,y1-y0+1)
    return cv.astype('uint8'),(x0,y0,side)
specs=json.load(open(S+'/specs.json'))
tiles=[]
from PIL import ImageFont
for nm,spec in specs.items():
    im,(x0,y0,side)=render(spec)
    scale=64/side
    crop=Image.fromarray(im).crop((x0,y0,x0+side,y0+side))
    small=crop.resize((64,64),Image.BOX)
    T=Image.new('RGB',(560,640),'white'); T.paste(crop.resize((side*5,side*5),Image.NEAREST),(10,40))
    T.paste(small.resize((128,128),Image.NEAREST),(10+side*5-128,500)); T.paste(small,(10,530))
    d=ImageDraw.Draw(T); d.text((10,10),f"{nm}  (lijf {round(scale*100)}% van het model)",fill=(0,0,0))
    d.text((80,560),"64x64 en 2x",fill=(90,90,90))
    tiles.append(T)
vel=Image.new('RGB',(1120,1280),'white')
for i,t in enumerate(tiles): vel.paste(t,((i%2)*560,(i//2)*640))
vel.save(sys.argv[2] if len(sys.argv)>2 else S+'/vel.png'); print('ok')
