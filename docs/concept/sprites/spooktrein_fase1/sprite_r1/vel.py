# vel: sprite 8x | model (natief, onbewerkt) verkleind op dezelfde maat (LANCZOS) 8x ; 1x/2x op licht en donker
import sys; from PIL import Image, ImageDraw; import numpy as np
NPY=sys.argv[1]; OUT=sys.argv[2]; PNG=sys.argv[3] if len(sys.argv)>3 else None
H=lambda c:[int(c[i:i+2],16) for i in (1,3,5)]
PAL=['#1e170e','#433425','#5f4b3a','#765a43','#9f7e65','#b39b87','#36332b','#4e4a44','#7b7975','#a39b93','#d8c8b0']
P=np.array([H(c) for c in PAL],np.uint8)
o=np.load(NPY)
rgba=np.zeros((64,64,4),np.uint8); rgba[o>0,:3]=P[o[o>0]-1]; rgba[o>0,3]=255
sp=Image.fromarray(rgba,'RGBA')
if PNG:
    sp.save(PNG); sp.convert('RGB').resize((512,512),Image.NEAREST)
    w=Image.new('RGB',(64,64),'white'); w.paste(sp,(0,0),sp); w.resize((512,512),Image.NEAREST).save(PNG.replace('.png','_8x.png'))
X,Y,ww,hh=[int(t) for t in open('plaats.txt').read().split()]
m=Image.open('natief.png').convert('RGB'); a=np.asarray(m); fg=a.min(2)<225; ys,xs=np.where(fg)
mm=m.crop((xs.min(),ys.min(),xs.max()+1,ys.max()+1)).resize((ww,hh),Image.LANCZOS)
ref=Image.new('RGB',(64,64),'white'); ref.paste(mm,(X,Y))
def on(bg): b=Image.new('RGBA',(64,64),bg); return Image.alpha_composite(b,sp).convert('RGB')
V=Image.new('RGB',(512*2+48+256+16,512+16+190),(236,236,236)); d=ImageDraw.Draw(V)
V.paste(on((255,255,255,255)).resize((512,512),Image.NEAREST),(16,16)); V.paste(ref.resize((512,512),Image.NEAREST),(512+32,16))
y=512+44; x=16
for bg in ((255,255,255),(40,44,60)):
    V.paste(on(bg+(255,)),(x,y)); x+=80
    V.paste(on(bg+(255,)).resize((128,128),Image.NEAREST),(x,y)); x+=150
V.paste(ref,(x,y)); V.paste(ref.resize((128,128),Image.NEAREST),(x+80,y))
import os
if os.path.exists('kaal.npy'):
    k=np.load('kaal.npy'); kr=np.full((64,64,3),255,np.uint8); kr[k>0]=P[k[k>0]-1]
    V.paste(Image.fromarray(kr).resize((256,256),Image.NEAREST),(512*2+48,16)); d.text((512*2+48,276),'kale reductie (zonder samenvoegen) 4x',fill=(0,0,0))
d.text((16,2),f'{NPY} 8x  |  model (natief) verkleind op dezelfde maat 8x',fill=(0,0,0)); d.text((16,512+26),'sprite 1x/2x licht, donker | model 1x/2x',fill=(0,0,0))
V.save(OUT)
