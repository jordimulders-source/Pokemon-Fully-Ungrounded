# zoommodel.py x0 y0 x1 y1 (figuurcoörd) uit.png [schaal] : model met spritecelraster + labels
import sys
from PIL import Image, ImageDraw
R='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/capybarrel/'
x0,y0,x1,y1=map(int,sys.argv[1:5]); Z=int(sys.argv[6]) if len(sys.argv)>6 else 3
p=738/46; mx=143; my1=799; H=34
X0=mx+x0*p; X1=mx+x1*p; Y0=my1-(H-y0)*p; Y1=my1-(H-y1)*p
im=Image.open(R+'referenties/model_r3.png').convert('RGB').crop((int(X0),int(Y0),int(X1),int(Y1)))
im=im.resize((im.width*Z,im.height*Z),Image.NEAREST); d=ImageDraw.Draw(im)
for i in range(x0,x1+1):
    x=(mx+i*p-int(X0))*Z; d.line([(x,0),(x,im.height)],fill=(0,200,255)); d.text((x+2,2),str(i),fill=(0,0,255))
for j in range(y0,y1+1):
    y=(my1-(H-j)*p-int(Y0))*Z; d.line([(0,y),(im.width,y)],fill=(0,200,255)); d.text((2,y+2),str(j),fill=(0,0,255))
im.save(sys.argv[5])
