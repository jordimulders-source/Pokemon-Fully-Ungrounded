import sys
sys.path.insert(0,'../k1')
from gereedschap import *
from PIL import Image, ImageDraw
def rgba(a,pal):
    R=rgb(a,pal).astype('uint8'); A=np.where(a==0,0,255).astype('uint8')
    return Image.fromarray(np.dstack([R,A]),'RGBA')
def op(im,c=(255,255,255)):
    bg=Image.new('RGB',im.size,c); bg.paste(im,(0,0),im); return bg
a14,pal=laad('../k14/tempel.png'); a,pal2=laad('tempel.png')
k14,k15=rgba(a14,pal),rgba(a,pal2)
op(k15.resize((512,512),Image.NEAREST)).save('tempel_8x.png')
X0,Y0,X1,Y1=34,0,56,14; S=14
W=Image.new('RGB',(3*(X1-X0)*S+40,(Y1-Y0)*S+30+512+20+80),(236,236,236)); d=ImageDraw.Draw(W)
d.text((10,4),'top 14x (x%d-%d, y%d-%d): k14 | k15 | model (zelfde uitsnede)'%(X0,X1-1,Y0,Y1-1),fill=(0,0,0))
for i,im in enumerate([k14,k15]):
    W.paste(op(im.crop((X0,Y0,X1,Y1)).resize(((X1-X0)*S,(Y1-Y0)*S),Image.NEAREST)),(10+i*((X1-X0)*S+10),20))
m=Image.open('../../referenties/model.webp').convert('RGB')
mx0=46+(X0-1)*15.3; mx1=46+(X1-1)*15.3; my0=57+(Y0-3)*15.25; my1=57+(Y1-3)*15.25
mc=Image.new('RGB',(int(mx1-mx0),int(my1-my0)),(255,255,255)); mc.paste(m.crop((int(mx0),max(0,int(my0)),int(mx1),int(my1))),(0,max(0,-int(my0))))
W.paste(mc.resize(((X1-X0)*S,(Y1-Y0)*S),Image.LANCZOS),(10+2*((X1-X0)*S+10),20))
y=20+(Y1-Y0)*S+10
d.text((10,y),'k15 8x | 1x op licht/donker',fill=(0,0,0))
W.paste(op(k15.resize((512,512),Image.NEAREST)),(10,y+12))
for j,c in enumerate([(255,255,255),(40,40,48),(152,208,160)]):
    W.paste(op(k15,c),(540+j*74,y+12)); W.paste(op(k14,c),(540+j*74,y+86))
d.text((540,y+156),'boven k15, onder k14 (1x)',fill=(0,0,0))
W.save('vel.png')
