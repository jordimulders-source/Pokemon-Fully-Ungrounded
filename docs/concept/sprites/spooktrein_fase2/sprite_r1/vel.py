# vel: sprite 8x | model verkleind naar dezelfde schaal 8x (zelfde gumwerk/indrukking, LANCZOS) ; 1x en 2x op licht en donker
import sys; from PIL import Image, ImageDraw; import numpy as np
VAR,SP,OUT=sys.argv[1],sys.argv[2],sys.argv[3]
s,X0,Y0,oy,XC,k=[float(v) for v in open(f'basis_{VAR}.meta').read().split()]
a=np.asarray(Image.open('natief.png').convert('RGB')).astype(np.uint8).copy()
for (x0,x1,y0,y1) in ((165,178,112,122),(157,163,123,129),(181,187,124,130),(169,175,129,132)): a[y0:y1+1,x0:x1+1]=255  # zelfde gum
m=Image.fromarray(a)
# staart indrukken zoals de sprite: kolommen rechts van XC horizontaal schalen
L=m.crop((0,0,min(199,int(XC)),199)); R=m.crop((min(199,int(XC)),0,199,199)) if XC<199 else Image.new('RGB',(0,199)); R=R.resize((max(1,round(R.width*k)),199),Image.LANCZOS) if R.width>0 else R
mm=Image.new('RGB',(L.width+R.width,199),'white'); mm.paste(L,(0,0)); mm.paste(R,(L.width,0))
mm=mm.crop((int(X0),int(Y0),mm.width,199)); mm=mm.resize((round(mm.width*s),round(mm.height*s)),Image.LANCZOS)
ref=Image.new('RGB',(64,64),'white'); ref.paste(mm,(0,int(oy)))
sp=Image.open(SP).convert('RGBA')
def on(bg): b=Image.new('RGBA',(64,64),bg); return Image.alpha_composite(b,sp).convert('RGB')
W=512*2+3*16; V=Image.new('RGB',(W,512+16+180),(236,236,236)); d=ImageDraw.Draw(V)
V.paste(on('white').resize((512,512),Image.NEAREST),(16,16)); V.paste(ref.resize((512,512),Image.NEAREST),(512+32,16))
y=512+40; x=16
for bg in ((255,255,255),(40,44,60)):
    V.paste(on(bg+(255,)),(x,y)); x+=80
    V.paste(on(bg+(255,)).resize((128,128),Image.NEAREST),(x,y)); x+=150
V.paste(ref,(x,y)); V.paste(ref.resize((128,128),Image.NEAREST),(x+80,y))
d.text((16,2),f'{SP} 8x  |  model (natief, gegumd, zelfde schaal) 8x',fill=(0,0,0)); d.text((16,512+24),'1x/2x licht, donker | model 1x/2x',fill=(0,0,0))
V.save(OUT)
