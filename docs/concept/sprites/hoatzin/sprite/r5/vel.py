# vel.png: r5 | r4 | model op schaal (8x); daaronder 1x op wit en donker: r5, r4, model, Murkrow (gba); hoatzin_r5_8x.png
import sys,os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'../r4'))
from gemeen import model_op_schaal
from PIL import Image, ImageDraw
import numpy as np
H=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.join(H,'../../../../../..')
def plat(im,bg):
    im=im.convert('RGBA'); out=Image.new('RGBA',im.size,bg+(255,)); out.alpha_composite(im); return out.convert('RGB')
r5=Image.open(H+'/hoatzin_r5.png'); r4=Image.open(H+'/../r4/hoatzin_r4.png'); m=model_op_schaal()
mk=Image.open(ROOT+'/graphics/pokemon/murkrow/anim_front_gba.png').crop((0,0,64,64))
L=open(ROOT+'/graphics/pokemon/murkrow/normal_gba.pal').read().split('\n')[3:]; pl=[int(v) for l in L if l.strip() for v in l.split()]
mk.putpalette(pl); mk=mk.convert('RGBA'); a=np.array(mk); a[...,3]=np.where((a[...,:3]==pl[:3]).all(-1),0,255); mk=Image.fromarray(a)
plat(r5,(255,255,255)).resize((512,512),0).save(H+'/hoatzin_r5_8x.png')
W=Image.new('RGB',(3*512+2*8,512+20+2*(64*2+8)+8),(200,200,200)); d=ImageDraw.Draw(W)
for i,(im,n) in enumerate([(plat(r5,(255,255,255)),'r5'),(plat(r4,(255,255,255)),'r4'),(m,'model')]):
    W.paste(im.resize((512,512),0),(i*520,20)); d.text((i*520+4,4),n+' 8x',fill=(0,0,0))
y0=540
for j,bg in enumerate([(255,255,255),(40,40,48)]):
    for i,im in enumerate([r5,r4,None,mk]):
        x=i*140+8; y=y0+j*144
        if im is None: W.paste(m.resize((128,128),0) if False else m,(x,y)); continue
        W.paste(plat(im,bg),(x,y)); W.paste(plat(im,bg).resize((128,128),0),(x+560,y))
d.text((8,y0-14),'1x: r5 | r4 | model | Murkrow (gba)   --   2x: r5 | r4 | . | Murkrow',fill=(0,0,0))
W.save(H+'/vel.png'); print(W.size)
