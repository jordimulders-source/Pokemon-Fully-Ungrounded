import sys, numpy as np; sys.path.insert(0,'.'); sys.path.insert(0,'r4')
from PIL import Image, ImageDraw
import bouw
from bouw4 import S, S3
from natcoord import NY, NX, NAT
bouw.P3[12]=(190,92,84); rgb=bouw.rgb
bouw.opslaan(S,'r4/claydol_g3r4.png'); rgb(S).resize((512,512),0).save('r4/claydol_g3r4_8x.png')
Mm=np.full((64,64,3),255,'uint8'); ok=(NY>=0)&(S>0); Mm[ok]=NAT[NY[ok],NX[ok]]; M=Image.fromarray(Mm)   # model per spritepixel (rechterstaf via eigen schrapping)
r4,r3=rgb(S),rgb(S3)
V=Image.new('RGB',(1600,1400),(236,236,236)); d=ImageDraw.Draw(V)
for i,(t,im) in enumerate([('r4',r4),('r3',r3),('model (per spritepixel)',M)]):
    d.text((10+i*530,5),t+' (8x)',fill=(0,0,0)); V.paste(im.resize((512,512),0),(10+i*530,20))
y=545
zones=[('1 neusruggen (ongewijzigd)',(16,17,46,32)),('2 knop rechterstaf',(50,35,64,49)),('3 knop linkerstaf',(0,31,10,44)),('4 treden lijf',(14,41,40,49))]
x=10; rowh=0
for t,(x0,y0,x1,y1) in zones:
    s=12; w,h=(x1-x0)*s,(y1-y0)*s
    if x+3*w+20>1600: x=10; y+=rowh+30; rowh=0
    d.text((x,y),t+': r4 | r3 | model (12x)',fill=(0,0,0))
    for j,im in enumerate([r4,r3,M]): V.paste(im.crop((x0,y0,x1,y1)).resize((w,h),0),(x+j*(w+6),y+15))
    x+=3*(w+6)+30; rowh=max(rowh,h+15)
y+=rowh+30; d.text((10,y),'1x licht / donker',fill=(0,0,0))
Image.open('r4/claydol_g3r4.png').save('/tmp/_r4.png'); sp=Image.open('/tmp/_r4.png').convert('RGBA')
for i,bg in enumerate([(255,255,255),(48,48,56)]):
    b=Image.new('RGBA',(64,64),bg+(255,)); b.alpha_composite(sp); V.paste(b.convert('RGB'),(10+i*80,y+15))
V.crop((0,0,1600,y+90)).save('r4/vel.png')
